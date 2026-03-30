"""Blue ocean niche discovery — finds low-competition, high-demand micro-niches.

Strategy:
  1. Pull the current top trending keywords from DB (red ocean context).
  2. Ask Gemini to identify adjacent micro-niches that are under-served on Etsy
     but have real buying intent — the "blue ocean" angle.
  3. Score each: blue_ocean_score = demand_score × (1 − competition_level)
  4. Save as Niche + TrendSnapshot rows with source="blue_ocean".

Runs biweekly (1st and 15th of each month via Celery Beat).
"""
import json
import re
from datetime import datetime, timezone

from google import genai
from sqlalchemy import select, desc

from tools.shared.config import GEMINI_API_KEY
from tools.shared.db import get_session
from tools.shared.models import Niche, TrendSnapshot
from tools.shared.logger import get_logger

logger = get_logger("blue_ocean_scraper")

MODEL = "gemini-2.5-flash"
MAX_RED_OCEAN_CONTEXT = 30   # trending niches fed as context to Gemini
RESULTS_PER_BATCH = 40       # niches returned per Gemini call


# ── Prompts ───────────────────────────────────────────────────────────────────

_BLUE_OCEAN_PROMPT = """You are an expert Etsy print-on-demand market researcher
specialising in finding UNDERSERVED, LOW-COMPETITION micro-niches.

Today is {today}.

These keywords are currently TRENDING and SATURATED on Etsy (red ocean — avoid these directly):
{red_ocean_list}

Your task: identify {n} BLUE OCEAN micro-niches that:
1. Have REAL buying intent on Etsy (people will actually search and buy)
2. Are NOT yet saturated — fewer than ~500 competing Etsy listings expected
3. Derive from the trending categories above but target a SPECIFIC sub-audience
4. Work as POD products (t-shirts, hoodies, mugs, tote bags, stickers, sweatshirts)

Winning blue ocean patterns:
- Hyper-specific profession: "pediatric ICU nurse" not just "nurse"
- Micro-demographic: "girl dog mom of two" not just "dog mom"
- Hobby × identity: "book club wine night" not just "book lover"
- Underserved culture/region niche: specific cultural celebrations, languages
- New identity labels: emerging social labels that buyers self-identify with
- Niche sport sub-audience: "disc golf dad" not just "golf dad"
- Event micro-niche: "first Father's Day twins" not just "first Father's Day"
- Occupation × milestone: "nurse graduating 2026" not just "nurse"
- Aesthetic sub-niche: "dark academia book witch" not just "bookish"

Return ONLY a valid JSON array of {n} objects, no markdown:
[
  {{
    "keyword": "specific Etsy search phrase (2-6 words)",
    "parent_niche": "the red ocean niche this derives from",
    "demand_score": <float 0-100, how much buying intent exists>,
    "competition_level": <float 0.0-1.0, 0=no competition, 1=saturated>,
    "blue_ocean_score": <float 0-100, demand_score × (1 - competition_level)>,
    "target_customer": "age range, identity/role, occasion, price sensitivity (e.g. 'Women 25-40, new stepmoms, Mother's Day, $20-35')",
    "recommended_products": ["top 2-3 POD product types from: t-shirt, hoodie, sweatshirt, mug, tote, sticker, tumbler, hat, phone case, pillow"],
    "design_pattern": "visual style and theme (e.g. 'Retro varsity font, earth tones, wildflower border; or Minimalist line-art, black on white, single icon')",
    "reason": "one sentence: why this is underserved and why NOW"
  }}
]

Sort by blue_ocean_score descending. Only include niches with blue_ocean_score >= 40."""

