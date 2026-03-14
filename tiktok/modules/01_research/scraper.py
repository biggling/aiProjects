"""Main research orchestrator — runs all scrapers in sequence."""

import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from dotenv import load_dotenv
from loguru import logger

from modules.01_research.db import init_db
from modules.01_research.tiktok_trends import scrape_trends
from modules.01_research.shop_products import scrape_products
from modules.01_research.competitor import scrape_competitor_hooks

load_dotenv()

# Configure loguru
LOG_DIR = Path("data/logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)
logger.add(LOG_DIR / "research.log", rotation="1 day", retention="7 days", serialize=True)


def run_research() -> dict:
    """Run all research scrapers. Returns summary dict."""
    access_token = os.getenv("TIKTOK_ACCESS_TOKEN", "")
    summary = {"trends": 0, "products": 0, "hooks": 0}

    # Initialize database tables
    init_db()

    # 1. Scrape trends
    try:
        logger.info("Starting trend scraper...")
        summary["trends"] = scrape_trends(access_token)
    except Exception as e:
        logger.error(f"Trend scraper failed: {e}")

    # 2. Scrape products
    try:
        logger.info("Starting product scraper...")
        summary["products"] = scrape_products(access_token)
    except Exception as e:
        logger.error(f"Product scraper failed: {e}")

    # 3. Scrape competitor hooks
    try:
        logger.info("Starting competitor hook scraper...")
        # Use trending hashtags for competitor research
        hashtags = ["tiktokshop", "รีวิว", "ของดี", "viral", "fyp"]
        summary["hooks"] = scrape_competitor_hooks(access_token, hashtags)
    except Exception as e:
        logger.error(f"Competitor hook scraper failed: {e}")

    logger.info(f"Research complete: {summary}")
    return summary


if __name__ == "__main__":
    result = run_research()
    print(f"Research summary: {result}")
