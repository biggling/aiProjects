"""Job 5: Order & Fulfillment Monitor
Schedule: Every 2 hours
"""
from datetime import datetime, timedelta
from database.models import SessionLocal, Listing, Order
from utils.platform_api import EtsyClient
from utils.notify import slack, alert_order, alert_fulfillment_stuck
from config import get_logger

logger = get_logger("job5_order_monitor")

STUCK_FULFILLMENT_HOURS = 48


def sync_etsy_orders(session) -> int:
    """Poll Etsy API for new orders and sync to DB."""
    client = EtsyClient()
    synced = 0
    try:
        receipts = client.get_receipts(limit=50)
        for receipt in receipts:
            receipt_id = str(receipt.get("receipt_id", ""))
            existing = session.query(Order).filter_by(
                platform="etsy", listing_id=None
            ).first()  # simplified lookup
            if existing:
                continue

            # Map receipt to our listing
            for transaction in receipt.get("transactions", []):
                listing_title = transaction.get("title", "")
                listing = session.query(Listing).filter(
                    Listing.title.ilike(f"%{listing_title[:30]}%"),
                    Listing.platform == "etsy"
                ).first()

                revenue = float(receipt.get("grandtotal", {}).get("amount", 0)) / 100
                platform_fee = revenue * 0.065  # Etsy ~6.5% transaction fee
                print_cost = 12.50  # approximate Printify base cost

                order = Order(
                    listing_id=listing.id if listing else None,
                    platform="etsy",
                    qty=transaction.get("quantity", 1),
                    revenue=revenue,
                    platform_fee=platform_fee,
                    print_cost=print_cost,
                    profit=revenue - platform_fee - print_cost,
                    fulfillment_status=receipt.get("status", "pending"),
                    order_date=datetime.utcnow(),
                )
                session.add(order)
                synced += 1

                if revenue > 0:
                    alert_order("Etsy", listing_title, revenue)

    except Exception as e:
        logger.error(f"Etsy order sync failed: {e}")
    return synced


def check_stuck_fulfillments(session) -> int:
    """Alert on orders stuck in pending/processing > 48h."""
    cutoff = datetime.utcnow() - timedelta(hours=STUCK_FULFILLMENT_HOURS)
    stuck = session.query(Order).filter(
        Order.fulfillment_status.in_(["pending", "processing"]),
        Order.order_date < cutoff,
    ).all()

    for order in stuck:
        hours = int((datetime.utcnow() - order.order_date).total_seconds() / 3600)
        alert_fulfillment_stuck(order.id, hours)
        logger.warning(f"Order {order.id} stuck for {hours}h")

    return len(stuck)


def run():
    logger.info("=== Job 5: Order Monitor started ===")

    session = SessionLocal()
    try:
        synced = sync_etsy_orders(session)
        stuck_count = check_stuck_fulfillments(session)
        session.commit()
        logger.info(f"Synced {synced} orders. Stuck: {stuck_count}.")
        logger.info("=== Job 5 complete ===")
    except Exception as e:
        session.rollback()
        logger.error(f"Job 5 failed: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    run()