_HORIZON_BLUE_OCEAN_PROMPT = """You are an expert Etsy POD researcher finding FUTURE blue ocean niches.

Today is {today}. Target window: niches that will peak around {peak_date} ({horizon_days} days from now).

These are known upcoming trends for that window (already competitive — avoid direct overlap):
{upcoming_list}

Identify {n} BLUE OCEAN micro-niches that will peak around {peak_date} but are NOT yet
on anyone's radar. Think: what specific sub-audience within those trends is being ignored?

Apply the same blue ocean patterns (hyper-specific profession, micro-demographic,
hobby × identity, emerging labels, niche sport, event micro-niche, aesthetic sub-niche).

Return ONLY a valid JSON array of {n} objects, no markdown:
[
  {{
    "keyword": "specific Etsy search phrase (2-6 words)",
    "parent_niche": "the upcoming trend this derives from",
    "demand_score": <float 0-100>,
    "competition_level": <float 0.0-1.0>,
    "blue_ocean_score": <float 0-100, demand × (1 - competition)>,
    "horizon_days": {horizon_days},
    "peak_date": "{peak_date}",
    "target_customer": "age range, identity/role, occasion, price sensitivity (e.g. 'Men 30-50, first-time dads, Father's Day, $25-45')",
    "recommended_products": ["top 2-3 POD product types from: t-shirt, hoodie, sweatshirt, mug, tote, sticker, tumbler, hat, phone case, pillow"],
    "design_pattern": "visual style and theme (e.g. 'Bold retro serif, navy + gold, sports crest motif; or Soft watercolor florals, sage green palette, handwritten font')",
    "reason": "one sentence: why this is underserved and why it peaks then"
  }}
]

Sort by blue_ocean_score descending. Only include niches with blue_ocean_score >= 40."""


# ── Helpers ───────────────────────────────────────────────────────────────────

def _call_gemini(prompt: str) -> list[dict]:
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
        # Truncate to the last complete object — find last "}," or final "}"
        last_obj = text.rfind("},")
        if last_obj == -1:
            last_obj = text.rfind("}")
        if last_obj != -1:
            truncated = text[: last_obj + 1].rstrip(",") + "\n]"
            return json.loads(truncated)
        raise


def _get_top_trending(session, limit: int) -> list[str]:
    """Return the top trending keyword strings from the DB."""
    niches = session.execute(
        select(Niche)
        .where(Niche.status == "active")
        .order_by(desc(Niche.trend_score))
        .limit(limit)
    ).scalars().all()
    return [n.keyword for n in niches if n.keyword]


def _get_upcoming_for_horizon(session, horizon_days: int, limit: int = 20) -> list[str]:
    """Return top upcoming keyword strings for a given horizon."""
    snaps = session.execute(
        select(TrendSnapshot)
        .where(
            TrendSnapshot.is_upcoming == True,
            TrendSnapshot.horizon_days == horizon_days,
        )
        .order_by(desc(TrendSnapshot.trend_score))
        .limit(limit)
    ).scalars().all()
    niche_ids = {s.niche_id for s in snaps}
    if not niche_ids:
        return []
    niches = session.execute(
        select(Niche).where(Niche.id.in_(niche_ids))
    ).scalars().all()
    kw_map = {n.id: n.keyword for n in niches}
    return [kw_map[s.niche_id] for s in snaps if s.niche_id in kw_map]


def _save_blue_ocean_results(items: list[dict], is_upcoming: bool = False) -> int:
    """Upsert Niche rows and write TrendSnapshot rows for blue ocean results."""
    now = datetime.now(timezone.utc)
    saved = 0

    with get_session() as session:
        for i, item in enumerate(items, 1):
            keyword = item.get("keyword", "").strip().lower()
            if not keyword:
                continue

            demand = float(item.get("demand_score", 50.0))
            competition = float(item.get("competition_level", 0.5))
            bo_score = float(item.get("blue_ocean_score", demand * (1 - competition)))

            # Upsert niche
            niche = session.execute(
                select(Niche).where(Niche.keyword == keyword)
            ).scalar_one_or_none()
            if not niche:
                niche = Niche(keyword=keyword, status="active")
                session.add(niche)

            niche.trend_score = niche.trend_score or demand
            niche.competition_level = competition
            niche.blue_ocean_score = bo_score
            niche.parent_niche = item.get("parent_niche")
            niche.gemini_reason = item.get("reason")
            niche.target_customer = item.get("target_customer")
            niche.recommended_products = item.get("recommended_products")
            niche.design_pattern = item.get("design_pattern")

            scores = niche.source_scores or {}
            scores["blue_ocean"] = bo_score
            niche.source_scores = scores

            session.flush()

            snapshot = TrendSnapshot(
                niche_id=niche.id,
                source="blue_ocean",
                trend_score=demand,
                velocity=0.5,           # assumed rising (blue ocean = early stage)
                rank_position=i,
                reason=(
                    f"[{item.get('target_audience', '')}] "
                    f"{item.get('reason', '')} "
                    f"| Product fit: {item.get('product_fit', '')}"
                ),
                is_upcoming=is_upcoming,
                horizon_days=item.get("horizon_days"),
                competition_level=competition,
                blue_ocean_score=bo_score,
                snapshot_date=now,
            )
            session.add(snapshot)
            saved += 1

    return saved


