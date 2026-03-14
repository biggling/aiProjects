import time
from pytrends.request import TrendReq
from sqlalchemy import select

from tools.shared.config import SEED_KEYWORDS
from tools.shared.db import get_session
from tools.shared.models import Niche
from tools.shared.logger import get_logger

logger = get_logger("trend_scraper")

MAX_RETRIES = 3
RETRY_SLEEP = 60


def fetch_trends(keywords: list[str], timeframe: str = "today 3-m") -> dict:
    """Fetch Google Trends data for a batch of keywords (max 5 at a time)."""
    pytrends = TrendReq(hl="en-US", tz=360)
    results = {}

    for i in range(0, len(keywords), 5):
        batch = keywords[i:i + 5]
        for attempt in range(MAX_RETRIES):
            try:
                pytrends.build_payload(batch, timeframe=timeframe)

                # Interest over time
                iot = pytrends.interest_over_time()
                if not iot.empty:
                    for kw in batch:
                        if kw in iot.columns:
                            values = iot[kw].values
                            avg_score = float(values.mean())
                            if len(values) >= 2:
                                recent = float(values[-4:].mean())
                                older = float(values[:4].mean())
                                velocity = (recent - older) / max(older, 1.0)
                            else:
                                velocity = 0.0
                            results[kw] = {
                                "trend_score": avg_score,
                                "velocity": velocity,
                            }

                # Related / rising queries
                related = pytrends.related_queries()
                for kw in batch:
                    if kw in related and related[kw]["rising"] is not None:
                        rising = related[kw]["rising"]
                        for _, row in rising.head(5).iterrows():
                            rq = row["query"].lower().strip()
                            if rq not in results:
                                results[rq] = {
                                    "trend_score": float(row.get("value", 50)),
                                    "velocity": 1.0,
                                }
                break  # success
            except Exception as e:
                logger.warning(f"Attempt {attempt + 1} failed for {batch}: {e}")
                if attempt < MAX_RETRIES - 1:
                    time.sleep(RETRY_SLEEP)
                else:
                    logger.error(f"All retries exhausted for {batch}")

        time.sleep(2)  # rate limit between batches

    return results


def upsert_niches(trends: dict):
    """Upsert trend data into the niches table."""
    updated = 0
    with get_session() as session:
        for keyword, data in trends.items():
            niche = session.execute(
                select(Niche).where(Niche.keyword == keyword)
            ).scalar_one_or_none()

            if niche:
                niche.trend_score = data["trend_score"]
                niche.velocity = data["velocity"]
            else:
                niche = Niche(
                    keyword=keyword,
                    trend_score=data["trend_score"],
                    velocity=data["velocity"],
                    status="active",
                )
                session.add(niche)
            updated += 1

    return updated


def run():
    """Main entry point for trend scraping."""
    logger.info(f"Starting trend scrape with {len(SEED_KEYWORDS)} seed keywords")

    trends = fetch_trends(SEED_KEYWORDS)
    count = upsert_niches(trends)

    # Log top 5
    with get_session() as session:
        top = session.execute(
            select(Niche).order_by(Niche.trend_score.desc()).limit(5)
        ).scalars().all()
        for n in top:
            logger.info(f"  Top niche: {n.keyword} (score={n.trend_score:.1f}, vel={n.velocity:.2f})")

    logger.info(f"Trend scrape complete: {count} niches updated")
    return f"{count} niches updated"
