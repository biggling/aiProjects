"""Polymarket data collector — fetches market data from Gamma API."""

import json
import sqlite3
import time
from datetime import datetime
from pathlib import Path

import requests
from loguru import logger
from dotenv import load_dotenv

load_dotenv()

DATA_DIR = Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = DATA_DIR / "polymarket.db"

GAMMA_API = "https://gamma-api.polymarket.com"
CLOB_API = "https://clob.polymarket.com"


def init_db():
    """Initialize SQLite database with required tables."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS markets (
            id TEXT PRIMARY KEY,
            question TEXT,
            category TEXT,
            end_date TEXT,
            active INTEGER,
            closed INTEGER,
            volume REAL,
            liquidity REAL,
            created_at TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS snapshots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            market_id TEXT,
            yes_price REAL,
            no_price REAL,
            volume REAL,
            liquidity REAL,
            snapshot_at TEXT,
            FOREIGN KEY (market_id) REFERENCES markets(id)
        )
    """)
    conn.commit()
    conn.close()
    logger.info(f"Database initialized at {DB_PATH}")


def fetch_markets(limit: int = 100, active: bool = True) -> list[dict]:
    """Fetch markets from Gamma API."""
    params = {"limit": limit, "active": str(active).lower()}
    try:
        resp = requests.get(f"{GAMMA_API}/markets", params=params, timeout=30)
        resp.raise_for_status()
        markets = resp.json()
        logger.info(f"Fetched {len(markets)} markets")
        return markets
    except Exception as e:
        logger.error(f"Failed to fetch markets: {e}")
        return []


def fetch_events(limit: int = 50) -> list[dict]:
    """Fetch events (grouped markets) from Gamma API."""
    params = {"limit": limit, "active": "true"}
    try:
        resp = requests.get(f"{GAMMA_API}/events", params=params, timeout=30)
        resp.raise_for_status()
        events = resp.json()
        logger.info(f"Fetched {len(events)} events")
        return events
    except Exception as e:
        logger.error(f"Failed to fetch events: {e}")
        return []


def save_markets(markets: list[dict]):
    """Save markets to SQLite."""
    conn = sqlite3.connect(DB_PATH)
    now = datetime.utcnow().isoformat()

    for m in markets:
        # Upsert market
        conn.execute("""
            INSERT OR REPLACE INTO markets (id, question, category, end_date, active, closed, volume, liquidity, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            m.get("id", ""),
            m.get("question", ""),
            m.get("category", ""),
            m.get("endDate", ""),
            1 if m.get("active") else 0,
            1 if m.get("closed") else 0,
            float(m.get("volume", 0) or 0),
            float(m.get("liquidity", 0) or 0),
            now,
        ))

        # Save price snapshot
        prices = m.get("outcomePrices", "[]")
        if isinstance(prices, str):
            try:
                prices = json.loads(prices)
            except json.JSONDecodeError:
                prices = []

        yes_price = float(prices[0]) if len(prices) > 0 else 0.0
        no_price = float(prices[1]) if len(prices) > 1 else 0.0

        conn.execute("""
            INSERT INTO snapshots (market_id, yes_price, no_price, volume, liquidity, snapshot_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            m.get("id", ""),
            yes_price,
            no_price,
            float(m.get("volume", 0) or 0),
            float(m.get("liquidity", 0) or 0),
            now,
        ))

    conn.commit()
    conn.close()
    logger.info(f"Saved {len(markets)} markets and snapshots to DB")


def run():
    """Main collector entry point."""
    init_db()
    markets = fetch_markets(limit=200)
    if markets:
        save_markets(markets)
    logger.info(f"Collection complete: {len(markets)} markets")
    return {"markets_collected": len(markets)}


if __name__ == "__main__":
    run()
