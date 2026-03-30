"""Gemini-powered micro-SaaS opportunity trend scraper.

Calls Gemini across four lenses each run:
  1. Current pain points  — seller/dev pain trending RIGHT NOW
  2. Market gaps          — missing tools with no good SaaS solution yet
  3. Competitor signals   — tools that are overpriced, bugged, or abandoned
  4. Emerging platforms   — new ecosystems that will need tooling

Saves a timestamped markdown findings file to research/findings/ and
optionally patches the Known Facts section of research/AGENT.md.

Usage:
    python tools/gemini_trends_scraper.py [--update-agent] [--dry-run]

Env:
    GEMINI_API_KEY  — required
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

# ---------------------------------------------------------------------------
# Load .env — check micro-saas/.env first, then ../pod/.env (shared key)
# ---------------------------------------------------------------------------
try:
    from dotenv import load_dotenv
    _here = Path(__file__).parent.parent
    for _env in [_here / ".env", _here.parent / "pod" / ".env"]:
        if _env.exists():
            load_dotenv(_env)
            break
except ImportError:
    pass

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).parent
PROJECT_DIR = SCRIPT_DIR.parent
FINDINGS_DIR = PROJECT_DIR / "research" / "findings"
AGENT_MD = PROJECT_DIR / "research" / "AGENT.md"

# ---------------------------------------------------------------------------
# Gemini config
# ---------------------------------------------------------------------------
MODEL = "gemini-2.5-flash"

# ---------------------------------------------------------------------------
# Prompts
# ---------------------------------------------------------------------------

TODAY = datetime.now(timezone.utc).strftime("%Y-%m-%d")

_PAIN_POINTS_PROMPT = f"""You are an expert micro-SaaS market researcher with deep knowledge of
global e-commerce platforms (Amazon, Etsy, TikTok Shop, Shopify, eBay), developer tools, and SMB software.

Today is {TODAY}. Identify 20 specific pain points that are ACTIVELY TRENDING right now among:
- E-commerce sellers globally (Amazon FBA/FBM, Etsy, TikTok Shop US/UK/EU, Shopify merchants)
- Freelancers and solo developers worldwide (US, EU, UK, AU primary markets)
- SMB owners dealing with compliance or operational headaches (global English-speaking markets)

Focus on pains that:
- Have NO existing affordable SaaS solution (under $50/month)
- Generate strong "would pay to fix this" frustration in English-speaking communities
- Are measurable (you can see them causing lost revenue or wasted hours)
- Are acute RIGHT NOW due to platform policy changes, compliance deadlines, or market shifts

Return ONLY a valid JSON array of 20 objects, no markdown:
[
  {{
    "pain": "one-sentence description of the exact problem",
    "persona": "who experiences this (role + platform/context)",
    "frequency": "how often this pain hits (daily/weekly/event-driven)",
    "urgency": <float 0-100, 100=bleeding emergency right now>,
    "existing_tools": ["tools that partially address this, or empty if none"],
    "gap": "what existing tools miss or why they're inadequate",
    "revenue_impact": "how this pain translates to lost money or time",
    "reason_trending_now": "one sentence: why is this acute in {TODAY}"
  }}
]"""

_MARKET_GAPS_PROMPT = f"""You are an expert micro-SaaS market researcher. Today is {TODAY}.

Identify 15 specific software gaps — problems where no dedicated micro-SaaS exists at an
affordable price ($5–$50/month) that a solo developer could build in 1-4 weekends.

Focus on gaps in these verticals:
- E-commerce operations (Amazon, Etsy, TikTok Shop, Shopify — global seller tooling)
- Developer utilities (webhook management, API monitoring, CI/CD helpers, observability)
- Compliance automation (EU AI Act, SOC2, GDPR, global e-invoicing mandates)
- Small team operations (scheduling, invoicing, reporting for <10 person teams)
- Content creator tools (YouTube, newsletter, podcast monetization and analytics)

For each gap, assess build complexity honestly (1 = trivial CRUD, 5 = complex ML).

