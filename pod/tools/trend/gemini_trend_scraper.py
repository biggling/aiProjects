"""Gemini-powered trend discovery with historical snapshot persistence.

Two modes per run:
  1. Current trends  — top 20 niches active right now
  2. Upcoming trends — top 15 niches predicted to peak in the next 14-28 days

Both are saved as TrendSnapshot rows (is_upcoming=False / True).
Snapshots accumulate over time, enabling trend-over-time comparison and
popularity ranking across sources (Gemini, pytrends, Reddit, Etsy).
"""
import json
import re
from datetime import datetime, timezone, timedelta

from google import genai
from sqlalchemy import select, func as sqlfunc

from tools.shared.config import GEMINI_API_KEY
from tools.shared.db import get_session
from tools.shared.models import Niche, TrendSnapshot
from tools.shared.logger import get_logger

logger = get_logger("gemini_trend_scraper")

MODEL = "gemini-2.5-flash"

# ── Prompts ───────────────────────────────────────────────────────────────────

_CURRENT_TRENDS_PROMPT = """You are an expert Etsy print-on-demand market researcher.

Identify 40 niche keywords that are CURRENTLY trending and have strong buying
intent on Etsy for POD products (t-shirts, hoodies, mugs, tote bags, stickers).

Focus on:
- Seasonal and holiday themes active in the next 30 days
- Viral pop-culture moments, memes, or social movements
- Profession and identity groups (nurses, teachers, dog moms, gamers)
- Hobby and lifestyle niches (hiking, yoga, gardening, reading)
- Humor and motivational niches with evergreen appeal
- Underserved micro-niches with low competition but rising search volume

Return ONLY a valid JSON array of 40 objects, no markdown:
[
  {
    "keyword": "short Etsy search phrase (2-5 words)",
    "trend_score": <float 0-100, 100=peak right now>,
    "velocity": <float -1.0 to 1.0, positive=rising>,
    "target_customer": "age range, identity/role, occasion, price sensitivity",
    "recommended_products": ["top 2-3 POD product types from: t-shirt, hoodie, sweatshirt, mug, tote, sticker, tumbler, hat"],
    "design_pattern": "visual style and theme (font style, colors, motif)",
    "reason": "one sentence on why this is trending NOW"
  }
]"""

# Upcoming horizons: every 2 weeks from 2 weeks to 4 months
# (14, 28, 42, 56, 70, 84, 98, 112 days)
UPCOMING_HORIZONS = [14, 28, 42, 56, 70, 84, 98, 112]

_UPCOMING_PROMPT_TEMPLATE = """You are an expert Etsy print-on-demand market researcher.

Today is {today}. Identify 40 niche keywords that will PEAK on Etsy
around {peak_date} ({horizon_days} days from now) for POD products
(t-shirts, hoodies, mugs, tote bags, stickers).

Think about what buyers will be actively searching on Etsy in ~{horizon_days} days:
- Holidays, observances, and seasonal events peaking around {peak_date}
- Sports seasons, playoffs, championships happening at that time
- Awareness months, cultural moments, or annual events at that window
- Seasonal buying patterns (summer, back-to-school, fall, holidays, etc.)
- Trends that take {horizon_days} days to go from seed to peak search volume

Return ONLY a valid JSON array of 40 objects, no markdown:
[
  {{
    "keyword": "short Etsy search phrase (2-5 words)",
    "trend_score": <float 0-100, current score today>,
    "velocity": <float 0.0 to 1.0, rising speed>,
    "upcoming_score": <float 0-100, predicted peak score at {peak_date}>,
    "horizon_days": {horizon_days},
    "peak_date": "{peak_date}",
    "target_customer": "age range, identity/role, occasion, price sensitivity",
    "recommended_products": ["top 2-3 POD product types from: t-shirt, hoodie, sweatshirt, mug, tote, sticker, tumbler, hat"],
    "design_pattern": "visual style and theme (font style, colors, motif)",
    "reason": "one sentence: what event/moment drives this and when"
  }}
]"""


# ── Helpers ───────────────────────────────────────────────────────────────────

