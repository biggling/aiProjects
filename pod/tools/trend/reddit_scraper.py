import json
import time

import praw
from sqlalchemy import select

from tools.shared.api_clients import get_anthropic
from tools.shared.config import REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT
from tools.shared.db import get_session
from tools.shared.models import Niche
from tools.shared.logger import get_logger

logger = get_logger("reddit_scraper")

SUBREDDITS = ["Etsy", "printondemand", "redbubble"]
POST_LIMIT = 25
VELOCITY_BOOST = 0.3


def get_reddit() -> praw.Reddit:
    return praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        user_agent=REDDIT_USER_AGENT,
    )


def fetch_rising_posts(reddit: praw.Reddit) -> list[str]:
    """Collect titles from rising/hot posts across target subreddits."""
    titles = []
    for sub_name in SUBREDDITS:
        try:
            subreddit = reddit.subreddit(sub_name)
            for post in subreddit.hot(limit=POST_LIMIT):
                titles.append(post.title)
            time.sleep(1)  # respect rate limit
        except Exception as e:
            logger.warning(f"Failed to fetch r/{sub_name}: {e}")
    return titles


def extract_keywords(titles: list[str]) -> list[str]:
    """Use Claude to extract niche/product keywords from post titles."""
    if not titles:
        return []

    client = get_anthropic()
    titles_text = "\n".join(f"- {t}" for t in titles[:50])

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": (
                "Extract print-on-demand niche keywords from these Reddit post titles. "
                "Return ONLY a JSON array of lowercase keyword strings (e.g. [\"cat mom\", \"retro gaming\"]). "
                "Focus on product niches, trending themes, and design ideas. "
                "Ignore meta/business posts. Max 20 keywords.\n\n"
                f"{titles_text}"
            ),
        }],
    )

    text = response.content[0].text.strip()
    # Parse JSON, handle potential markdown wrapping
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    return json.loads(text)


def upsert_reddit_niches(keywords: list[str]) -> int:
    """Upsert keywords into niches table, boosting velocity for existing ones."""
    updated = 0
    with get_session() as session:
        for kw in keywords:
            kw = kw.lower().strip()
            if not kw or len(kw) < 3:
                continue

            niche = session.execute(
                select(Niche).where(Niche.keyword == kw)
            ).scalar_one_or_none()

            if niche:
                niche.velocity = (niche.velocity or 0) + VELOCITY_BOOST
            else:
                niche = Niche(
                    keyword=kw,
                    trend_score=50.0,  # default mid-range
                    velocity=VELOCITY_BOOST,
                    status="active",
                )
                session.add(niche)
            updated += 1

    return updated


def run():
    """Main entry point."""
    logger.info("Starting Reddit scrape")

    reddit = get_reddit()
    titles = fetch_rising_posts(reddit)
    logger.info(f"Fetched {len(titles)} post titles")

    keywords = extract_keywords(titles)
    logger.info(f"Extracted {len(keywords)} keywords via Claude")

    count = upsert_reddit_niches(keywords)
    logger.info(f"Reddit scrape complete: {count} niches upserted")

    return f"{count} niches from Reddit"