Return ONLY a valid JSON array of 15 objects, no markdown:
[
  {{
    "gap_name": "short product concept name (3-6 words)",
    "problem": "one-sentence: what problem does this solve",
    "target_persona": "who pays for this",
    "why_no_solution_exists": "one sentence: why hasn't someone built this",
    "build_complexity": <int 1-5>,
    "monetization": "suggested pricing model and price point",
    "market_size_signal": "rough estimate of addressable users",
    "urgency": <float 0-100>,
    "adjacent_competition": ["tools that are close but miss the mark"],
    "mvp_core_feature": "the single feature that makes the MVP viable"
  }}
]"""

_COMPETITOR_SIGNALS_PROMPT = f"""You are an expert micro-SaaS market researcher. Today is {TODAY}.

Identify 12 existing SaaS tools (in global e-commerce, developer tooling, or SMB software) that are:
- Overpriced with a clear gap in the $10-$50/month tier
- Widely complained about in Reddit/Twitter/Indie Hackers for bugs or missing features
- Recently abandoned or deprioritized by their founders
- Enterprise-only with no SMB/indie option

These are "displacement opportunities" — niches where a focused micro-SaaS can win by being
simpler, cheaper, or better at one specific thing.

Return ONLY a valid JSON array of 12 objects, no markdown:
[
  {{
    "tool_name": "existing tool name",
    "category": "what category it's in",
    "pricing_gap": "where the pricing cliff or gap is",
    "top_complaint": "the #1 thing users hate (from community feedback)",
    "displacement_angle": "how a micro-SaaS could win against this tool",
    "target_switcher": "which user segment would switch first and why",
    "urgency": <float 0-100>,
    "evidence_source": "where this signal comes from (Reddit, G2, community, etc.)"
  }}
]"""

_EMERGING_PLATFORMS_PROMPT = f"""You are an expert micro-SaaS market researcher. Today is {TODAY}.

Identify 10 emerging platforms, APIs, or ecosystems that are growing fast and will need
new tooling, integrations, or monitoring tools in the next 3-12 months.

Think about:
- New AI platforms (agents, LLM APIs, AI coding tools) with monetization or compliance needs
- E-commerce platforms expanding globally (TikTok Shop EU/AU, Amazon new regions)
- Regulatory changes creating new compliance software needs (EU AI Act, US state privacy laws, global e-invoicing)
- Developer platforms with API ecosystems that need observability/management tools
- Creator economy platforms (Substack, Beehiiv, Spotify for Podcasters, YouTube) needing business tooling

Return ONLY a valid JSON array of 10 objects, no markdown:
[
  {{
    "platform": "name of platform or ecosystem",
    "why_growing": "one sentence on growth driver",
    "tooling_need": "what software will be needed that doesn't exist yet",
    "timing": "when is the window (months from now)",
    "first_mover_advantage": <float 0-100, 100=massive advantage to move now>,
    "build_window": "estimated time to ship MVP before market saturates",
    "monetization_potential": "rough revenue ceiling at scale"
  }}
]"""

# ---------------------------------------------------------------------------
# Gemini client
# ---------------------------------------------------------------------------

def _call_gemini(prompt: str) -> list[dict]:
    """Call Gemini and parse JSON response. Returns empty list on failure."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable is not set")

    try:
        from google import genai
    except ImportError:
        raise RuntimeError(
            "google-genai is not installed. Run: pip install google-genai"
        )

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(model=MODEL, contents=prompt)
    text = response.text.strip()

    # Strip markdown code fences if present
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # Truncate to last complete JSON object
        last_obj = text.rfind("},")
        if last_obj == -1:
            last_obj = text.rfind("}")
        if last_obj != -1:
            truncated = text[: last_obj + 1].rstrip(",") + "\n]"
            return json.loads(truncated)
        raise


# ---------------------------------------------------------------------------
# Markdown rendering
# ---------------------------------------------------------------------------

