"""Job 7: Competitor & Market Intelligence
Schedule: Weekly Sunday at 07:00 UTC
"""
import time
import random
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from database.models import SessionLocal, Niche, Competitor
from utils.platform_api import EtsyClient
from config import ETSY_ACCESS_TOKEN, get_logger

logger = get_logger("job7_competitor_intel")

OPPORTUNITY_REVIEW_THRESHOLD = 100


def scrape_etsy_top_listings(keyword: str, limit: int = 20) -> list[dict]:
    """Get top Etsy listings for keyword via API."""
    results = []
    if not ETSY_ACCESS_TOKEN:
        logger.info("Etsy token not configured, skipping API scrape.")
        return results
    try:
        client = EtsyClient()
        listings = client.search_listings(keyword, limit=limit)
        for item in listings:
            results.append({
                "title": item.get("title", ""),
                "price": item.get("price", {}).get("amount", 0) / 100,
                "reviews": item.get("num_favorers", 0),
                "tags": ",".join(item.get("tags", [])),
                "url": f"https://www.etsy.com/listing/{item.get('listing_id', '')}",
            })
    except Exception as e:
        logger.warning(f"Etsy competitor fetch failed for '{keyword}': {e}")
    return results


def find_keyword_gaps(our_tags: set, competitor_results: list[dict]) -> list[str]:
    """Find tags competitors use that we don't."""
    competitor_tags: set = set()
    for c in competitor_results:
        tags = [t.strip().lower() for t in c.get("tags", "").split(",") if t.strip()]
        competitor_tags.update(tags)
    gaps = sorted(competitor_tags - our_tags)
    return gaps[:10]


def run():
    logger.info("=== Job 7: Competitor Intel started ===")

    session = SessionLocal()
    try:
        niches = session.query(Niche).filter_by(status="active").all()
        logger.info(f"Analyzing {len(niches)} niches for competitor data.")

        opportunities = []

        for niche_row in niches:
            niche = niche_row.niche
            competitors = scrape_etsy_top_listings(niche, limit=20)

            for comp in competitors:
                record = Competitor(
                    niche=niche,
                    platform="etsy",
                    title=comp["title"],
                    price=comp["price"],
                    reviews=comp["reviews"],
                    tags=comp["tags"],
                    url=comp["url"],
                    scraped_at=datetime.utcnow(),
                )
                session.add(record)

            # Flag opportunity: top competitor has < threshold reviews
            top_reviews = [c["reviews"] for c in competitors if c["reviews"] > 0]
            if top_reviews and max(top_reviews) < OPPORTUNITY_REVIEW_THRESHOLD:
                opportunities.append(niche)
                logger.info(f"Opportunity niche: {niche} (max reviews: {max(top_reviews)})")

            time.sleep(random.uniform(1, 3))

        session.commit()
        logger.info(f"Competitor data saved. Opportunities found: {len(opportunities)}")
        logger.info(f"=== Job 7 complete ===")
        return opportunities

    except Exception as e:
        session.rollback()
        logger.error(f"Job 7 failed: {e}")
        return []
    finally:
        session.close()


if __name__ == "__main__":
    run()
