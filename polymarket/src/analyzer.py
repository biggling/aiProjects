"""Polymarket data analyzer — identify mispricing and trends."""

import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
from loguru import logger

DATA_DIR = Path(__file__).parent.parent / "data"
DB_PATH = DATA_DIR / "polymarket.db"


def get_db() -> sqlite3.Connection:
    """Get database connection."""
    return sqlite3.connect(DB_PATH)


def get_active_markets(min_volume: float = 10000) -> pd.DataFrame:
    """Get active markets with minimum volume."""
    conn = get_db()
    df = pd.read_sql_query("""
        SELECT * FROM markets
        WHERE active = 1 AND volume >= ?
        ORDER BY volume DESC
    """, conn, params=(min_volume,))
    conn.close()
    logger.info(f"Found {len(df)} active markets with volume >= ${min_volume:,.0f}")
    return df


def detect_mispricing(threshold: float = 0.03) -> pd.DataFrame:
    """Find markets where YES + NO prices don't sum to ~1.0.

    A spread > threshold suggests mispricing or arb opportunity.
    """
    conn = get_db()
    df = pd.read_sql_query("""
        SELECT s.market_id, m.question, s.yes_price, s.no_price,
               (s.yes_price + s.no_price) as total,
               ABS(1.0 - (s.yes_price + s.no_price)) as spread,
               m.volume, s.snapshot_at
        FROM snapshots s
        JOIN markets m ON s.market_id = m.id
        WHERE m.active = 1
        AND s.snapshot_at = (SELECT MAX(snapshot_at) FROM snapshots WHERE market_id = s.market_id)
        ORDER BY spread DESC
    """, conn)
    conn.close()

    mispriced = df[df["spread"] > threshold]
    if len(mispriced) > 0:
        logger.info(f"Found {len(mispriced)} markets with spread > {threshold}")
    else:
        logger.info("No significant mispricing detected")
    return mispriced


def price_movers(hours: int = 24, min_move: float = 0.05) -> pd.DataFrame:
    """Find markets with largest price moves in the last N hours."""
    conn = get_db()
    cutoff = (datetime.utcnow() - timedelta(hours=hours)).isoformat()

    df = pd.read_sql_query("""
        SELECT s1.market_id, m.question,
               s1.yes_price as current_price,
               s2.yes_price as prev_price,
               (s1.yes_price - s2.yes_price) as price_change,
               m.volume
        FROM snapshots s1
        JOIN markets m ON s1.market_id = m.id
        JOIN snapshots s2 ON s1.market_id = s2.market_id
        WHERE s1.snapshot_at = (SELECT MAX(snapshot_at) FROM snapshots WHERE market_id = s1.market_id)
        AND s2.snapshot_at = (SELECT MIN(snapshot_at) FROM snapshots WHERE market_id = s2.market_id AND snapshot_at >= ?)
        AND s1.snapshot_at != s2.snapshot_at
        ORDER BY ABS(s1.yes_price - s2.yes_price) DESC
    """, conn, params=(cutoff,))
    conn.close()

    movers = df[df["price_change"].abs() >= min_move]
    logger.info(f"Found {len(movers)} markets with ≥{min_move*100:.0f}% move in {hours}h")
    return movers


def market_summary():
    """Print a summary of the current market state."""
    markets = get_active_markets(min_volume=0)
    mispriced = detect_mispricing()

    print(f"\n{'='*60}")
    print(f"  POLYMARKET SUMMARY")
    print(f"{'='*60}")
    print(f"  Active markets: {len(markets)}")
    print(f"  Total volume: ${markets['volume'].sum():,.0f}")
    print(f"  Mispriced (>3% spread): {len(mispriced)}")
    print()

    if len(markets) > 0:
        print("  Top 10 by Volume:")
        for _, row in markets.head(10).iterrows():
            q = row["question"][:50]
            print(f"    ${row['volume']:>12,.0f}  {q}")

    if len(mispriced) > 0:
        print(f"\n  Mispriced Markets:")
        for _, row in mispriced.head(5).iterrows():
            q = row["question"][:45]
            print(f"    Spread: {row['spread']:.3f}  YES:{row['yes_price']:.2f} NO:{row['no_price']:.2f}  {q}")

    print(f"{'='*60}")


if __name__ == "__main__":
    market_summary()