def _render_pain_points(items: list[dict]) -> str:
    lines = ["## Current Pain Points — Trending NOW\n"]
    for i, item in enumerate(sorted(items, key=lambda x: x.get("urgency", 0), reverse=True), 1):
        lines.append(f"### {i}. {item.get('pain', 'N/A')}")
        lines.append(f"- **Persona**: {item.get('persona', '')}")
        lines.append(f"- **Urgency**: {item.get('urgency', 0):.0f}/100 | **Frequency**: {item.get('frequency', '')}")
        lines.append(f"- **Gap**: {item.get('gap', '')}")
        lines.append(f"- **Revenue impact**: {item.get('revenue_impact', '')}")
        lines.append(f"- **Why now**: {item.get('reason_trending_now', '')}")
        existing = item.get("existing_tools", [])
        if existing:
            lines.append(f"- **Existing tools**: {', '.join(existing)}")
        lines.append("")
    return "\n".join(lines)


def _render_market_gaps(items: list[dict]) -> str:
    lines = ["## Market Gaps — No SaaS Solution Exists\n"]
    for i, item in enumerate(sorted(items, key=lambda x: x.get("urgency", 0), reverse=True), 1):
        complexity = "⭐" * item.get("build_complexity", 3)
        lines.append(f"### {i}. {item.get('gap_name', 'N/A')} `{complexity}`")
        lines.append(f"- **Problem**: {item.get('problem', '')}")
        lines.append(f"- **Target**: {item.get('target_persona', '')}")
        lines.append(f"- **Urgency**: {item.get('urgency', 0):.0f}/100")
        lines.append(f"- **Monetization**: {item.get('monetization', '')}")
        lines.append(f"- **Market signal**: {item.get('market_size_signal', '')}")
        lines.append(f"- **MVP feature**: {item.get('mvp_core_feature', '')}")
        lines.append(f"- **Why no one built it**: {item.get('why_no_solution_exists', '')}")
        competition = item.get("adjacent_competition", [])
        if competition:
            lines.append(f"- **Adjacent tools**: {', '.join(competition)}")
        lines.append("")
    return "\n".join(lines)


def _render_competitor_signals(items: list[dict]) -> str:
    lines = ["## Competitor Displacement Signals\n"]
    for i, item in enumerate(sorted(items, key=lambda x: x.get("urgency", 0), reverse=True), 1):
        lines.append(f"### {i}. {item.get('tool_name', 'N/A')} — {item.get('category', '')}")
        lines.append(f"- **Pricing gap**: {item.get('pricing_gap', '')}")
        lines.append(f"- **Top complaint**: {item.get('top_complaint', '')}")
        lines.append(f"- **How to win**: {item.get('displacement_angle', '')}")
        lines.append(f"- **Target switcher**: {item.get('target_switcher', '')}")
        lines.append(f"- **Urgency**: {item.get('urgency', 0):.0f}/100")
        lines.append(f"- **Evidence**: {item.get('evidence_source', '')}")
        lines.append("")
    return "\n".join(lines)


def _render_emerging_platforms(items: list[dict]) -> str:
    lines = ["## Emerging Platforms — First-Mover Tooling Opportunities\n"]
    for i, item in enumerate(sorted(items, key=lambda x: x.get("first_mover_advantage", 0), reverse=True), 1):
        lines.append(f"### {i}. {item.get('platform', 'N/A')}")
        lines.append(f"- **Why growing**: {item.get('why_growing', '')}")
        lines.append(f"- **Tooling need**: {item.get('tooling_need', '')}")
        lines.append(f"- **Timing**: {item.get('timing', '')} | **Build window**: {item.get('build_window', '')}")
        lines.append(f"- **First-mover advantage**: {item.get('first_mover_advantage', 0):.0f}/100")
        lines.append(f"- **Revenue ceiling**: {item.get('monetization_potential', '')}")
        lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Top opportunities summary
# ---------------------------------------------------------------------------

