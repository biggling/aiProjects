"""Job 8: Viral Trend Monitoring (30-min polling)
Schedule: Every 30 minutes
"""
import time
import feedparser
from pytrends.request import TrendReq
from database.models import SessionLocal, Topic
from utils.notify import alert_trend
from config import TREND_VELOCITY_THRESHOLD, get_logger

logger = get_logger("job8_trend_monitoring")

NEWS_FEEDS = [
    "https://feeds.bbci.co.uk/news/rss.xml",
    "https://techcrunch.com/feed/",
    "https://feeds.reuters.com/reuters/topNews",
]

_previous_scores: dict = {}  # in-memory baseline for velocity calc


def fetch_realtime_trends() -> dict:
    """Fetch real-time Google Trends (1-hour window)."""
    pytrends = TrendReq(hl="en-US", tz=0)
    trending = {}
    try:
        df = pytrends.trending_searches(pn="united_states")
        for topic in df[0].tolist()[:20]:
            trending[topic] = 80.0  # trending search = high score
    except Exception as e:
        logger.warning(f"Realtime trends failed: {e}")
    return trending


def fetch_news_breaking() -> list[str]:
    topics = []
    for url in NEWS_FEEDS:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:3]:
                topics.append(entry.title[:80])
        except Exception as e:
            logger.warning(f"RSS feed failed: {e}")
    return topics


def calculate_velocity(topic: str, current_score: float) -> float:
    prev = _previous_scores.get(topic, current_score)
    velocity = (current_score - prev) / (prev + 0.01)  # % change
    _previous_scores[topic] = current_score
    return velocity


def run():
    logger.info("=== Job 8: Trend Monitoring started ===")

    current_trends = fetch_realtime_trends()
    news_topics = fetch_news_breaking()

    # Add news topics with high base score
    for topic in news_topics:
        current_trends[topic] = current_trends.get(topic, 60.0)

    session = SessionLocal()
    triggered = 0

    try:
        for topic, score in current_trends.items():
            velocity = calculate_velocity(topic, score)

            if velocity >= TREND_VELOCITY_THRESHOLD:
                logger.info(f"HIGH VELOCITY TREND: {topic} (+{velocity*100:.0f}%)")
                alert_trend(topic, velocity * 100)

                # Check if already in DB
                existing = session.query(Topic).filter_by(topic=topic, status="pending").first()
                if not existing:
                    session.add(Topic(
                        topic=topic,
                        trend_score=round(score, 2),
                        source="realtime_trends",
                        status="pending",
                    ))
                    triggered += 1

        session.commit()
        if triggered:
            logger.info(f"Added {triggered} high-velocity topics for script generation")
        logger.info("=== Job 8 complete ===")

    except Exception as e:
        session.rollback()
        logger.error(f"Job 8 failed: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    run()
