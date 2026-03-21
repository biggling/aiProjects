"""Run all strategy backtests and compare results."""

import json
import sys
from pathlib import Path

import pandas as pd
from loguru import logger

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.strategies import grid, mean_reversion, momentum
from src.utils.config import OHLCV_DIR, RESULTS_DIR, SYMBOLS, DEFAULT_INTERVAL


def load_data(symbol: str, interval: str = DEFAULT_INTERVAL) -> pd.DataFrame:
    """Load OHLCV data from CSV."""
    path = OHLCV_DIR / f"{symbol}_{interval}.csv"
    if not path.exists():
        logger.error(f"Data file not found: {path}")
        logger.info("Run 'python -m src.data.downloader' first to download data.")
        sys.exit(1)
    df = pd.read_csv(path, parse_dates=["timestamp"])
    logger.info(f"Loaded {len(df)} candles for {symbol} from {df['timestamp'].min()} to {df['timestamp'].max()}")
    return df


def run_all():
    """Run all strategies on all symbols and print comparison."""
    all_results = []

    for symbol in SYMBOLS:
        logger.info(f"\n{'='*60}\n  {symbol}\n{'='*60}")
        df = load_data(symbol)

        # Grid Trading
        grid_result = grid.run_backtest(df)
        grid_result["symbol"] = symbol
        all_results.append(grid_result)

        # Mean Reversion
        mr_result = mean_reversion.run_backtest(df)
        mr_result["symbol"] = symbol
        all_results.append(mr_result)

        # Momentum
        mom_result = momentum.run_backtest(df)
        mom_result["symbol"] = symbol
        all_results.append(mom_result)

    # Print comparison table
    print(f"\n{'='*80}")
    print(f"  BACKTEST RESULTS COMPARISON")
    print(f"{'='*80}")
    print(f"{'Symbol':<10} {'Strategy':<35} {'Return %':>10} {'MaxDD %':>10} {'Win Rate':>10} {'Trades':>8}")
    print(f"{'-'*80}")

    for r in all_results:
        win_rate = r.get("win_rate_pct", "N/A")
        if isinstance(win_rate, (int, float)):
            win_rate = f"{win_rate:.1f}%"
        print(
            f"{r['symbol']:<10} {r['strategy']:<35} "
            f"{r['total_return_pct']:>9.2f}% {r['max_drawdown_pct']:>9.2f}% "
            f"{win_rate:>10} {r['total_trades']:>8}"
        )

    print(f"{'='*80}")

    # Save results
    results_path = RESULTS_DIR / "backtest_results.json"
    with open(results_path, "w") as f:
        json.dump(all_results, f, indent=2, default=str)
    logger.info(f"Results saved to {results_path}")

    return all_results


if __name__ == "__main__":
    run_all()
