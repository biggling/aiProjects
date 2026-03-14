import requests
from fastapi import APIRouter, Request

from tools.shared.config import PRINTIFY_API_KEY, PRINTIFY_SHOP_ID
from tools.shared.db import get_session
from tools.shared.models import Listing
from tools.shared.logger import get_logger

logger = get_logger("order_router")

router = APIRouter()

PRINTIFY_BASE = "https://api.printify.com"


@router.post("/webhook/etsy-order")
async def handle_etsy_order(request: Request):
    """Handle incoming Etsy order webhook and route to Printify."""
    payload = await request.json()
    logger.info(f"Received Etsy order webhook: {payload.get('receipt_id', 'unknown')}")

    transactions = payload.get("transactions", [])
    orders_created = 0

    for txn in transactions:
        listing_id = str(txn.get("listing_id", ""))

        with get_session() as session:
            listing = session.query(Listing).filter_by(
                etsy_listing_id=listing_id
            ).first()

            if not listing or not listing.printify_product_id:
                logger.warning(f"No Printify product for Etsy listing {listing_id}")
                continue

            printify_product_id = listing.printify_product_id

        # Create Printify order
        headers = {
            "Authorization": f"Bearer {PRINTIFY_API_KEY}",
            "Content-Type": "application/json",
        }

        order_data = {
            "external_id": str(payload.get("receipt_id", "")),
            "line_items": [{
                "product_id": printify_product_id,
                "variant_id": 1,
                "quantity": txn.get("quantity", 1),
            }],
            "shipping_method": 1,
            "address_to": {
                "first_name": payload.get("first_name", ""),
                "last_name": payload.get("last_name", ""),
                "address1": payload.get("address", {}).get("first_line", ""),
                "city": payload.get("address", {}).get("city", ""),
                "region": payload.get("address", {}).get("state", ""),
                "zip": payload.get("address", {}).get("zip", ""),
                "country": payload.get("address", {}).get("country_iso", "US"),
            },
        }

        try:
            resp = requests.post(
                f"{PRINTIFY_BASE}/v1/shops/{PRINTIFY_SHOP_ID}/orders.json",
                headers=headers, json=order_data, timeout=30,
            )

            if resp.status_code in (200, 201):
                order_id = resp.json().get("id")
                logger.info(f"Printify order created: {order_id}")
                orders_created += 1
            else:
                logger.error(f"Printify order failed: {resp.status_code} {resp.text[:200]}")

        except Exception as e:
            logger.error(f"Order routing failed: {e}")

    return {"status": "ok", "orders_created": orders_created}
