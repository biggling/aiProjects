"""Job 8: Listing Refresh & Optimization
Schedule: Weekly Wednesday at 09:00 UTC
"""
from datetime import datetime, timedelta
from database.models import SessionLocal, Listing, Order, Competitor, OptimizationLog
from utils.ai_utils import generate_listing_seo
from utils.platform_api import EtsyClient
from config import (
    LISTING_REFRESH_DAYS_NO_SALES, LISTING_PAUSE_DAYS_NO_SALES, get_logger
)

logger = get_logger("job8_listing_refresh")


def get_listing_sales_count(session, listing_id: int) -> int:
    return session.query(Order).filter_by(listing_id=listing_id).count()


def get_competitor_keyword_gaps(session, niche: str) -> list[str]:
    """Find tags from competitor data not in our listing."""
    competitors = session.query(Competitor).filter_by(niche=niche, platform="etsy").all()
    competitor_tags: set = set()
    for c in competitors:
        tags = [t.strip().lower() for t in (c.tags or "").split(",") if t.strip()]
        competitor_tags.update(tags)
    return sorted(competitor_tags)[:10]


def refresh_listing_tags(session, listing: Listing, new_tags: str) -> bool:
    """Update listing tags via Etsy API and log the change."""
    try:
        if listing.external_id and listing.platform == "etsy":
            client = EtsyClient()
            client.update_listing(listing.external_id, {"tags": new_tags.split(",")[:13]})

        log = OptimizationLog(
            listing_id=listing.id,
            change_type="tags",
            old_value=listing.tags,
            new_value=new_tags,
            optimized_at=datetime.utcnow(),
        )
        session.add(log)
        listing.tags = new_tags
        listing.last_optimized_at = datetime.utcnow()
        listing.status = "optimized"
        return True
    except Exception as e:
        logger.error(f"Tag refresh failed for listing {listing.id}: {e}")
        return False


def pause_listing(session, listing: Listing) -> bool:
    """Pause listing on platform and mark in DB."""
    try:
        if listing.external_id and listing.platform == "etsy":
            client = EtsyClient()
            client.update_listing(listing.external_id, {"state": "inactive"})

        log = OptimizationLog(
            listing_id=listing.id,
            change_type="paused",
            old_value="active",
            new_value="paused",
            optimized_at=datetime.utcnow(),
        )
        session.add(log)
        listing.status = "paused"
        return True
    except Exception as e:
        logger.error(f"Pause failed for listing {listing.id}: {e}")
        return False


def run():
    logger.info("=== Job 8: Listing Refresh started ===")

    session = SessionLocal()
    refreshed = 0
    paused = 0

    try:
        refresh_cutoff = datetime.utcnow() - timedelta(days=LISTING_REFRESH_DAYS_NO_SALES)
        pause_cutoff = datetime.utcnow() - timedelta(days=LISTING_PAUSE_DAYS_NO_SALES)

        active_listings = session.query(Listing).filter_by(status="active").all()
        logger.info(f"Checking {len(active_listings)} active listings.")

        for listing in active_listings:
            sales = get_listing_sales_count(session, listing.id)
            if sales > 0:
                continue  # Has sales — leave it alone

            age_days = (datetime.utcnow() - (listing.published_at or datetime.utcnow())).days

            niche = ""
            if listing.design and listing.design.niche:
                niche = listing.design.niche.niche

            if age_days >= LISTING_PAUSE_DAYS_NO_SALES:
                # Pause after 60 days with no sales
                if pause_listing(session, listing):
                    paused += 1
                    logger.info(f"Paused listing {listing.id} ({age_days}d, 0 sales)")

            elif age_days >= LISTING_REFRESH_DAYS_NO_SALES:
                # Refresh after 30 days with no sales
                try:
                    seo = generate_listing_seo(niche or "general", listing.design.style if listing.design else "typography")
                    new_tags = seo.get("tags", "")
                    # Incorporate competitor keyword gaps
                    gaps = get_competitor_keyword_gaps(session, niche)
                    if gaps:
                        existing_tags = [t.strip() for t in new_tags.split(",")]
                        for gap in gaps:
                            if gap not in existing_tags and len(existing_tags) < 13:
                                existing_tags.append(gap)
                        new_tags = ",".join(existing_tags[:13])

                    if refresh_listing_tags(session, listing, new_tags):
                        refreshed += 1
                        logger.info(f"Refreshed listing {listing.id} ({age_days}d, 0 sales)")
                except Exception as e:
                    logger.error(f"Refresh SEO failed for listing {listing.id}: {e}")

        session.commit()
        logger.info(f"=== Job 8 complete — refreshed: {refreshed}, paused: {paused} ===")

    except Exception as e:
        session.rollback()
        logger.error(f"Job 8 failed: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    run()
