"""Affiliate API clients: Amazon PAAPI, TikTok Shop."""
import requests
from config import (
    AMAZON_ACCESS_KEY, AMAZON_SECRET_KEY, AMAZON_PARTNER_TAG,
    TIKTOK_SHOP_APP_KEY, TIKTOK_SHOP_ACCESS_TOKEN, get_logger
)

logger = get_logger("affiliate_api")

AMAZON_CATEGORIES = {
    "beauty": "BeautyRotator",
    "fitness": "SportsAndOutdoors",
    "gadgets": "Electronics",
    "food": "GroceryAndGourmetFood",
    "pets": "PetSupplies",
    "tech": "Computers",
}


def fetch_amazon_bestsellers(niche: str, limit: int = 5) -> list[dict]:
    """Fetch Amazon bestsellers in niche category using PAAPI."""
    if not AMAZON_ACCESS_KEY:
        logger.info("Amazon PAAPI not configured.")
        return []
    try:
        # PAAPI v5 SearchItems endpoint
        import hmac
        import hashlib
        import datetime

        endpoint = "webservices.amazon.com"
        path = "/paapi5/searchitems"
        category = AMAZON_CATEGORIES.get(niche.lower(), "All")

        payload = {
            "Keywords": niche,
            "Resources": [
                "ItemInfo.Title",
                "Offers.Listings.Price",
                "BrowseNodeInfo.BrowseNodes",
            ],
            "SearchIndex": category,
            "ItemCount": limit,
            "SortBy": "Featured",
            "PartnerTag": AMAZON_PARTNER_TAG,
            "PartnerType": "Associates",
            "Marketplace": "www.amazon.com",
        }

        headers = {
            "host": endpoint,
            "content-type": "application/json; charset=utf-8",
            "x-amz-target": "com.amazon.paapi5.v1.ProductAdvertisingAPIv1.SearchItems",
        }
        r = requests.post(
            f"https://{endpoint}{path}",
            json=payload,
            headers=headers,
            timeout=15,
        )
        if r.ok:
            items = r.json().get("SearchResult", {}).get("Items", [])
            return [
                {
                    "product_name": item.get("ItemInfo", {}).get("Title", {}).get("DisplayValue", ""),
                    "product_url": item.get("DetailPageURL", ""),
                    "affiliate_link": item.get("DetailPageURL", "") + f"?tag={AMAZON_PARTNER_TAG}",
                    "commission_pct": 3.0,  # Amazon standard ~3%
                    "affiliate_network": "amazon",
                }
                for item in items
            ]
    except Exception as e:
        logger.error(f"Amazon PAAPI failed: {e}")
    return []


def fetch_tiktok_shop_trending(niche: str, limit: int = 5) -> list[dict]:
    """Fetch trending products from TikTok Shop."""
    if not TIKTOK_SHOP_ACCESS_TOKEN:
        logger.info("TikTok Shop not configured.")
        return []
    try:
        r = requests.get(
            "https://open-api.tiktokglobalshop.com/product/202212/products/search",
            headers={
                "x-tts-access-token": TIKTOK_SHOP_ACCESS_TOKEN,
                "app-key": TIKTOK_SHOP_APP_KEY,
            },
            params={"keyword": niche, "page_size": limit, "sort_by": "SALES_VOLUME_DESC"},
            timeout=15,
        )
        if r.ok:
            items = r.json().get("data", {}).get("products", [])
            return [
                {
                    "product_name": item.get("title", ""),
                    "product_url": item.get("url", ""),
                    "affiliate_link": item.get("affiliate_link", item.get("url", "")),
                    "commission_pct": float(item.get("commission_rate", 10)),
                    "affiliate_network": "tiktok_shop",
                }
                for item in items
            ]
    except Exception as e:
        logger.error(f"TikTok Shop fetch failed: {e}")
    return []


def get_affiliate_earnings(period: str) -> dict:
    """Get affiliate earnings summary for a period (YYYY-MM-DD)."""
    # Amazon: requires PAAPI earnings report (not yet in PAAPI v5 — use Associate dashboard)
    # This is a placeholder for actual integration
    return {"amazon": 0.0, "tiktok_shop": 0.0, "period": period}
