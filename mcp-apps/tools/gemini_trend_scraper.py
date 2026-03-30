"""Gemini-powered MCP niche trend discovery.

Identifies trending niches and developer pain points for MCP server products.

Two modes per run:
  1. Current hot niches  — what devs/AI users need RIGHT NOW
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

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
MODEL = "gemini-2.5-flash"
OUTPUT_DIR = Path(__file__).resolve().parents[1] / "research" / "trends"

# ── Prompts ───────────────────────────────────────────────────────────────────

_CURRENT_PROMPT = """You are an expert in developer tools, AI ecosystems, and the MCP (Model Context Protocol) marketplace.

Identify 30 niche use-cases / problem domains that are HOT RIGHT NOW for MCP server products.
Developers and AI power-users are actively looking for MCP servers that solve these needs today.

Focus on:
- Workflow automation gaps (tasks people do manually that AI could handle via MCP)
- Hot SaaS/API integrations developers want in their AI agents (CRMs, project trackers, comms tools)
- Data source connectors with high demand and low existing MCP supply
- Developer productivity niches (code review, CI/CD, infra monitoring)
- Domain-specific AI assistants (finance, legal, e-commerce, marketing, health)
- Thai / Southeast Asian market gaps (local payment systems, local SaaS, local data)

Return ONLY a valid JSON array of 30 objects, no markdown:
[
  {
    "niche": "short MCP product name or category (3-6 words)",
    "trend_score": <float 0-100, 100 = peak demand right now>,
    "velocity": <float -1.0 to 1.0, positive = rising fast>,
    "target_user": "who needs this: role, use-case, willingness to pay",
    "key_integrations": ["top 2-3 APIs or services this MCP would wrap"],
    "competition_level": "none | low | medium | high",
    "monetization": "how to charge: free tier + subscription | one-time | marketplace",
    "reason": "one sentence: why this is in demand right now"
  }
]"""

UPCOMING_HORIZONS = [14, 28, 42, 56, 84, 112]

_UPCOMING_PROMPT_TEMPLATE = """You are an expert in developer tools, AI ecosystems, and the MCP (Model Context Protocol) marketplace.

Today is {today}. Identify 25 niche use-cases for MCP server products that will PEAK in demand
around {peak_date} ({horizon_days} days from now).

Think about:
- Platform launches, API releases, or developer conferences happening around {peak_date}
- Seasonal business workflows that spike at that time (tax season, budget cycles, hiring waves)
- AI ecosystem shifts: new model releases, new agent frameworks going mainstream
- Regulatory or compliance deadlines that force workflow changes
- Growing developer communities that will hit critical mass at that horizon

Return ONLY a valid JSON array of 25 objects, no markdown:
[
  {{
    "niche": "short MCP product name or category (3-6 words)",
    "trend_score": <float 0-100, current score today>,
    "velocity": <float 0.0 to 1.0, rising speed>,
    "upcoming_score": <float 0-100, predicted peak score at {peak_date}>,
    "horizon_days": {horizon_days},
    "peak_date": "{peak_date}",
    "target_user": "who needs this: role, use-case, willingness to pay",
    "key_integrations": ["top 2-3 APIs or services this MCP would wrap"],
    "competition_level": "none | low | medium | high",
    "monetization": "how to charge",
    "reason": "one sentence: what event/shift drives peak demand at {peak_date}"
  }}
]"""


# ── Gemini helpers ────────────────────────────────────────────────────────────

def _call_gemini(prompt: str) -> list[dict]:
    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY not set — check aiProjects/.env")
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
            "target_user": latest.get("target_user"),
            "key_integrations": latest.get("key_integrations"),
            "reason": latest.get("reason"),
        })

    ranked.sort(key=lambda x: x["composite_score"], reverse=True)
    return ranked[:top_n]


# ── Main ──────────────────────────────────────────────────────────────────────

def run():
    today = datetime.now(timezone.utc)
    today_str = today.strftime("%Y-%m-%d")
    print(f"[gemini_trend_scraper] Starting — {today_str}")

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
    print("\n  Top 15 composite-ranked MCP niches (all-time):")
    for i, r in enumerate(get_top_niches(15), 1):
        flag = f" (seen {r['appearances']}x)" if r["appearances"] > 1 else ""
        print(
            f"    {i:>2}. [{r['composite_score']:>5.1f}]{flag} {r['niche']}"
            f"  [{r['competition_level']}] — {r.get('reason', '')[:80]}"
        )

    print("\n[gemini_trend_scraper] Done.")


if __name__ == "__main__":
    run()
