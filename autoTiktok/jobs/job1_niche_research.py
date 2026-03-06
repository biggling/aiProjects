"""Job 1: Niche & Product Research
Schedule: Daily at 06:00 UTC
"""
from datetime import datetime
from database.models import SessionLocal, Niche
from utils.affiliate_api import fetch_amazon_bestsellers, fetch_tiktok_shop_trending
from utils.notify import slack
from config import get_logger

logger = get_logger("job1_niche_research")

SEED_NICHES = ["beauty", "fitness", "gadgets", "food", "pets", "tech"]


def score_product(trend_score: float, commission_pct: float, competition: float = 0.5) -> float:
    return (trend_score * commission_pct) / (competition * 100 + 1)


def run():
    logger.info("=== Job 1: Niche Research started ===")

    session = SessionLocal()
    saved = 0

    try:
        for niche in SEED_NICHES:
            products = fetch_tiktok_shop_trending(niche, limit=3)
            if not products:
                products = fetch_amazon_bestsellers(niche, limit=3)

            for product in products:
                trend_score = 60.0  # default
                perf_score = score_product(trend_score, product.get("commission_pct", 3.0))

                existing = session.query(Niche).filter_by(
                    product_url=product["product_url"]
                ).first()
                if existing:
                    existing.trend_score = trend_score
                    existing.performance_score = perf_score
                    existing.updated_at = datetime.utcnow()
                else:
                    session.add(Niche(
                        niche=niche,
                        product_name=product["product_name"],
                        product_url=product["product_url"],
                        affiliate_link=product["affiliate_link"],
                        affiliate_network=product["affiliate_network"],
                        commission_pct=product["commission_pct"],
                        trend_score=trend_score,
                        performance_score=perf_score,
                    ))
                    saved += 1

        session.commit()
        logger.info(f"Saved {saved} new products to niches DB.")
        logger.info("=== Job 1 complete ===")
    except Exception as e:
        session.rollback()
        logger.error(f"Job 1 failed: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    run()
