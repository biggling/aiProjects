"""Download OHLCV data from Binance public API."""

import time
from pathlib import Path

import pandas as pd
import requests
from loguru import logger

from src.utils.config import BINANCE_BASE_URL, OHLCV_DIR, DEFAULT_INTERVAL, DEFAULT_LOOKBACK_DAYS


def fetch_klines(
    symbol: str,
    interval: str = DEFAULT_INTERVAL,
    lookback_days: int = DEFAULT_LOOKBACK_DAYS,
) -> pd.DataFrame:
    """Fetch OHLCV klines from Binance public API (no auth required)."""
    url = f"{BINANCE_BASE_URL}/api/v3/klines"
    end_ms = int(time.time() * 1000)
    start_ms = end_ms - (lookback_days * 24 * 60 * 60 * 1000)

    all_klines = []
    current_start = start_ms

    while current_start < end_ms:
        params = {
            "symbol": symbol,
            "interval": interval,
            "startTime": current_start,
            "endTime": end_ms,
            "limit": 1000,
        }
        resp = requests.get(url, params=params, timeout=30)
        resp.raise_for_status()
        klines = resp.json()

        if not klines:
            break

        all_klines.extend(klines)
        current_start = klines[-1][0] + 1  # next ms after last candle

        logger.debug(f"{symbol}: fetched {len(klines)} candles, total {len(all_klines)}")
        time.sleep(0.1)  # respect rate limits

    df = pd.DataFrame(all_klines, columns=[
        "timestamp", "open", "high", "low", "close", "volume",
        "close_time", "quote_volume", "trades", "taker_buy_base",
        "taker_buy_quote", "ignore",
    ])

    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    for col in ["open", "high", "low", "close", "volume"]:
        df[col] = df[col].astype(float)

    df = df[["timestamp", "open", "high", "low", "close", "volume"]].copy()
    df = df.drop_duplicates(subset="timestamp").sort_values("timestamp").reset_index(drop=True)
    return df


def download_all(
    symbols: list[str] | None = None,
    interval: str = DEFAULT_INTERVAL,
    lookback_days: int = DEFAULT_LOOKBACK_DAYS,
) -> dict[str, Path]:
    """Download OHLCV data for all symbols and save as CSV."""
    from src.utils.config import SYMBOLS as default_symbols

    symbols = symbols or default_symbols
    saved = {}

    for symbol in symbols:
        logger.info(f"Downloading {symbol} {interval} data ({lookback_days} days)...")
        df = fetch_klines(symbol, interval, lookback_days)
        out_path = OHLCV_DIR / f"{symbol}_{interval}.csv"
        df.to_csv(out_path, index=False)
        logger.info(f"Saved {len(df)} candles to {out_path}")
        saved[symbol] = out_path

    return saved


if __name__ == "__main__":
    download_all()