def _top_opportunities(
    pain_points: list[dict],
    gaps: list[dict],
    competitors: list[dict],
    platforms: list[dict],
) -> str:
    lines = ["## Top Opportunities (Combined Signal)\n"]

    # Score each gap by urgency, boosted if there's a matching pain point
    gap_scores = []
    for i, g in enumerate(gaps):
        score = g.get("urgency", 0)
        # Boost if build complexity is low
        complexity = g.get("build_complexity", 3)
        if complexity <= 2:
            score *= 1.2
        gap_scores.append((score, i, g))
    gap_scores.sort(key=lambda x: x[0], reverse=True)

    lines.append("### Build These First\n")
    for score, _, g in gap_scores[:5]:
        complexity_stars = "⭐" * g.get("build_complexity", 3)
        lines.append(
            f"- **{g.get('gap_name')}** `{complexity_stars}` "
            f"(score: {score:.0f}) — {g.get('problem', '')} "
            f"| Target: {g.get('target_persona', '')} "
            f"| Price: {g.get('monetization', '')}"
        )

    lines.append("\n### Hottest Pain Points Right Now\n")
    hot = sorted(pain_points, key=lambda x: x.get("urgency", 0), reverse=True)[:5]
    for p in hot:
        lines.append(
            f"- **{p.get('pain', '')}** (urgency: {p.get('urgency', 0):.0f}) "
            f"— {p.get('persona', '')}"
        )

    lines.append("\n### Easiest Competitor Displacement\n")
    easy = sorted(competitors, key=lambda x: x.get("urgency", 0), reverse=True)[:3]
    for c in easy:
        lines.append(
            f"- **{c.get('tool_name')}** — {c.get('displacement_angle', '')} "
            f"| Switcher: {c.get('target_switcher', '')}"
        )

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Save findings
# ---------------------------------------------------------------------------

def save_findings(
    pain_points: list[dict],
    gaps: list[dict],
    competitors: list[dict],
    platforms: list[dict],
    dry_run: bool = False,
) -> Path:
    now = datetime.now(timezone.utc)
    filename = now.strftime("%Y-%m-%d_%H%M") + ".md"
    out_path = FINDINGS_DIR / filename

    header = f"# micro-saas Research — {now.strftime('%Y-%m-%d_%H%M')}\n\n"
    header += f"_Generated by gemini_trends_scraper.py using {MODEL}_\n\n"
    header += "---\n\n"

    content = (
        header
        + _top_opportunities(pain_points, gaps, competitors, platforms)
        + "\n\n---\n\n"
        + _render_pain_points(pain_points)
        + "\n---\n\n"
        + _render_market_gaps(gaps)
        + "\n---\n\n"
        + _render_competitor_signals(competitors)
        + "\n---\n\n"
        + _render_emerging_platforms(platforms)
    )

    if dry_run:
        print(content)
    else:
        FINDINGS_DIR.mkdir(parents=True, exist_ok=True)
        out_path.write_text(content, encoding="utf-8")
        # Update latest symlink
        latest = FINDINGS_DIR / "latest.md"
        if latest.exists() or latest.is_symlink():
            latest.unlink()
        latest.symlink_to(filename)
        print(f"Saved: {out_path}")

    return out_path


# ---------------------------------------------------------------------------
# Patch AGENT.md Known Facts
# ---------------------------------------------------------------------------

_KNOWN_FACTS_MARKER_START = "## Known Facts"
_KNOWN_FACTS_MARKER_END = "\n## "  # next H2 section


