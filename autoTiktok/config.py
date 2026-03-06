"""Global configuration for autoTiktok."""
import os
import sys
import logging
import logging.handlers
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).parent
SCRIPTS_DIR = BASE_DIR / "scripts"
VIDEOS_DIR = BASE_DIR / "videos"
ASSETS_DIR = BASE_DIR / "assets"
REPORTS_DIR = BASE_DIR / "reports"
LOGS_DIR = BASE_DIR / "logs"
REVIEW_QUEUE_DIR = BASE_DIR / "review_queue"

for d in [SCRIPTS_DIR, VIDEOS_DIR, ASSETS_DIR / "fonts", ASSETS_DIR / "music",
          ASSETS_DIR / "templates", REPORTS_DIR, LOGS_DIR, REVIEW_QUEUE_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# Database
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///autoTiktok.db")

# AI
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "")
CLAUDE_MODEL = "claude-sonnet-4-6"

# TikTok
TIKTOK_CLIENT_KEY = os.getenv("TIKTOK_CLIENT_KEY", "")
TIKTOK_CLIENT_SECRET = os.getenv("TIKTOK_CLIENT_SECRET", "")
TIKTOK_ACCESS_TOKEN = os.getenv("TIKTOK_ACCESS_TOKEN", "")

# Instagram
INSTAGRAM_ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN", "")
INSTAGRAM_BUSINESS_ACCOUNT_ID = os.getenv("INSTAGRAM_BUSINESS_ACCOUNT_ID", "")

# YouTube
YOUTUBE_CLIENT_ID = os.getenv("YOUTUBE_CLIENT_ID", "")
YOUTUBE_CLIENT_SECRET = os.getenv("YOUTUBE_CLIENT_SECRET", "")
YOUTUBE_REFRESH_TOKEN = os.getenv("YOUTUBE_REFRESH_TOKEN", "")

# Amazon Affiliate
AMAZON_ACCESS_KEY = os.getenv("AMAZON_ACCESS_KEY", "")
AMAZON_SECRET_KEY = os.getenv("AMAZON_SECRET_KEY", "")
AMAZON_PARTNER_TAG = os.getenv("AMAZON_PARTNER_TAG", "")

# TikTok Shop
TIKTOK_SHOP_APP_KEY = os.getenv("TIKTOK_SHOP_APP_KEY", "")
TIKTOK_SHOP_APP_SECRET = os.getenv("TIKTOK_SHOP_APP_SECRET", "")
TIKTOK_SHOP_ACCESS_TOKEN = os.getenv("TIKTOK_SHOP_ACCESS_TOKEN", "")

# Content
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY", "")
PIXABAY_API_KEY = os.getenv("PIXABAY_API_KEY", "")

# Notifications
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL", "")

# App settings
MAX_POSTS_PER_DAY = int(os.getenv("MAX_POSTS_PER_DAY", "3"))
MAX_ENGAGEMENT_ACTIONS_PER_HOUR = int(os.getenv("MAX_ENGAGEMENT_ACTIONS_PER_HOUR", "50"))
DEFAULT_LANGUAGE = os.getenv("DEFAULT_LANGUAGE", "en")
REVIEW_QUEUE_TIMEOUT_HOURS = int(os.getenv("REVIEW_QUEUE_TIMEOUT_HOURS", "2"))

# Video specs
VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920
VIDEO_FPS = 30
VIDEO_BITRATE = "8M"

# Performance thresholds
WINNER_VIEWS_24H = 1000
LOSER_VIEWS_48H = 200
WINNER_FOLLOWS_24H = 50
VIRAL_COMMISSION_THRESHOLD = 50.0  # USD
REPLICATE_CONVERSION_RATE = 0.03   # 3%

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(getattr(logging, LOG_LEVEL, logging.INFO))
        fmt = logging.Formatter("%(asctime)s [%(name)s] %(levelname)s: %(message)s")
        ch = logging.StreamHandler(sys.stdout)
        ch.setFormatter(fmt)
        logger.addHandler(ch)
        fh = logging.handlers.RotatingFileHandler(
            LOGS_DIR / f"{name}.log", maxBytes=5_000_000, backupCount=3
        )
        fh.setFormatter(fmt)
        logger.addHandler(fh)
    return logger
