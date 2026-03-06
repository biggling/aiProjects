"""Job 7: Affiliate & Monetization Tracker
Schedule: Every 6 hours
"""
from datetime import datetime, date
from database.models import SessionLocal, Post, Niche, Affiliate
from utils.affiliate_api import get_affiliate_earnings
from utils.notify import alert_commission
from config import VIRAL_COMMISSION_THRESHOLD, REPLICATE_CONVERSION_RATE, get_logger

logger = get_logger("job7_affiliate_tracker")


def sync_affiliate_earnings(session) -> dict:
    today = date.today().isoformat()
    earnings = get_affiliate_earnings(today)

    for network, amount in earnings.items():
        if amount > 0:
            session.add(Affiliate(
                affiliate_network=network,
                commission=amount,
                period=today,
                recorded_at=datetime.utcnow(),
            ))
            if amount >= VIRAL_COMMISSION_THRESHOLD:
                alert_commission(amount, "multiple products", network)

    return earnings


def flag_high_performers(session) -> list:
    """Find products with high conversion rates → flag for more content."""
    from sqlalchemy import func

    products_to_replicate = []
    products = session.query(Niche).filter_by(status="active").all()

    for product in products:
        # Get affiliate data for this product (simplified - by matching posts)
        affiliate_data = session.query(Affiliate).filter_by(
            affiliate_network=product.affiliate_network
        ).all()

        total_clicks = sum(a.clicks for a in affiliate_data)
        total_conversions = sum(a.conversions for a in affiliate_data)
        conversion_rate = total_conversions / max(total_clicks, 1)

        if conversion_rate >= REPLICATE_CONVERSION_RATE:
            products_to_replicate.append(product.id)
            logger.info(f"High performer flagged: {product.product_name} ({conversion_rate*100:.1f}% CVR)")

        # Retire products with < 5 clicks after 3+ posts
        post_count = session.query(Post).join(
            "video", "script"
        ).filter_by(product_id=product.id).count()
        if total_clicks < 5 and post_count >= 3:
            product.status = "retired"
            logger.info(f"Retiring low-performer: {product.product_name} ({total_clicks} clicks / {post_count} posts)")

    return products_to_replicate


def run():
    logger.info("=== Job 7: Affiliate Tracker started ===")

    session = SessionLocal()
    try:
        earnings = sync_affiliate_earnings(session)
        replicate_ids = flag_high_performers(session)
        session.commit()

        total = sum(earnings.values())
        logger.info(f"Earnings today: ${total:.2f} | Products to replicate: {len(replicate_ids)}")
        logger.info("=== Job 7 complete ===")
    except Exception as e:
        session.rollback()
        logger.error(f"Job 7 failed: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    run()