def _call_gemini(prompt: str) -> list[dict]:
    """Call Gemini and parse JSON response."""
    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY is not set")

    client = genai.Client(api_key=GEMINI_API_KEY)
    response = client.models.generate_content(model=MODEL, contents=prompt)
    text = response.text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # Truncate to the last complete object and close the array
        last_obj = text.rfind("},")
        if last_obj == -1:
            last_obj = text.rfind("}")
        if last_obj != -1:
            truncated = text[: last_obj + 1].rstrip(",") + "\n]"
            return json.loads(truncated)
        raise


def _get_or_create_niche(session, keyword: str) -> Niche:
    niche = session.execute(
        select(Niche).where(Niche.keyword == keyword)
    ).scalar_one_or_none()
    if not niche:
        niche = Niche(keyword=keyword, status="active")
        session.add(niche)
        session.flush()  # get niche.id
    return niche


def _rank_items(items: list[dict]) -> list[tuple[dict, int]]:
    """Sort by trend_score desc and attach rank position (1-based)."""
    sorted_items = sorted(items, key=lambda x: x.get("trend_score", 0), reverse=True)
    return [(item, rank + 1) for rank, item in enumerate(sorted_items)]


# ── Core save functions ───────────────────────────────────────────────────────

def save_current_trends(trends: list[dict]) -> int:
    """Upsert Niche rows and write TrendSnapshot rows for current trends."""
    ranked = _rank_items(trends)
    now = datetime.now(timezone.utc)
    saved = 0

    with get_session() as session:
        for item, rank in ranked:
            keyword = item.get("keyword", "").strip().lower()
            if not keyword:
                continue

            niche = _get_or_create_niche(session, keyword)

            # Update niche with latest Gemini data
            niche.trend_score = float(item.get("trend_score", niche.trend_score or 50.0))
            niche.velocity = float(item.get("velocity", niche.velocity or 0.0))
            niche.gemini_reason = item.get("reason")
            niche.target_customer = item.get("target_customer")
            niche.recommended_products = item.get("recommended_products")
            niche.design_pattern = item.get("design_pattern")

            # Merge into source_scores breakdown
            scores = niche.source_scores or {}
            scores["gemini"] = niche.trend_score
            niche.source_scores = scores

            # Write snapshot row
            snapshot = TrendSnapshot(
                niche_id=niche.id,
                source="gemini",
                trend_score=niche.trend_score,
                velocity=niche.velocity,
                rank_position=rank,
                reason=item.get("reason"),
                is_upcoming=False,
                snapshot_date=now,
            )
            session.add(snapshot)
            saved += 1

    return saved


def save_upcoming_trends(trends: list[dict]) -> int:
    """Upsert Niche rows and write TrendSnapshot rows for upcoming trends."""
    ranked = _rank_items(trends)
    now = datetime.now(timezone.utc)
    saved = 0

    with get_session() as session:
        for item, rank in ranked:
            keyword = item.get("keyword", "").strip().lower()
            if not keyword:
                continue

            niche = _get_or_create_niche(session, keyword)

            # Update upcoming_score on the niche (preserve existing trend_score)
            upcoming = float(item.get("upcoming_score", item.get("trend_score", 50.0)))
            niche.upcoming_score = upcoming
            if not niche.trend_score:
                niche.trend_score = float(item.get("trend_score", 40.0))
            if not niche.velocity:
                niche.velocity = float(item.get("velocity", 0.3))
            if item.get("target_customer"):
                niche.target_customer = item.get("target_customer")
            if item.get("recommended_products"):
                niche.recommended_products = item.get("recommended_products")
            if item.get("design_pattern"):
                niche.design_pattern = item.get("design_pattern")

            scores = niche.source_scores or {}
            scores["gemini_upcoming"] = upcoming
            niche.source_scores = scores

            # Write upcoming snapshot
            snapshot = TrendSnapshot(
                niche_id=niche.id,
                source="gemini",
                trend_score=float(item.get("trend_score", 40.0)),
                velocity=float(item.get("velocity", 0.3)),
                rank_position=rank,
                reason=item.get("reason"),
                is_upcoming=True,
                horizon_days=int(item.get("horizon_days", 14)),
                snapshot_date=now,
            )
            session.add(snapshot)
            saved += 1

    return saved


# ── Ranking helpers ───────────────────────────────────────────────────────────

