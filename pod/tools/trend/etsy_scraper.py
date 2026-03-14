import asyncio
import random
import re
import time

from playwright.async_api import async_playwright
from sqlalchemy import select

from tools.shared.db import get_session
from tools.shared.models import Niche
from tools.shared.logger import get_logger

logger = get_logger("etsy_scraper")

USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
]

PAGE_DELAY = 2


async def scrape_etsy_keyword(page, keyword: str) -> float:
    """Scrape Etsy search results for a keyword and return competition score."""
    url = f"https://www.etsy.com/search?q={keyword.replace(' ', '+')}"
    await page.set_extra_http_headers({"User-Agent": random.choice(USER_AGENTS)})

    try:
        await page.goto(url, wait_until="domcontentloaded", timeout=15000)
        await page.wait_for_timeout(2000)

        # Extract listing data
        listings = await page.query_selector_all("[data-listing-id]")
        sales_counts = []

        for listing in listings[:20]:
            text = await listing.inner_text()
            # Look for sale count patterns like "1,234 sales" or "(1.2k sales)"
            match = re.search(r"([\d,]+(?:\.\d+)?)\s*[kK]?\s*sales", text)
            if match:
                raw = match.group(1).replace(",", "")
                count = float(raw)
                if "k" in text[match.start():match.end()].lower():
                    count *= 1000
                sales_counts.append(count)

        if sales_counts:
            avg_sales = sum(sales_counts) / len(sales_counts)
            # Normalize: higher avg sales = higher competition (0-1 scale)
            competition = min(avg_sales / 10000, 1.0)
        else:
            # If we got listings but no sales data, moderate competition
            competition = 0.5 if listings else 0.3

        logger.info(f"  {keyword}: {len(listings)} listings, competition={competition:.2f}")
        return competition

    except Exception as e:
        logger.warning(f"  Failed to scrape '{keyword}': {e}")
        return 0.5  # default mid-range on failure


async def _scrape_all(keywords_to_scrape: list[tuple[int, str]]) -> dict[int, float]:
    """Scrape competition data for all keywords."""
    results = {}
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        for niche_id, keyword in keywords_to_scrape:
            competition = await scrape_etsy_keyword(page, keyword)
            results[niche_id] = competition
            await asyncio.sleep(PAGE_DELAY)

        await browser.close()

    return results


def run():
    """Main entry point."""
    logger.info("Starting Etsy competition scrape")

    with get_session() as session:
        niches = session.execute(
            select(Niche).where(Niche.status == "active").order_by(Niche.trend_score.desc()).limit(20)
        ).scalars().all()
        keywords_to_scrape = [(n.id, n.keyword) for n in niches]

    if not keywords_to_scrape:
        logger.info("No active niches to scrape")
        return "0 niches scraped"

    results = asyncio.run(_scrape_all(keywords_to_scrape))

    with get_session() as session:
        for niche_id, competition in results.items():
            niche = session.get(Niche, niche_id)
            if niche:
                niche.competition = competition

    logger.info(f"Etsy scrape complete: {len(results)} niches updated")
    return f"{len(results)} niches scraped"
