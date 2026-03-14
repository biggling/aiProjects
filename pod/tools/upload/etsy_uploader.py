import time
from datetime import datetime, timezone

import requests
from sqlalchemy import select

from tools.shared.config import ETSY_API_KEY, ETSY_SHOP_ID
from tools.shared.db import get_session
from tools.shared.models import Listing, Design
from tools.shared.logger import get_logger

logger = get_logger("etsy_uploader")

ETSY_BASE = "https://openapi.etsy.com/v3"
MAX_RETRIES = 3
RATE_LIMIT_SLEEP = 60


def create_etsy_listing(title: str, description: str, tags: list[str],
                        mockup_path: str | None) -> str | None:
    """Create an Etsy listing via v3 API."""
    headers = {
        "x-api-key": ETSY_API_KEY,
        "Content-Type": "application/json",
    }

    listing_data = {
        "title": title[:140],
        "description": description,
        "tags": tags[:13],
        "price": {"amount": 2499, "divisor": 100, "currency_code": "USD"},
        "quantity": 999,
        "who_made": "i_did",
        "when_made": "made_to_order",
        "taxonomy_id": 482,  # Clothing > Shirts & Tees
        "state": "active",
        "type": "physical",
        "shipping_profile_id": 1,
    }

    for attempt in range(MAX_RETRIES):
        try:
            resp = requests.post(
                f"{ETSY_BASE}/application/shops/{ETSY_SHOP_ID}/listings",
                headers=headers, json=listing_data, timeout=30,
            )

            if resp.status_code in (200, 201):
                return str(resp.json().get("listing_id"))
            elif resp.status_code == 429:
                logger.warning(f"Rate limited, waiting {RATE_LIMIT_SLEEP}s")
                time.sleep(RATE_LIMIT_SLEEP)
            else:
                logger.error(f"Etsy API error {resp.status_code}: {resp.text[:200]}")
                return None

        except Exception as e:
            logger.error(f"Request failed (attempt {attempt + 1}): {e}")
            time.sleep(5)

    return None


def run():
    """Upload listings to Etsy that have Printify products but no Etsy listing."""
    logger.info("Starting Etsy upload")

    with get_session() as session:
        listings = session.execute(
            select(Listing).where(
                Listing.etsy_listing_id.is_(None),
                Listing.printify_product_id.isnot(None),
            )
        ).scalars().all()
        listing_data = [(l.id, l.title, l.description, l.tags, l.design_id) for l in listings]

    if not listing_data:
        logger.info("No listings to upload")
        return "0 listings uploaded"

    uploaded = 0
    for listing_id, title, description, tags, design_id in listing_data:
        try:
            # Get mockup path
            with get_session() as session:
                design = session.get(Design, design_id)
                mockup_path = design.mockup_path if design else None

            etsy_id = create_etsy_listing(title, description, tags or [], mockup_path)

            if etsy_id:
                with get_session() as session:
                    listing = session.get(Listing, listing_id)
                    listing.etsy_listing_id = etsy_id
                    listing.status = "live"
                    listing.uploaded_at = datetime.now(timezone.utc)
                uploaded += 1
                logger.info(f"  Uploaded listing {listing_id} → Etsy {etsy_id}")
            else:
                logger.warning(f"  Failed to upload listing {listing_id}")

        except Exception as e:
            logger.error(f"  Error uploading listing {listing_id}: {e}")

    logger.info(f"Etsy upload complete: {uploaded}")
    return f"{uploaded} listings uploaded"
