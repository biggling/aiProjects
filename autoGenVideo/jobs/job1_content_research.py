"""Job 1: Content & Trend Research
Schedule: Every 4 hours
"""
import time
import random
import requests
import feedparser
from bs4 import BeautifulSoup
from pytrends.request import TrendReq
from database.models import SessionLocal, Topic
from config import YOUTUBE_API_KEY, REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, get_logger

logger = get_logger("job1_content_research")

SEED_TOPICS = [
    "productivity tips", "life hacks", "AI tools", "fitness motivation",
    "money saving", "cooking recipes", "travel destinations", "mental health",
    "technology news", "DIY projects", "business tips", "study motivation",
]

NEWS_FEEDS = [
    "https://feeds.bbci.co.uk/news/rss.xml",
    "https://techcrunch.com/feed/",
]


def fetch_google_trends(keywords: list) -> dict:
    pytrends = TrendReq(hl="en-US", tz=0)
    scores = {}
    for i in range(0, len(keywords), 5):
        batch = keywords[i:i + 5]
        try:
            pytrends.build_payload(batch, timeframe="now 4-H")
            data = pytrends.interest_over_time()
            for kw in batch:
                if not data.empty and kw in data.columns:
                    scores[kw] = float(data[kw].mean())
            time.sleep(random.uniform(4, 7))
        except Exception as e:
            logger.warning(f"pytrends error: {e}")
    return scores


def fetch_youtube_trending() -> list[str]:
    if not YOUTUBE_API_KEY:
        return []
    try:
        r = requests.get(
            "https://www.googleapis.com/youtube/v3/videos",
            params={
                "part": "snippet",
                "chart": "mostPopular",
                "regionCode": "US",
                "maxResults": 20,
                "key": YOUTUBE_API_KEY,
            },
            timeout=15,
        )
        items = r.json().get("items", [])
        return [item["snippet"]["title"][:80] for item in items]
    except Exception as e:
        logger.warning(f"YouTube trending failed: {e}")
        return []


def fetch_reddit_hot(subreddits: list) -> list[str]:
    if not REDDIT_CLIENT_ID:
        return []
    try:
        import praw
        reddit = praw.Reddit(
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_CLIENT_SECRET,
            user_agent="autoGenVideo/1.0",
        )
        topics = []
        for sub in subreddits[:3]:
            for post in reddit.subreddit(sub).hot(limit=5):
                if not post.stickied:
                    topics.append(post.title[:80])
        return topics
    except Exception as e:
        logger.warning(f"Reddit fetch failed: {e}")
        return []


def fetch_news_topics() -> list[str]:
    topics = []
    for url in NEWS_FEEDS:
        try:
            feed = feedparser.parse(url)
            topics.extend(e.title[:80] for e in feed.entries[:5])
        except Exception as e:
            logger.warning(f"RSS feed failed {url}: {e}")
    return topics


def score_topic(trend_score: float) -> float:
    return min(trend_score / 100.0, 1.0)


def run():
    logger.info("=== Job 1: Content Research started ===")

    trend_scores = fetch_google_trends(SEED_TOPICS)
    yt_topics = fetch_youtube_trending()
    reddit_topics = fetch_reddit_hot(["todayilearned", "productivity", "technology"])
    news_topics = fetch_news_topics()

    all_candidates = []
    for t, s in trend_scores.items():
        all_candidates.append({"topic": t, "trend_score": s, "source": "pytrends"})
    for t in yt_topics:
        all_candidates.append({"topic": t, "trend_score": random.uniform(40, 80), "source": "youtube_trending"})
    for t in reddit_topics:
        all_candidates.append({"topic": t, "trend_score": random.uniform(30, 70), "source": "reddit"})
    for t in news_topics:
        all_candidates.append({"topic": t, "trend_score": random.uniform(50, 90), "source": "news_rss"})

    all_candidates.sort(key=lambda x: x["trend_score"], reverse=True)
    top = all_candidates[:10]
    logger.info(f"Top {len(top)} topics selected.")

    session = SessionLocal()
    try:
        for item in top:
            session.add(Topic(
                topic=item["topic"],
                trend_score=round(item["trend_score"], 2),
                source=item["source"],
                status="pending",
            ))
        session.commit()
        logger.info(f"Saved {len(top)} topics to DB.")
    except Exception as e:
        session.rollback()
        logger.error(f"DB write failed: {e}")
    finally:
        session.close()

    logger.info("=== Job 1 complete ===")
    return top


if __name__ == "__main__":
    run()
