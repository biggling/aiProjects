"""
Gemini-powered trend discovery for Etsy print-on-demand.

Asks Gemini to identify trending niches, themes, and keywords that are
currently selling well on Etsy as print-on-demand products (t-shirts, mugs,
tote bags, stickers, etc.), then upserts the results into the niches table.
"""

import json
import re

from google import genai
from sqlalchemy import select

from tools.shared.config import GEMINI_API_KEY
from tools.shared.db import get_session
from tools.shared.models import Niche
from tools.shared.logger import get_logger

logger = get_logger("gemini_trend_scraper")

MODEL = "gemini-2.0-flash"

PROMPT = """You are an expert Etsy print-on-demand market researcher.

Identify 20 trending niche keywords that are currently popular and have strong
buying intent on Etsy for print-on-demand products such as t-shirts, hoodies,
mugs, tote bags, and stickers.

Focus on:
- Seasonal and upcoming holiday themes (next 60 days)
- Viral pop-culture moments, memes, or movements
- Professions and identity groups (nurses, teachers, dog moms, gamers, etc.)
- Hobbies and lifestyle niches (hiking, yoga, gardening, reading, etc.)
- Motivational and humor niches with evergreen appeal
- Underserved micro-niches with low competition but rising search volume

For each keyword return a JSON object with:
- "keyword": short search phrase (2-5 words), as someone would type on Etsy
- "trend_score": estimated popularity 0-100 (100 = peak trend right now)
- "velocity": momentum score -1.0 to 1.0 (positive = rising, negative = fading)
- "reason": one sentence explaining why this niche is trending now

Return ONLY a valid JSON array of 20 objects, no markdown, no extra text.
"""


def fetch_gemini_trends() -> list[dict]:
    """Call Gemini API and parse the trending niches response."""
    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY is not set in environment")

    client = genai.Client(api_key=GEMINI_API_KEY)
    response = client.models.generate_content(model=MODEL, contents=PROMPT)
    text = response.text.strip()

    # Strip markdown code fences if present
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)

    trends = json.loads(text)
    return trends


def upsert_niches(trends: list[dict]) -> int:
    """Upsert Gemini trend data into the niches table."""
    updated = 0
    with get_session() as session:
        for item in trends:
            keyword = item.get("keyword", "").strip().lower()
            if not keyword:
                continue

            niche = session.execute(
                select(Niche).where(Niche.keyword == keyword)
            ).scalar_one_or_none()

            if niche:
                niche.trend_score = float(item.get("trend_score", niche.trend_score))
                niche.velocity = float(item.get("velocity", niche.velocity or 0.0))
            else:
                niche = Niche(
                    keyword=keyword,
                    trend_score=float(item.get("trend_score", 50.0)),
                    velocity=float(item.get("velocity", 0.0)),
                    status="active",
                )
                session.add(niche)
            updated += 1

    return updated


def run():
    """Main entry point."""
    logger.info("Starting Gemini POD trend discovery")

    trends = fetch_gemini_trends()
    logger.info(f"Gemini returned {len(trends)} trending niches")

    for item in trends:
        logger.info(
            f"  [{item.get('trend_score', '?'):>5.1f} | vel {item.get('velocity', 0):+.2f}] "
            f"{item.get('keyword')} — {item.get('reason', '')}"
        )

    count = upsert_niches(trends)
    logger.info(f"Gemini trend scrape complete: {count} niches upserted")
    return f"{count} niches upserted"
