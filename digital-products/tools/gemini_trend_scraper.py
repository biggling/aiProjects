"""Gemini-powered digital products trend discovery.

Identifies trending niches for Gumroad/Etsy digital downloads:
templates, prompt packs, configs, planners, notion templates, etc.

Two modes per run:
  1. Current hot niches  — what buyers need RIGHT NOW
  2. Upcoming niches     — what will be hot in 2-16 weeks

Results saved as JSON snapshots in research/trends/ for historical comparison.
"""
import json
import os
import re
from datetime import datetime, timezone, timedelta
from pathlib import Path

from dotenv import load_dotenv
from google import genai

# Load from workspace root .env first, then local .env
_ROOT = Path(__file__).resolve().parents[2]  # aiProjects/
load_dotenv(_ROOT / ".env")
load_dotenv(Path(__file__).resolve().parents[1] / ".env", override=False)
# Also try mcp-apps .env for the key
load_dotenv(_ROOT / "mcp-apps" / ".env", override=False)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
MODEL = "gemini-2.5-flash"
OUTPUT_DIR = Path(__file__).resolve().parents[1] / "research" / "trends"

# ── Prompts ───────────────────────────────────────────────────────────────────

_CURRENT_PROMPT = """You are an expert in digital products, indie hacking, and the Gumroad/Etsy/Lemon Squeezy marketplace for creators and developers.

Identify 30 niche product categories that are HOT RIGHT NOW for digital downloads targeting developers, AI power-users, indie hackers, and creators.

Products include: Notion templates, prompt packs, AI workflow configs, code templates, productivity planners, spreadsheet tools, Figma UI kits, script bundles, tutorial PDFs, toolkits, and config packs.

Focus on buyer intent in 2026:
- AI coding tools ecosystem (Claude Code, Cursor, Windsurf, OpenCode configs and workflows)
- Developer productivity (project planning, code review templates, sprint planners)
- AI prompt engineering (prompt packs for GPT-4, Claude, Gemini for specific workflows)
- Solo founder / indie hacker toolkits (business templates, revenue trackers, launch checklists)
- Non-developer AI users (designers, marketers, writers using AI tools daily)
- Notion ecosystem (database templates, dashboards, CRM/project management systems)
- Freelancer/agency tools (client onboarding, proposal templates, invoice systems)
- Passive income systems (affiliate tracking, newsletter templates, content calendars)

Return ONLY a valid JSON array of 30 objects, no markdown:
[
  {
    "niche": "short product name or category (3-6 words)",
    "trend_score": <float 0-100, 100 = peak demand right now>,
    "velocity": <float -1.0 to 1.0, positive = rising fast>,
    "target_buyer": "who buys this: role, use-case, willingness to pay",
    "platform_fit": ["Gumroad", "Etsy", "Lemon Squeezy"],
    "price_range": "$X-$Y",
    "competition_level": "none | low | medium | high",
    "format": "ZIP | PDF | Notion template | spreadsheet | video course | mixed",
    "reason": "one sentence: why this is in demand right now"
  }
]"""

UPCOMING_HORIZONS = [14, 28, 42, 56, 84, 112]

_UPCOMING_PROMPT_TEMPLATE = """You are an expert in digital products, indie hacking, and the Gumroad/Etsy/Lemon Squeezy marketplace.

Today is {today}. Identify 25 digital product niches that will PEAK in demand around {peak_date} ({horizon_days} days from now).

Products: Notion templates, prompt packs, AI workflow configs, productivity planners, code templates, toolkits, PDFs.
Buyers: developers, AI power-users, indie hackers, creators, non-technical founders.

Think about what will drive demand at that horizon:
- AI ecosystem events: new model launches, tool releases, agent framework updates
- Seasonal business cycles: Q2 planning, mid-year review templates, tax tools, budget planners
- Indie hacker / startup events: major conferences, Product Hunt trends, launch calendar waves
- Platform policy changes affecting creators (Etsy, Gumroad, Notion updates)
- Growing communities hitting critical mass (vibe coders, solopreneurs, AI-first teams)
- Developer tool adoption waves (new IDEs, frameworks, workflow tools going mainstream)

Return ONLY a valid JSON array of 25 objects, no markdown:
[
  {{
    "niche": "short product name or category (3-6 words)",
    "trend_score": <float 0-100, current score today>,
    "velocity": <float 0.0 to 1.0, rising speed>,
    "upcoming_score": <float 0-100, predicted peak score at {peak_date}>,
    "horizon_days": {horizon_days},
    "peak_date": "{peak_date}",
    "target_buyer": "who buys this: role, use-case, willingness to pay",
    "platform_fit": ["Gumroad", "Etsy"],
    "price_range": "$X-$Y",
    "competition_level": "none | low | medium | high",
    "format": "ZIP | PDF | Notion template | spreadsheet | mixed",
    "reason": "one sentence: what event/shift drives peak demand at {peak_date}"
  }}
]"""


