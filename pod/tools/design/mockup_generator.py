import os

import requests
from sqlalchemy import select

from tools.shared.config import PRINTIFY_API_KEY, PRINTIFY_SHOP_ID
from tools.shared.db import get_session
from tools.shared.models import Design
from tools.shared.logger import get_logger

logger = get_logger("mockup_generator")

MOCKUP_DIR = os.path.join("data", "designs", "mockups")
PRINTIFY_BASE = "https://api.printify.com"
# T-shirt blueprint and print provider defaults
BLUEPRINT_ID = 5        # Unisex Gildan t-shirt
PRINT_PROVIDER_ID = 29  # Monster Digital


def create_printify_mockup(design_id: int, processed_path: str) -> str | None:
    """Upload design to Printify and download mockup image."""
    headers = {"Authorization": f"Bearer {PRINTIFY_API_KEY}"}

    # Step 1: Upload image to Printify
    with open(processed_path, "rb") as f:
        upload_resp = requests.post(
            f"{PRINTIFY_BASE}/v1/uploads/images.json",
            headers=headers,
            files={"file": (f"design_{design_id}.png", f, "image/png")},
            timeout=60,
        )

    if upload_resp.status_code != 200:
        logger.error(f"Upload failed: {upload_resp.status_code} {upload_resp.text[:200]}")
        return None

    image_id = upload_resp.json().get("id")

    # Step 2: Create product to get mockup
    product_data = {
        "title": f"Design {design_id} Preview",
        "blueprint_id": BLUEPRINT_ID,
        "print_provider_id": PRINT_PROVIDER_ID,
        "variants": [{"id": 1, "price": 0, "is_enabled": False}],
        "print_areas": [{
            "variant_ids": [1],
            "placeholders": [{
                "position": "front",
                "images": [{"id": image_id, "x": 0.5, "y": 0.5, "scale": 1}],
            }],
        }],
    }

    product_resp = requests.post(
        f"{PRINTIFY_BASE}/v1/shops/{PRINTIFY_SHOP_ID}/products.json",
        headers={**headers, "Content-Type": "application/json"},
        json=product_data,
        timeout=60,
    )

    if product_resp.status_code not in (200, 201):
        logger.error(f"Product create failed: {product_resp.status_code}")
        return None

    # Extract mockup image URL from response
    product = product_resp.json()
    images = product.get("images", [])
    if not images:
        logger.warning("No mockup images in product response")
        return None

    mockup_url = images[0].get("src")
    if not mockup_url:
        return None

    # Step 3: Download mockup
    os.makedirs(MOCKUP_DIR, exist_ok=True)
    mockup_path = os.path.join(MOCKUP_DIR, f"{design_id}.png")

    img_resp = requests.get(mockup_url, timeout=30)
    if img_resp.status_code == 200:
        with open(mockup_path, "wb") as f:
            f.write(img_resp.content)
        return mockup_path

    return None


def run():
    """Generate mockups for all approved designs missing mockups."""
    logger.info("Starting mockup generation")

    with get_session() as session:
        designs = session.execute(
            select(Design).where(
                Design.status == "approved",
                Design.mockup_path.is_(None),
                Design.processed_path.isnot(None),
            )
        ).scalars().all()
        design_data = [(d.id, d.processed_path) for d in designs]

    if not design_data:
        logger.info("No designs need mockups")
        return "0 mockups generated"

    generated = 0
    for design_id, processed_path in design_data:
        try:
            mockup_path = create_printify_mockup(design_id, processed_path)
            if mockup_path:
                with get_session() as session:
                    design = session.get(Design, design_id)
                    design.mockup_path = mockup_path
                    design.status = "mockup_ready"
                generated += 1
                logger.info(f"  Mockup generated for design {design_id}")
            else:
                logger.warning(f"  No mockup for design {design_id}")
        except Exception as e:
            logger.error(f"  Mockup failed for design {design_id}: {e}")

    logger.info(f"Mockup generation complete: {generated}/{len(design_data)}")
    return f"{generated} mockups generated"
