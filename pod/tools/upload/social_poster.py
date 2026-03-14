import os
from datetime import datetime, timezone

import requests
from sqlalchemy import select

from tools.shared.config import BUFFER_ACCESS_TOKEN
from tools.shared.db import get_session
from tools.shared.models import Listing, Design
from tools.shared.logger import get_logger

logger = get_logger("social_poster")

BUFFER_BASE = "https://api.bufferapp.com/1"


def post_to_buffer(caption: str, image_path: str | None) -> bool:
    """Post to Buffer API."""
    headers = {"Authorization": f"Bearer {BUFFER_ACCESS_TOKEN}"}

    # Get profiles
    profiles_resp = requests.get(
        f"{BUFFER_BASE}/profiles.json", headers=headers, timeout=15,
    )
    if profiles_resp.status_code != 200:
        logger.error("Failed to get Buffer profiles")
        return False

    profiles = profiles_resp.json()
    if not profiles:
        logger.warning("No Buffer profiles configured")
        return False

    profile_ids = [p["id"] for p in profiles[:3]]  # Post to first 3 profiles

    post_data = {
        "text": caption,
        "profile_ids[]": profile_ids,
    }

    if image_path and os.path.exists(image_path):
        post_data["media[photo]"] = image_path

    resp = requests.post(
        f"{BUFFER_BASE}/updates/create.json",
        headers=headers, data=post_data, timeout=30,
    )

    return resp.status_code in (200, 201)


def run():
    """Post live listings to social media via Buffer."""
    logger.info("Starting social posting")

    with get_session() as session:
        listings = session.execute(
            select(Listing).where(
                Listing.status == "live",
                Listing.caption.isnot(None),
            ).limit(5)
        ).scalars().all()

        to_post = []
        for l in listings:
            # Check if already posted (uploaded_at would be set)
            # Using a simple check: if caption exists and status is live
            design = session.get(Design, l.design_id) if l.design_id else None
            mockup_path = design.mockup_path if design else None
            to_post.append((l.id, l.caption, mockup_path))

    if not to_post:
        logger.info("No listings to post")
        return "0 posts created"

    posted = 0
    for listing_id, caption, mockup_path in to_post:
        try:
            if post_to_buffer(caption, mockup_path):
                posted += 1
                logger.info(f"  Posted listing {listing_id}")
            else:
                logger.warning(f"  Failed to post listing {listing_id}")
        except Exception as e:
            logger.error(f"  Social post failed for listing {listing_id}: {e}")

    logger.info(f"Social posting complete: {posted}")
    return f"{posted} posts created"