def patch_agent_md(gaps: list[dict], pain_points: list[dict], dry_run: bool = False) -> None:
    """Insert top-scoring new facts into the Known Facts section of AGENT.md."""
    if not AGENT_MD.exists():
        print(f"Warning: {AGENT_MD} not found, skipping patch")
        return

    text = AGENT_MD.read_text(encoding="utf-8")

    # Build new fact lines from top gaps and pain points
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    new_lines = []

    top_gaps = sorted(gaps, key=lambda x: x.get("urgency", 0), reverse=True)[:3]
    for g in top_gaps:
        fact = (
            f"- **{g.get('gap_name')}**: {g.get('problem', '')} — "
            f"{g.get('why_no_solution_exists', '')} "
            f"Price: {g.get('monetization', '')}. [{today}, Gemini]"
        )
        if fact not in text:
            new_lines.append(fact)

    top_pains = sorted(pain_points, key=lambda x: x.get("urgency", 0), reverse=True)[:3]
    for p in top_pains:
        fact = (
            f"- **Pain — {p.get('persona', '')}**: {p.get('pain', '')} — "
            f"{p.get('gap', '')} [{today}, Gemini]"
        )
        if fact not in text:
            new_lines.append(fact)

    if not new_lines:
        print("No new facts to add to AGENT.md")
        return

    # Find insertion point: after "## Known Facts" header, before next H2
    start_idx = text.find(_KNOWN_FACTS_MARKER_START)
    if start_idx == -1:
        print("Warning: '## Known Facts' not found in AGENT.md, skipping patch")
        return

    # Find the first blank line or content line after the header
    after_header = text.find("\n", start_idx) + 1
    # Skip the comment line if present
    comment_end = text.find("\n", after_header)
    insert_at = comment_end + 1

    insertion = "\n### Gemini Scraper — Latest Signals\n" + "\n".join(new_lines) + "\n"

    patched = text[:insert_at] + insertion + text[insert_at:]

    if dry_run:
        print("\n--- AGENT.md patch preview ---")
        print(insertion)
    else:
        AGENT_MD.write_text(patched, encoding="utf-8")
        print(f"Patched {AGENT_MD} with {len(new_lines)} new facts")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def run(update_agent: bool = False, dry_run: bool = False) -> None:
    print(f"[gemini_trends_scraper] Starting — model={MODEL}, date={TODAY}")

    print("  Fetching current pain points...")
    try:
        pain_points = _call_gemini(_PAIN_POINTS_PROMPT)
        print(f"  Got {len(pain_points)} pain points")
    except Exception as e:
        print(f"  ERROR fetching pain points: {e}")
        pain_points = []

    print("  Fetching market gaps...")
    try:
        gaps = _call_gemini(_MARKET_GAPS_PROMPT)
        print(f"  Got {len(gaps)} market gaps")
    except Exception as e:
        print(f"  ERROR fetching gaps: {e}")
        gaps = []

    print("  Fetching competitor signals...")
    try:
        competitors = _call_gemini(_COMPETITOR_SIGNALS_PROMPT)
        print(f"  Got {len(competitors)} competitor signals")
    except Exception as e:
        print(f"  ERROR fetching competitor signals: {e}")
        competitors = []

    print("  Fetching emerging platforms...")
    try:
        platforms = _call_gemini(_EMERGING_PLATFORMS_PROMPT)
        print(f"  Got {len(platforms)} platform opportunities")
    except Exception as e:
        print(f"  ERROR fetching platform signals: {e}")
        platforms = []

    if not any([pain_points, gaps, competitors, platforms]):
        print("ERROR: All Gemini calls failed. Check GEMINI_API_KEY.")
        sys.exit(1)

    out_path = save_findings(pain_points, gaps, competitors, platforms, dry_run=dry_run)

    if update_agent and not dry_run:
        patch_agent_md(gaps, pain_points, dry_run=dry_run)
    elif update_agent and dry_run:
        patch_agent_md(gaps, pain_points, dry_run=True)

    print(f"\nDone. Findings: {out_path}")

    # Print top 3 opportunities to stdout for quick visibility
    print("\n=== TOP 3 GAPS BY URGENCY ===")
    top = sorted(gaps, key=lambda x: x.get("urgency", 0), reverse=True)[:3]
    for i, g in enumerate(top, 1):
        print(f"  {i}. [{g.get('urgency', 0):.0f}] {g.get('gap_name')} — {g.get('problem', '')}")

    print("\n=== TOP 3 PAIN POINTS BY URGENCY ===")
    top_pains = sorted(pain_points, key=lambda x: x.get("urgency", 0), reverse=True)[:3]
    for i, p in enumerate(top_pains, 1):
        print(f"  {i}. [{p.get('urgency', 0):.0f}] {p.get('pain', '')}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gemini micro-SaaS opportunity trend scraper")
    parser.add_argument(
        "--update-agent",
        action="store_true",
        help="Patch new facts into research/AGENT.md Known Facts section",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print output to stdout instead of writing files",
    )
    args = parser.parse_args()
    run(update_agent=args.update_agent, dry_run=args.dry_run)
