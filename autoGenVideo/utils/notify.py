"""Slack notifications for autoGenVideo."""
import requests
from config import SLACK_WEBHOOK_URL, get_logger

logger = get_logger("notify")


def slack(message: str) -> bool:
    if not SLACK_WEBHOOK_URL:
        return False
    try:
        r = requests.post(SLACK_WEBHOOK_URL, json={"text": message}, timeout=10)
        return r.status_code == 200
    except Exception as e:
        logger.error(f"Slack failed: {e}")
        return False


def alert_viral(platform: str, topic: str, views: int, url: str = ""):
    slack(f":fire: Viral video on *{platform}*! Topic: {topic} — {views:,} views {url}")


def alert_posted(platform: str, topic: str, url: str = ""):
    slack(f":clapper: Posted on *{platform}*: {topic[:60]} {url}")


def alert_trend(topic: str, velocity: float):
    slack(f":chart_with_upwards_trend: Trending: *{topic}* ({velocity:.0f}% rise in 1h) — generating video...")
