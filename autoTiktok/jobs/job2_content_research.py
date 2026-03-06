"""Job 2: Content & Trend Research
Schedule: Every 4 hours
"""
import time
import random
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from database.models import SessionLocal, Niche, Trend
from utils.ai_utils import classify_hook_pattern
from config import get_logger

logger = get_logger("job2_content_research")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"
}


def scrape_tiktok_search(keyword: str, limit: int = 10) -> list[dict]:
    """Scrape TikTok search results for keyword (public data)."""
    results = []
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(f"https://www.tiktok.com/search?q={keyword}", timeout=20000)
            page.wait_for_timeout(3000)

            # Extract video items from search results
            videos = page.query_selector_all("[data-e2e='search_top-item']")[:limit]
            for vid in videos:
                try:
                    desc = vid.query_selector("[data-e2e='search-card-desc']")
                    views = vid.query_selector("[data-e2e='video-views']")
                    results.append({
                        "caption": desc.inner_text()[:200] if desc else "",
                        "views": views.inner_text() if views else "0",
                    })
                except Exception:
                    pass
            browser.close()
    except Exception as e:
        logger.warning(f"TikTok scrape failed for '{keyword}': {e} — using fallback data")
        # Fallback: synthetic trend data for testing
        results = [
            {"caption": f"This {keyword} hack will change your life #fyp #{keyword.replace(' ', '')}", "views": "1.2M"},
            {"caption": f"5 best {keyword} products you need in 2026 #trending", "views": "800K"},
        ]
    return results


def extract_hashtags(caption: str) -> list[str]:
    return [word for word in caption.split() if word.startswith("#")]


def run():
    logger.info("=== Job 2: Content Research started ===")

    session = SessionLocal()
    saved = 0

    try:
        niches = session.query(Niche).filter_by(status="active").distinct(Niche.niche).limit(6).all()
        seen_niches = set()

        for niche_row in niches:
            niche = niche_row.niche
            if niche in seen_niches:
                continue
            seen_niches.add(niche)

            videos = scrape_tiktok_search(niche, limit=5)
            logger.info(f"Got {len(videos)} videos for niche: {niche}")

            for video in videos:
                caption = video.get("caption", "")
                hashtags = extract_hashtags(caption)

                # Classify hook pattern
                hook_text = " ".join(caption.split()[:12])
                try:
                    classification = classify_hook_pattern(hook_text)
                    hook_pattern = classification.get("pattern", "bold_claim")
                except Exception:
                    hook_pattern = "bold_claim"

                trend = Trend(
                    niche=niche,
                    hook_pattern=hook_pattern,
                    hook_text=hook_text,
                    hashtags=",".join(hashtags[:5]),
                    views=0,
                    scraped_at=datetime.utcnow(),
                )
                session.add(trend)
                saved += 1

            time.sleep(random.uniform(2, 5))

        session.commit()
        logger.info(f"Saved {saved} trend records.")
        logger.info("=== Job 2 complete ===")
    except Exception as e:
        session.rollback()
        logger.error(f"Job 2 failed: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    run()