# ── Gemini helpers ────────────────────────────────────────────────────────────

def _call_gemini(prompt: str) -> list[dict]:
    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY not set — check aiProjects/.env or mcp-apps/.env")
    client = genai.Client(api_key=GEMINI_API_KEY)
    response = client.models.generate_content(model=MODEL, contents=prompt)
    text = response.text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        last = text.rfind("},")
        if last == -1:
            last = text.rfind("}")
        if last != -1:
            return json.loads(text[: last + 1].rstrip(",") + "\n]")
        raise


# ── Persistence ───────────────────────────────────────────────────────────────

def _save_snapshot(tag: str, data: list[dict]) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")
    path = OUTPUT_DIR / f"{ts}_{tag}.json"
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False))
    return path


def _load_all_snapshots() -> list[dict]:
    """Load all saved current-trend snapshots for composite ranking."""
    snapshots = []
    for f in sorted(OUTPUT_DIR.glob("*_current.json")):
        try:
            items = json.loads(f.read_text())
            for item in items:
                item["_snapshot_file"] = f.name
            snapshots.extend(items)
        except Exception:
            pass
    return snapshots


# ── Composite ranking ─────────────────────────────────────────────────────────

def get_top_niches(top_n: int = 20) -> list[dict]:
    """Aggregate all current snapshots, average scores per niche, rank by composite."""
    raw = _load_all_snapshots()
    if not raw:
        return []

    by_niche: dict[str, list[dict]] = {}
    for item in raw:
        key = item.get("niche", "").strip().lower()
        if key:
            by_niche.setdefault(key, []).append(item)

    ranked = []
    for niche, entries in by_niche.items():
        avg_score = sum(e.get("trend_score", 0) for e in entries) / len(entries)
        avg_vel = sum(e.get("velocity", 0) for e in entries) / len(entries)
        composite = avg_score * (1 + avg_vel * 0.2)
        latest = max(entries, key=lambda e: e.get("_snapshot_file", ""))
        ranked.append({
            "niche": niche,
            "composite_score": round(composite, 2),
            "avg_trend_score": round(avg_score, 2),
            "avg_velocity": round(avg_vel, 3),
            "appearances": len(entries),
            "competition_level": latest.get("competition_level"),
            "target_buyer": latest.get("target_buyer"),
            "price_range": latest.get("price_range"),
            "format": latest.get("format"),
            "reason": latest.get("reason"),
        })

    ranked.sort(key=lambda x: x["composite_score"], reverse=True)
    return ranked[:top_n]


# ── Main ──────────────────────────────────────────────────────────────────────

def run():
    today = datetime.now(timezone.utc)
    today_str = today.strftime("%Y-%m-%d")
    print(f"[digital_trend_scraper] Starting — {today_str}")

    # Step 1: current trends
    print("  Fetching current hot niches...")
    current = _call_gemini(_CURRENT_PROMPT)
    current.sort(key=lambda x: x.get("trend_score", 0), reverse=True)
    path = _save_snapshot("current", current)
    print(f"  Saved {len(current)} niches → {path.name}")

    # Step 2: upcoming horizons
    for days in UPCOMING_HORIZONS:
        peak_date = (today + timedelta(days=days)).strftime("%Y-%m-%d")
        label = f"{days}d"
        print(f"  Fetching upcoming niches — {label} horizon (peak ~{peak_date})...")
        prompt = _UPCOMING_PROMPT_TEMPLATE.format(
            today=today_str,
            peak_date=peak_date,
            horizon_days=days,
        )
        try:
            items = _call_gemini(prompt)
            items.sort(key=lambda x: x.get("upcoming_score", 0), reverse=True)
            p = _save_snapshot(f"upcoming_{label}", items)
            print(f"    Saved {len(items)} niches → {p.name}")
        except Exception as e:
            print(f"    WARNING: parse error for {label} horizon: {e}")

    # Step 3: print composite rankings
    print("\n  Top 15 composite-ranked digital product niches (all-time):")
    for i, r in enumerate(get_top_niches(15), 1):
        flag = f" (seen {r['appearances']}x)" if r["appearances"] > 1 else ""
        print(
            f"    {i:>2}. [{r['composite_score']:>5.1f}]{flag} {r['niche']}"
            f"  [{r['competition_level']}] {r.get('price_range', '')} — {r.get('reason', '')[:80]}"
        )

    print("\n[digital_trend_scraper] Done.")


if __name__ == "__main__":
    run()
