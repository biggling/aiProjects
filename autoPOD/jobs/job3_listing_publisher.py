"""Job 3: Listing Publisher
Schedule: Daily at 10:00 UTC
"""
import base64
import time
from datetime import datetime
from pathlib import Path
from database.models import SessionLocal, Design, Listing, Niche
from utils.ai_utils import generate_listing_seo
from utils.platform_api import PrintifyClient, EtsyClient
from config import (
    MAX_LISTINGS_PER_DAY, ETSY_PRICE_MULTIPLIER, ETSY_SHIPPING,
    AMAZON_PRICE_MULTIPLIER, get_logger,
)

logger = get_logger("job3_listing_publisher")

PRINTIFY_TSHIRT_BLUEPRINT_ID = 5      # Unisex Staple T-Shirt (Bella+Canvas 3001)
PRINTIFY_PRINT_PROVIDER_ID = 99       # US provider (check Printify docs for your region)
ETSY_BASE_COST = 12.50                # approximate Printify base cost for t-shirt


def encode_image_b64(file_path: str) -> str:
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def publish_to_etsy_via_printify(
    design: Design, niche: str, seo: dict
) -> dict | None:
    printify = PrintifyClient()
    etsy = EtsyClient()

    try:
        # 1. Upload design image to Printify
        img_b64 = encode_image_b64(design.file_path)
        filename = Path(design.file_path).name
        upload_resp = printify.upload_image(filename, img_b64)
        image_id = upload_resp["id"]
        logger.info(f"Printify image uploaded: {image_id}")

        # 2. Create product in Printify
        price_cents = int((ETSY_BASE_COST * ETSY_PRICE_MULTIPLIER + ETSY_SHIPPING) * 100)
        product_data = {
            "title": seo["title"],
            "description": seo["description"],
            "blueprint_id": PRINTIFY_TSHIRT_BLUEPRINT_ID,
            "print_provider_id": PRINTIFY_PRINT_PROVIDER_ID,
            "variants": [
                {"id": 17390, "price": price_cents, "is_enabled": True},  # S
                {"id": 17391, "price": price_cents, "is_enabled": True},  # M
                {"id": 17392, "price": price_cents, "is_enabled": True},  # L
                {"id": 17393, "price": price_cents, "is_enabled": True},  # XL
            ],
            "print_areas": [
                {
                    "variant_ids": [17390, 17391, 17392, 17393],
                    "placeholders": [
                        {"position": "front", "images": [{"id": image_id, "x": 0.5, "y": 0.5, "scale": 1, "angle": 0}]}
                    ],
                }
            ],
        }
        product = printify.create_product(product_data)
        product_id = product["id"]
        logger.info(f"Printify product created: {product_id}")

        # 3. Publish to Etsy
        publish_data = {
            "title": True,
            "description": True,
            "images": True,
            "variants": True,
            "tags": True,
            "keyFeatures": True,
            "shipping_template": True,
        }
        printify.publish_product(product_id, publish_data)
        logger.info(f"Published to Etsy via Printify: {product_id}")

        return {"printify_id": product_id, "platform": "etsy"}

    except Exception as e:
        logger.error(f"Etsy/Printify publish failed for design {design.id}: {e}")
        return None


def run():
    logger.info("=== Job 3: Listing Publisher started ===")

    session = SessionLocal()
    published_count = 0

    try:
        ready_designs = session.query(Design).filter_by(status="ready").limit(MAX_LISTINGS_PER_DAY).all()
        logger.info(f"Found {len(ready_designs)} ready designs to publish.")

        for design in ready_designs:
            if published_count >= MAX_LISTINGS_PER_DAY:
                break

            niche_row = session.query(Niche).filter_by(id=design.niche_id).first()
            niche = niche_row.niche if niche_row else "general"

            # Generate SEO content
            try:
                seo = generate_listing_seo(niche, design.style, platform="etsy")
            except Exception as e:
                logger.error(f"SEO generation failed for design {design.id}: {e}")
                continue

            price = round(ETSY_BASE_COST * ETSY_PRICE_MULTIPLIER + ETSY_SHIPPING, 2)

            # Publish to Etsy via Printify
            result = publish_to_etsy_via_printify(design, niche, seo)

            if result:
                listing = Listing(
                    design_id=design.id,
                    platform="etsy",
                    external_id=result.get("printify_id"),
                    title=seo.get("title", ""),
                    description=seo.get("description", ""),
                    tags=seo.get("tags", ""),
                    price=price,
                    status="active",
                    published_at=datetime.utcnow(),
                )
                session.add(listing)
                design.status = "published"
                published_count += 1
                logger.info(f"Listing created for design {design.id} — {niche}")
                time.sleep(5)  # avoid platform rate limits

        session.commit()
        logger.info(f"=== Job 3 complete — {published_count} listings published ===")

    except Exception as e:
        session.rollback()
        logger.error(f"Job 3 failed: {e}")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    run()
