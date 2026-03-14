import asyncio
import re

from playwright.async_api import async_playwright
from sqlalchemy import select

from tools.shared.db import get_session
from tools.shared.models import Niche, Listing
from tools.shared.logger import get_logger

logger = get_logger("price_adjuster")


async def scrape_competitor_prices(keyword: str) -> list[float]:
    """Scrape top 20 Etsy results for pricing data."""
    prices = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        url = f"https://www.etsy.com/search?q={keyword.replace(' ', '+')}"
        try:
            await page.goto(url, wait_until="domcontentloaded", timeout=15000)
            await page.wait_for_timeout(2000)

            listings = await page.query_selector_all("[data-listing-id]")
            for listing in listings[:20]:
                text = await listing.inner_text()
                price_match = re.search(r"\$(\d+\.?\d*)", text)
                if price_match:
                    prices.append(float(price_match.group(1)))

        except Exception as e:
            logger.warning(f"Failed to scrape prices for '{keyword}': {e}")
        finally:
            await browser.close()

    return prices


def generate_report(keyword: str, our_price: float, competitor_prices: list[float]) -> str:
    """Generate a price comparison report."""
    if not competitor_prices:
        return f"{keyword}: No competitor prices found"

    median = sorted(competitor_prices)[len(competitor_prices) // 2]
    avg = sum(competitor_prices) / len(competitor_prices)
    low = min(competitor_prices)
    high = max(competitor_prices)

    lines = [
        f"Niche: {keyword}",
        f"  Our price: ${our_price:.2f}",
        f"  Competitor median: ${median:.2f}",
        f"  Competitor range: ${low:.2f} - ${high:.2f}",
        f"  Competitor avg: ${avg:.2f}",
    ]

    if our_price > median * 1.2:
        lines.append("  ⚠ WARNING: Our price is >20% above median")
    elif our_price < median * 1.1:
        lines.append("  💡 RECOMMENDATION: Consider raising price")
    else:
        lines.append("  ✅ Price is in competitive range")

    return "\n".join(lines)


def run():
    """Generate price comparison report for active niches."""
    logger.info("Starting price check")

    with get_session() as session:
        niches = session.execute(
            select(Niche).where(Niche.status == "active").limit(10)
        ).scalars().all()
        niche_keywords = [(n.id, n.keyword) for n in niches]

    if not niche_keywords:
        logger.info("No active niches to check")
        return "0 niches checked"

    our_price = 24.99  # Default price from Printify setup
    reports = []

    for niche_id, keyword in niche_keywords:
        try:
            prices = asyncio.run(scrape_competitor_prices(keyword))
            report = generate_report(keyword, our_price, prices)
            reports.append(report)
            logger.info(f"\n{report}")
        except Exception as e:
            logger.error(f"Price check failed for {keyword}: {e}")

    logger.info(f"Price check complete: {len(reports)} niches analysed")
    return f"{len(reports)} niches checked"
