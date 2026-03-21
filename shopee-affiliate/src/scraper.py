"""Shopee product scraper — fetches trending and bestselling products."""

from pathlib import Path
from datetime import datetime
import json
import requests
from loguru import logger
from dotenv import load_dotenv

load_dotenv()

DATA_DIR = Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)


def fetch_shopee_trending(category: str = "all", limit: int = 50) -> list[dict]:
    """Fetch trending products from Shopee Thailand.

    Note: Uses Shopee's public-facing endpoints.
    For affiliate links, use the Shopee Affiliate Platform API.
    """
    # Shopee public API endpoint for Thailand
    url = "https://shopee.co.th/api/v4/recommend/recommend"
    params = {
        "bundle": "category_landing_page",
        "limit": limit,
        "offset": 0,
    }

    try:
        resp = requests.get(url, params=params, timeout=30, headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
            "Accept-Language": "th-TH,th;q=0.9",
        })
        resp.raise_for_status()
        data = resp.json()
        products = []
        for item in data.get("data", {}).get("sections", [{}])[0].get("data", {}).get("item", []):
            products.append({
                "item_id": item.get("itemid"),
                "shop_id": item.get("shopid"),
                "name": item.get("name"),
                "price": item.get("price", 0) / 100000,  # Shopee price format
                "sold": item.get("historical_sold", 0),
                "rating": item.get("item_rating", {}).get("rating_star", 0),
                "image": item.get("image"),
                "scraped_at": datetime.now().isoformat(),
            })
        logger.info(f"Scraped {len(products)} trending products")
        return products

    except Exception as e:
        logger.warning(f"Shopee API unavailable, using fallback: {e}")
        return _fallback_products()


def _fallback_products() -> list[dict]:
    """Dev fallback data when API is unavailable."""
    return [
        {
            "item_id": "demo_001", "shop_id": "shop_001",
            "name": "เซรั่มวิตามินซี Skin1004", "price": 359.0,
            "sold": 12500, "rating": 4.8, "category": "beauty",
            "commission_rate": 12.0, "scraped_at": datetime.now().isoformat(),
        },
        {
            "item_id": "demo_002", "shop_id": "shop_002",
            "name": "หม้อทอดไร้น้ำมัน Simplus 4.5L", "price": 1290.0,
            "sold": 8700, "rating": 4.7, "category": "home",
            "commission_rate": 10.0, "scraped_at": datetime.now().isoformat(),
        },
        {
            "item_id": "demo_003", "shop_id": "shop_003",
            "name": "คอลลาเจน Savas Premium", "price": 590.0,
            "sold": 15200, "rating": 4.6, "category": "health",
            "commission_rate": 15.0, "scraped_at": datetime.now().isoformat(),
        },
    ]


def filter_by_commission(products: list[dict], min_rate: float = 10.0) -> list[dict]:
    """Filter products by minimum commission rate."""
    return [p for p in products if p.get("commission_rate", 0) >= min_rate]


def save_products(products: list[dict], filename: str = "trending"):
    """Save products to JSON file."""
    date_str = datetime.now().strftime("%Y-%m-%d")
    out_path = DATA_DIR / f"{filename}_{date_str}.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(products, f, ensure_ascii=False, indent=2)
    logger.info(f"Saved {len(products)} products to {out_path}")


def run():
    """Main scraper entry point."""
    products = fetch_shopee_trending()
    filtered = filter_by_commission(products)
    save_products(products, "all_trending")
    save_products(filtered, "high_commission")
    logger.info(f"Done: {len(products)} total, {len(filtered)} high-commission")
    return {"total": len(products), "high_commission": len(filtered)}


if __name__ == "__main__":
    run()
