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

# Image generation backend: "auto" | "gemini" | "stability" | "dalle"
# "auto" tries Gemini first (cheaper), falls back to Stability AI, then DALL-E.
IMAGE_BACKEND = _optional("IMAGE_BACKEND", "auto")

# Gemini image model: "imagen-4.0-generate-001" (best quality) or
# "gemini-3.1-flash-image-preview" (faster/cheaper)
GEMINI_IMAGE_MODEL = _optional("GEMINI_IMAGE_MODEL", "gemini-3.1-flash-image-preview")

# Etsy — Shop A (personalized gifts / seasonal)
ETSY_API_KEY = _optional("ETSY_API_KEY")
ETSY_SHOP_ID = _optional("ETSY_SHOP_ID")

# Etsy — Shop B (aesthetics / identity; launch Month 2)
ETSY_API_KEY_B = _optional("ETSY_API_KEY_B")
ETSY_SHOP_ID_B = _optional("ETSY_SHOP_ID_B")

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
CELERY_BROKER_URL = _optional("CELERY_BROKER_URL", "sqla+sqlite:///data/celery_broker.db")
CELERY_RESULT_BACKEND = _optional("CELERY_RESULT_BACKEND", "db+sqlite:///data/celery_results.db")
DASHBOARD_USER = _optional("DASHBOARD_USER", "admin")
DASHBOARD_PASS = _optional("DASHBOARD_PASS", "changeme")

# Seed keywords for trend research
# Update weekly: add seasonal keywords before each holiday, remove after peak.
SEED_KEYWORDS = [
    # URGENT — Mother's Day (May 10): list NOW
    "personalized mom gift",
    "first mother's day gift",
    "mama sweatshirt personalized",
    "custom tumbler for mom",
    "gift for stepmom",
    "promoted to grandma gift",
    "twin mom gift",
    "patchwork mama sweatshirt",
    "matching mama mini outfit",
    "mom mode on tote bag",

    # URGENT — Father's Day (June 21): list by May 1
    "best dad ever gift personalized",
    "fishing dad shirt funny",
    "camping dad gift",
    "golf dad tee",
    "gamer dad mug",
    "dog dad shirt",
    "first father's day gift",

    # URGENT — Pride Month (June 1-30): list by May 1
    "pride month shirt rainbow",
    "pride tote bag inclusive",

    # EVERGREEN — Gen X Women / Milestone gifts
    "turning 50 gift women",
    "turning 60 gift women",
    "retirement gift teacher",
    "retirement gift nurse",
    "empty nester gift",
    "milestone birthday tee women",
    "promoted to grandma 2026",

    # EVERGREEN — Personalized / Star Maps
    "star map personalized anniversary",
    "custom coordinates wall art",
    "personalized family name sign",
    "where we met map print",

    # EVERGREEN — Tote Bags / Mugs (high gross margin)
    "funny quote tote bag",
    "aesthetic tote bag bookish",
    "custom mug name milestone",
    "personalized coffee mug funny",

    # TRENDING 2026 — Crossbody bags (61% YoY search growth)
    "aesthetic crossbody bag",
    "cottagecore crossbody bag",
    "literary girl crossbody bag",

    # TRENDING 2026 — Aesthetic niches
    "romantic goth sweatshirt",
    "dark academia aesthetic shirt",
    "literary girl tote bag",
    "bookish mug reader gift",
    "chateaucore aesthetic mug",
    "circus maximalist wall art",

    # MEDIUM — Outdoor / hobby micro-niches
    "hiking gift women funny",
    "plant mom tote bag",
    "disc golf shirt funny",
    "glamping shirt women",

    # MEDIUM — Pet niche
    "custom pet portrait mug",
    "dog mom sweatshirt personalized",
    "cat mom gift funny",
]
