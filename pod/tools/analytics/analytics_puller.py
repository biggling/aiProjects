import requests
from sqlalchemy import select

from tools.shared.config import ETSY_API_KEY
from tools.shared.db import get_session
from tools.shared.models import Listing
from tools.shared.logger import get_logger

logger = get_logger("analytics_puller")

ETSY_BASE = "https://openapi.etsy.com/v3"


def fetch_listing_stats(etsy_listing_id: str) -> dict | None:
    """Fetch stats for a single Etsy listing."""
    headers = {"x-api-key": ETSY_API_KEY}

    try:
        resp = requests.get(
            f"{ETSY_BASE}/application/listings/{etsy_listing_id}",
            headers=headers, timeout=15,
        )
        if resp.status_code == 200:
            data = resp.json()
            return {
                "views": data.get("views", 0),
                "num_favorers": data.get("num_favorers", 0),
            }
    except Exception as e:
        logger.error(f"Failed to fetch stats for {etsy_listing_id}: {e}")

    return None


def run():
    """Pull analytics for all live Etsy listings."""
    logger.info("Starting analytics pull")

    with get_session() as session:
        listings = session.execute(
            select(Listing).where(Listing.etsy_listing_id.isnot(None))
        ).scalars().all()
        listing_data = [(l.id, l.etsy_listing_id) for l in listings]

    if not listing_data:
        logger.info("No listings to pull analytics for")
        return "0 listings updated"

    total_views = 0
    total_revenue = 0.0
    updated = 0

    for listing_id, etsy_id in listing_data:
        stats = fetch_listing_stats(etsy_id)
        if stats:
            with get_session() as session:
                listing = session.get(Listing, listing_id)
                listing.views = stats["views"]
                listing.favorites = stats["num_favorers"]
            total_views += stats["views"]
            updated += 1

    with get_session() as session:
        total_revenue = sum(
            l.revenue or 0 for l in session.execute(
                select(Listing).where(Listing.etsy_listing_id.isnot(None))
            ).scalars().all()
        )

    logger.info(f"Analytics pull complete: {updated} listings, {total_views} total views, ${total_revenue:.2f} revenue")
    return f"{updated} listings updated"
