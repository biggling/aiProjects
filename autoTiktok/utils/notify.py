"""Slack notifications for autoTiktok."""
import requests
from config import SLACK_WEBHOOK_URL, get_logger

logger = get_logger("notify")


def slack(message: str) -> bool:
    if not SLACK_WEBHOOK_URL:
        return False
    try:
        r = requests.post(SLACK_WEBHOOK_URL, json={"text": message}, timeout=10)
        return r.ok
    except Exception as e:
        logger.error(f"Slack failed: {e}")
        return False


def alert_review_queue(count: int, dir_path: str):
    slack(f":movie_camera: {count} TikTok scripts ready for review → `{dir_path}` (auto-approves in 2h)")


def alert_posted(platform: str, product: str, url: str = ""):
    slack(f":clapper: Posted on *{platform}*: {product[:50]} {url}")


def alert_commission(amount: float, product: str, network: str):
    slack(f":moneybag: Commission earned: ${amount:.2f} from *{product[:40]}* ({network})")


def alert_winner(video_id: int, views: int, platform: str):
    slack(f":fire: Winner! Video {video_id} on *{platform}*: {views:,} views — replicating...")
