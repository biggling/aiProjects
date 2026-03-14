"""Fetch TikTok Shop affiliate bestseller rankings."""

from datetime import datetime

import httpx
from loguru import logger

from modules.01_research.db import SessionLocal
from modules.01_research.models import Product


def fetch_bestsellers(access_token: str, min_commission: float = 10.0) -> list[dict]:
    """Fetch bestseller products from TikTok Shop affiliate API."""
    url = "https://open.tiktokapis.com/v2/affiliate/bestsellers/"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    try:
        with httpx.Client(timeout=30) as client:
            response = client.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            products = data.get("data", {}).get("products", [])
            return [p for p in products if p.get("commission_rate", 0) >= min_commission]
    except Exception as e:
        logger.warning(f"TikTok Shop API failed: {e}. Using fallback.")
        return _fallback_products(min_commission)


def _fallback_products(min_commission: float = 10.0) -> list[dict]:
    """Fallback product data for development."""
    logger.info("Using fallback product data for development")
    products = [
        {"name": "เซรั่มบำรุงผิว", "category": "Beauty", "price": 299.0, "commission_rate": 15.0, "rank": 1},
        {"name": "หูฟังบลูทูธ", "category": "Electronics", "price": 599.0, "commission_rate": 12.0, "rank": 2},
        {"name": "กระเป๋าสะพาย", "category": "Fashion", "price": 450.0, "commission_rate": 18.0, "rank": 3},
        {"name": "ครีมกันแดด SPF50", "category": "Beauty", "price": 350.0, "commission_rate": 14.0, "rank": 4},
        {"name": "เคสโทรศัพท์", "category": "Accessories", "price": 199.0, "commission_rate": 20.0, "rank": 5},
    ]
    return [p for p in products if p["commission_rate"] >= min_commission]


def scrape_products(access_token: str, min_commission: float = 10.0) -> int:
    """Scrape product data and store to database. Returns count of new records."""
    products_data = fetch_bestsellers(access_token, min_commission)
    count = 0

    db = SessionLocal()
    try:
        for item in products_data:
            product = Product(
                name=item["name"],
                category=item.get("category", ""),
                price=item.get("price", 0.0),
                commission_rate=item.get("commission_rate", 0.0),
                rank=item.get("rank", 0),
                scraped_at=datetime.utcnow(),
            )
            db.add(product)
            count += 1
        db.commit()
        logger.info(f"Stored {count} products")
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to store products: {e}")
        raise
    finally:
        db.close()

    return count
