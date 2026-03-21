"""Configuration and logging setup."""

from pathlib import Path
from dotenv import load_dotenv
from loguru import logger
import os
import sys

load_dotenv()

PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"
OHLCV_DIR = DATA_DIR / "ohlcv"
LOG_DIR = DATA_DIR / "logs"
RESULTS_DIR = PROJECT_ROOT / "backtests" / "results"

for d in [OHLCV_DIR, LOG_DIR, RESULTS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# Logging
logger.remove()
logger.add(sys.stderr, level=os.getenv("LOG_LEVEL", "INFO"))
logger.add(
    LOG_DIR / "trade_{time:YYYY-MM-DD}.log",
    rotation="1 day",
    retention="30 days",
    serialize=True,
    level="DEBUG",
)

# Binance
BINANCE_BASE_URL = "https://api.binance.com"
SYMBOLS = ["BTCUSDT", "ETHUSDT"]
DEFAULT_INTERVAL = "1h"
DEFAULT_LOOKBACK_DAYS = 365

# Trading defaults
INITIAL_CAPITAL = 10_000.0
COMMISSION_RATE = 0.001  # 0.1% per trade (Binance spot)
