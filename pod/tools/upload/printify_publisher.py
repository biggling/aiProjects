import os

import requests
from sqlalchemy import select

from tools.shared.config import PRINTIFY_API_KEY, PRINTIFY_SHOP_ID
from tools.shared.db import get_session
from tools.shared.models import Listing, Design
from tools.shared.logger import get_logger

logger = get_logger("printify_publisher")

PRINTIFY_BASE = "https://api.printify.com"
BLUEPRINT_ID = 5        # Unisex Gildan t-shirt
PRINT_PROVIDER_ID = 29  # Monster Digital


def upload_image(image_path: str) -> str | None:
    """Upload an image to Printify, return image ID."""
    headers = {"Authorization": f"Bearer {PRINTIFY_API_KEY}"}
    with open(image_path, "rb") as f:
        resp = requests.post(
            f"{PRINTIFY_BASE}/v1/uploads/images.json",
            headers=headers,
            files={"file": (os.path.basename(image_path), f, "image/png")},
            timeout=60,
        )
    if resp.status_code == 200:
        return resp.json().get("id")
    logger.error(f"Image upload failed: {resp.status_code}")
    return None


def create_product(title: str, description: str, image_id: str) -> str | None:
    """Create a Printify product and return product ID."""
    headers = {
        "Authorization": f"Bearer {PRINTIFY_API_KEY}",
        "Content-Type": "application/json",
    }

    product_data = {
        "title": title,
        "description": description,
        "blueprint_id": BLUEPRINT_ID,
        "print_provider_id": PRINT_PROVIDER_ID,
        "variants": [{"id": 1, "price": 2499, "is_enabled": True}],
        "print_areas": [{
            "variant_ids": [1],
            "placeholders": [{
                "position": "front",
                "images": [{"id": image_id, "x": 0.5, "y": 0.5, "scale": 1}],
            }],
        }],
    }

    resp = requests.post(
        f"{PRINTIFY_BASE}/v1/shops/{PRINTIFY_SHOP_ID}/products.json",
        headers=headers, json=product_data, timeout=60,
    )

    if resp.status_code in (200, 201):
        return resp.json().get("id")
    logger.error(f"Product create failed: {resp.status_code} {resp.text[:200]}")
    return None


def publish_product(product_id: str) -> bool:
    """Publish a product on Printify."""
    headers = {
        "Authorization": f"Bearer {PRINTIFY_API_KEY}",
        "Content-Type": "application/json",
    }

    resp = requests.post(
        f"{PRINTIFY_BASE}/v1/shops/{PRINTIFY_SHOP_ID}/products/{product_id}/publish.json",
        headers=headers,
        json={"title": True, "description": True, "images": True, "variants": True, "tags": True},
        timeout=30,
    )

    return resp.status_code == 200


def run():
    """Publish listings to Printify that don't have a product ID yet."""
    logger.info("Starting Printify publishing")

    with get_session() as session:
        listings = session.execute(
            select(Listing).where(
                Listing.printify_product_id.is_(None),
                Listing.status == "copy_ready",
            )
        ).scalars().all()
        listing_data = [(l.id, l.title, l.description, l.design_id) for l in listings]

    if not listing_data:
        logger.info("No listings to publish")
        return "0 products published"

    published = 0
    for listing_id, title, description, design_id in listing_data:
        try:
            # Get design's processed image path
            with get_session() as session:
                design = session.get(Design, design_id)
                image_path = design.processed_path if design else None

            if not image_path or not os.path.exists(image_path):
                logger.warning(f"  No image for listing {listing_id}")
                continue

            image_id = upload_image(image_path)
            if not image_id:
                continue

            product_id = create_product(title, description, image_id)
            if not product_id:
                continue

            publish_product(product_id)

            with get_session() as session:
                listing = session.get(Listing, listing_id)
                listing.printify_product_id = product_id

            published += 1
            logger.info(f"  Published listing {listing_id} → product {product_id}")

        except Exception as e:
            logger.error(f"  Failed listing {listing_id}: {e}")

    logger.info(f"Printify publishing complete: {published}")
    return f"{published} products published"
