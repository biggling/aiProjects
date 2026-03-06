"""Global configuration loaded from .env"""
import os
import sys
import logging
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# ── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).parent
DESIGNS_DIR = BASE_DIR / os.getenv("DESIGNS_DIR", "designs")
REPORTS_DIR = BASE_DIR / os.getenv("REPORTS_DIR", "reports")
LOGS_DIR = BASE_DIR / os.getenv("LOGS_DIR", "logs")
SESSIONS_DIR = BASE_DIR / "sessions"
ASSETS_DIR = BASE_DIR / "assets"

for d in [DESIGNS_DIR, REPORTS_DIR, LOGS_DIR, SESSIONS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# ── Database ─────────────────────────────────────────────────────────────────
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///autoPOD.db")

# ── AI APIs ──────────────────────────────────────────────────────────────────
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
CLAUDE_MODEL = "claude-sonnet-4-6"

# ── Etsy ─────────────────────────────────────────────────────────────────────
ETSY_API_KEY = os.getenv("ETSY_API_KEY", "")
ETSY_API_SECRET = os.getenv("ETSY_API_SECRET", "")
ETSY_ACCESS_TOKEN = os.getenv("ETSY_ACCESS_TOKEN", "")
ETSY_REFRESH_TOKEN = os.getenv("ETSY_REFRESH_TOKEN", "")
ETSY_SHOP_ID = os.getenv("ETSY_SHOP_ID", "")
ETSY_BASE_URL = "https://openapi.etsy.com/v3"

# ── Printify ─────────────────────────────────────────────────────────────────
PRINTIFY_API_KEY = os.getenv("PRINTIFY_API_KEY", "")
PRINTIFY_SHOP_ID = os.getenv("PRINTIFY_SHOP_ID", "")
PRINTIFY_BASE_URL = "https://api.printify.com/v1"

# ── Redbubble ────────────────────────────────────────────────────────────────
REDBUBBLE_EMAIL = os.getenv("REDBUBBLE_EMAIL", "")
REDBUBBLE_PASSWORD = os.getenv("REDBUBBLE_PASSWORD", "")

# ── Pinterest ────────────────────────────────────────────────────────────────
PINTEREST_API_KEY = os.getenv("PINTEREST_API_KEY", "")
PINTEREST_ACCESS_TOKEN = os.getenv("PINTEREST_ACCESS_TOKEN", "")
PINTEREST_BASE_URL = "https://api.pinterest.com/v5"

# ── Notifications ────────────────────────────────────────────────────────────
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL", "")
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY", "")
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL", "")

# ── Business Rules ────────────────────────────────────────────────────────────
MAX_DESIGNS_PER_DAY = int(os.getenv("MAX_DESIGNS_PER_DAY", "5"))
MAX_LISTINGS_PER_DAY = int(os.getenv("MAX_LISTINGS_PER_DAY", "10"))
NICHE_SCORE_THRESHOLD = 0.5
TOP_NICHES_PER_RUN = 20
LISTING_PAUSE_DAYS_NO_SALES = 60
LISTING_REFRESH_DAYS_NO_SALES = 30

# ── Pricing Formulas ─────────────────────────────────────────────────────────
ETSY_PRICE_MULTIPLIER = 3.5
ETSY_SHIPPING = 3.99
AMAZON_PRICE_MULTIPLIER = 2.8
REDBUBBLE_MARGIN_PCT = 0.20

# ── Logging ──────────────────────────────────────────────────────────────────
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(getattr(logging, LOG_LEVEL, logging.INFO))
        fmt = logging.Formatter("%(asctime)s [%(name)s] %(levelname)s: %(message)s")
        # Console
        ch = logging.StreamHandler(sys.stdout)
        ch.setFormatter(fmt)
        logger.addHandler(ch)
        # File
        fh = logging.handlers.RotatingFileHandler(
            LOGS_DIR / f"{name}.log", maxBytes=5_000_000, backupCount=3
        )
        fh.setFormatter(fmt)
        logger.addHandler(fh)
    return logger

import logging.handlers  # noqa: E402 (import after usage in function)


def validate_required_keys(*keys: str) -> bool:
    missing = [k for k in keys if not os.getenv(k)]
    if missing:
        print(f"WARNING: Missing env vars: {', '.join(missing)}")
        return False
    return True