def get_trend_rankings(top_n: int = 20) -> list[dict]:
    """Return niches ranked by composite popularity across all snapshot sources.

    Composite score = weighted average of last snapshot per source:
      gemini     × 0.40
      pytrends   × 0.30
      reddit     × 0.15
      etsy       × 0.15
    Velocity boost: score × (1 + velocity × 0.2)
    Upcoming multiplier: niches with upcoming_score > trend_score get a +10% bonus.
    """
    weights = {"gemini": 0.40, "pytrends": 0.30, "reddit": 0.15, "etsy": 0.15}

    with get_session() as session:
        niches = session.execute(
            select(Niche).where(Niche.status == "active")
        ).scalars().all()

        results = []
        for niche in niches:
            # Latest snapshot per source
            source_data: dict[str, TrendSnapshot] = {}
            for snap in niche.snapshots:
                if not snap.is_upcoming:
                    existing = source_data.get(snap.source)
                    if not existing or snap.snapshot_date > existing.snapshot_date:
                        source_data[snap.source] = snap

            if not source_data:
                continue

            composite = 0.0
            total_weight = 0.0
            for src, snap in source_data.items():
                w = weights.get(src, 0.10)
                composite += (snap.trend_score or 0) * w
                total_weight += w

            if total_weight > 0:
                composite /= total_weight

            # Velocity boost
            avg_vel = sum(
                (s.velocity or 0) for s in source_data.values()
            ) / len(source_data)
            composite *= 1 + (avg_vel * 0.2)

            # Upcoming bonus
            if niche.upcoming_score and niche.upcoming_score > (niche.trend_score or 0):
                composite *= 1.10

            results.append({
                "keyword": niche.keyword,
                "composite_score": round(composite, 2),
                "trend_score": niche.trend_score,
                "velocity": niche.velocity,
                "upcoming_score": niche.upcoming_score,
                "gemini_reason": niche.gemini_reason,
                "sources": list(source_data.keys()),
            })

        results.sort(key=lambda x: x["composite_score"], reverse=True)
        return results[:top_n]


# ── Main entrypoint ───────────────────────────────────────────────────────────

def run():
    """Fetch current + upcoming trends (every 2 weeks, 14d→112d) from Gemini."""
    logger.info("Starting Gemini trend discovery")

    today = datetime.now(timezone.utc)
    today_str = today.strftime("%Y-%m-%d")

    # Step 1 — Current trends
    logger.info("  Fetching current trends...")
    current = _call_gemini(_CURRENT_TRENDS_PROMPT)
    logger.info(f"  Gemini returned {len(current)} current trends")
    current_saved = save_current_trends(current)

    # Step 2 — Upcoming horizons: every 2 weeks from 2w to 4 months
    horizon_counts: dict[int, int] = {}
    for days in UPCOMING_HORIZONS:
        peak_date = (today + timedelta(days=days)).strftime("%Y-%m-%d")
        weeks = days // 7
        label = f"{weeks}w ({days}d)"
        logger.info(f"  Fetching upcoming trends — {label} horizon (peak ~{peak_date})...")
        prompt = _UPCOMING_PROMPT_TEMPLATE.format(
            today=today_str,
            peak_date=peak_date,
            horizon_days=days,
        )
        try:
            items = _call_gemini(prompt)
        except Exception as e:
            logger.warning(f"  Gemini parse error for {label} horizon, skipping: {e}")
            horizon_counts[days] = 0
            continue
        logger.info(f"  Gemini returned {len(items)} trends ({label})")
        horizon_counts[days] = save_upcoming_trends(items)

    upcoming_saved = sum(horizon_counts.values())
    breakdown = ", ".join(f"{c} × {d}d" for d, c in horizon_counts.items())

    # Step 3 — Log composite rankings
    rankings = get_trend_rankings(top_n=10)
    logger.info("  Top 10 composite-ranked niches:")
    for i, r in enumerate(rankings, 1):
        upcoming_flag = f" ↑→{r['upcoming_score']:.0f}" if r.get("upcoming_score") else ""
        logger.info(
            f"    {i:>2}. [{r['composite_score']:>5.1f}{upcoming_flag}] "
            f"{r['keyword']} (sources: {', '.join(r['sources'])})"
        )

    summary = f"{current_saved} current + {upcoming_saved} upcoming snapshots saved ({breakdown})"
    logger.info(f"Gemini trend scrape complete: {summary}")
    return summary
