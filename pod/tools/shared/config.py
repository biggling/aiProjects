import os
from dotenv import load_dotenv

load_dotenv()


def _require(key: str) -> str:
    val = os.getenv(key)
    if not val:
        raise RuntimeError(f"Missing required env var: {key}")
    return val


def _optional(key: str, default: str = "") -> str:
    return os.getenv(key, default)


# AI
ANTHROPIC_API_KEY = _optional("ANTHROPIC_API_KEY")
OPENAI_API_KEY = _optional("OPENAI_API_KEY")
STABILITY_API_KEY = _optional("STABILITY_API_KEY")
GEMINI_API_KEY = _optional("GEMINI_API_KEY")

# Etsy
ETSY_API_KEY = _optional("ETSY_API_KEY")
ETSY_SHOP_ID = _optional("ETSY_SHOP_ID")

# Printify
PRINTIFY_API_KEY = _optional("PRINTIFY_API_KEY")
PRINTIFY_SHOP_ID = _optional("PRINTIFY_SHOP_ID")

# Reddit
REDDIT_CLIENT_ID = _optional("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = _optional("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = _optional("REDDIT_USER_AGENT", "pod-bot/1.0")

# Social
BUFFER_ACCESS_TOKEN = _optional("BUFFER_ACCESS_TOKEN")
META_ACCESS_TOKEN = _optional("META_ACCESS_TOKEN")
META_PAGE_ID = _optional("META_PAGE_ID")

# Notifications
TELEGRAM_BOT_TOKEN = _optional("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = _optional("TELEGRAM_CHAT_ID")

# Storage
S3_BUCKET = _optional("S3_BUCKET")
S3_ACCESS_KEY = _optional("S3_ACCESS_KEY")
S3_SECRET_KEY = _optional("S3_SECRET_KEY")
S3_ENDPOINT_URL = _optional("S3_ENDPOINT_URL")

# App
DATABASE_URL = _optional("DATABASE_URL", "sqlite:///data/pod.db")
REDIS_URL = _optional("REDIS_URL", "redis://redis:6379/0")
DASHBOARD_USER = _optional("DASHBOARD_USER", "admin")
DASHBOARD_PASS = _optional("DASHBOARD_PASS", "changeme")

# Seed keywords for trend research
SEED_KEYWORDS = [
    "funny cat shirt", "motivational quotes", "retro vintage",
    "dog mom", "nurse life", "teacher appreciation",
    "hiking adventure", "gaming", "plant mom", "introvert",
]
