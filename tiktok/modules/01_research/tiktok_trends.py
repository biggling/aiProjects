"""Fetch trending sounds and hashtags from TikTok."""

from datetime import datetime, date

import httpx
from loguru import logger

from modules.01_research.db import SessionLocal
from modules.01_research.models import Trend


def fetch_trending_hashtags(access_token: str, limit: int = 20) -> list[dict]:
    """Fetch trending hashtags from TikTok Research API."""
    url = "https://open.tiktokapis.com/v2/research/hashtag/trending/"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    payload = {"count": limit}

    try:
        with httpx.Client(timeout=30) as client:
            response = client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            return data.get("data", {}).get("hashtags", [])
    except httpx.HTTPStatusError as e:
        logger.warning(f"TikTok Research API error: {e}. Using fallback.")
        return _fallback_trending()
    except Exception as e:
        logger.warning(f"TikTok API request failed: {e}. Using fallback.")
        return _fallback_trending()


def _fallback_trending() -> list[dict]:
    """Fallback trending data when API is unavailable."""
    logger.info("Using fallback trending data for development")
    return [
        {"hashtag_name": "fyp", "use_count": 1000000},
        {"hashtag_name": "tiktokshop", "use_count": 500000},
        {"hashtag_name": "viral", "use_count": 800000},
        {"hashtag_name": "รีวิว", "use_count": 300000},
        {"hashtag_name": "ของดี", "use_count": 200000},
    ]


def scrape_trends(access_token: str, limit: int = 20) -> int:
    """Scrape trending data and store to database. Returns count of new records."""
    trends_data = fetch_trending_hashtags(access_token, limit)
    today = date.today().isoformat()
    count = 0

    db = SessionLocal()
    try:
        for item in trends_data:
            trend = Trend(
                date=today,
                hashtag=item.get("hashtag_name", ""),
                sound_name=item.get("sound_name"),
                use_count=item.get("use_count", 0),
                scraped_at=datetime.utcnow(),
            )
            db.add(trend)
            count += 1
        db.commit()
        logger.info(f"Stored {count} trending items")
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to store trends: {e}")
        raise
    finally:
        db.close()

    return count