# ── Main entrypoint ───────────────────────────────────────────────────────────

# Horizons to run blue ocean research for (every 2 weeks, matching trend scraper)
BLUE_OCEAN_HORIZONS = [14, 28, 42, 56, 70, 84, 98, 112]


def run() -> str:
    """Discover blue ocean niches (current + per 2-week horizon) and persist to DB."""
    logger.info("Starting blue ocean niche discovery")

    today = datetime.now(timezone.utc)
    today_str = today.strftime("%Y-%m-%d")
    total_saved = 0

    with get_session() as session:
        red_ocean = _get_top_trending(session, MAX_RED_OCEAN_CONTEXT)

    if not red_ocean:
        logger.warning("No trending niches in DB — run gemini_trend_scraper first")
        return "0 niches saved (no trending context)"

    red_ocean_list = "\n".join(f"  - {kw}" for kw in red_ocean)

    # ── Step 1: Current blue ocean niches ─────────────────────────────────────
    logger.info(f"  Fetching current blue ocean niches (context: {len(red_ocean)} red ocean trends)...")
    prompt = _BLUE_OCEAN_PROMPT.format(
        today=today_str,
        red_ocean_list=red_ocean_list,
        n=RESULTS_PER_BATCH,
    )
    results = _call_gemini(prompt)
    results.sort(key=lambda x: x.get("blue_ocean_score", 0), reverse=True)
    saved_now = _save_blue_ocean_results(results, is_upcoming=False)
    total_saved += saved_now
    logger.info(f"  Saved {saved_now} current blue ocean niches")

    # Log top 10
    logger.info("  Top 10 current blue ocean niches:")
    for i, r in enumerate(results[:10], 1):
        products = ", ".join(r.get("recommended_products") or [])
        logger.info(
            f"    {i:>2}. [BO:{r.get('blue_ocean_score', 0):>4.0f} "
            f"D:{r.get('demand_score', 0):>3.0f} "
            f"C:{r.get('competition_level', 0):.2f}] "
            f"{r['keyword']}  ← {r.get('parent_niche', '')}"
        )
        logger.info(f"        👤 {r.get('target_customer', '')}")
        logger.info(f"        📦 {products}  |  🎨 {r.get('design_pattern', '')}")

    # ── Step 2: Future blue ocean per horizon ─────────────────────────────────
    horizon_counts: dict[int, int] = {}
    for days in BLUE_OCEAN_HORIZONS:
        from datetime import timedelta
        peak_date = (today + timedelta(days=days)).strftime("%Y-%m-%d")

        with get_session() as session:
            upcoming = _get_upcoming_for_horizon(session, days, limit=20)

        if not upcoming:
            logger.info(f"  Skipping {days}d horizon — no upcoming trends in DB yet")
            horizon_counts[days] = 0
            continue

        upcoming_list = "\n".join(f"  - {kw}" for kw in upcoming)
        logger.info(f"  Fetching blue ocean niches — {days}d horizon (peak ~{peak_date})...")
        prompt = _HORIZON_BLUE_OCEAN_PROMPT.format(
            today=today_str,
            peak_date=peak_date,
            horizon_days=days,
            upcoming_list=upcoming_list,
            n=RESULTS_PER_BATCH,
        )
        try:
            horizon_results = _call_gemini(prompt)
        except Exception as e:
            logger.warning(f"  Gemini parse error for {days}d horizon, skipping: {e}")
            horizon_counts[days] = 0
            continue
        horizon_results.sort(key=lambda x: x.get("blue_ocean_score", 0), reverse=True)
        count = _save_blue_ocean_results(horizon_results, is_upcoming=True)
        horizon_counts[days] = count
        total_saved += count
        logger.info(f"  Saved {count} blue ocean niches ({days}d horizon)")

    breakdown = ", ".join(f"{c} × {d}d" for d, c in horizon_counts.items() if c > 0)
    summary = f"{saved_now} current + {total_saved - saved_now} future blue ocean niches saved ({breakdown})"
    logger.info(f"Blue ocean discovery complete: {summary}")
    return summary
