"""Grid Trading Strategy — for range-bound markets.

Places buy and sell orders at fixed price intervals within a defined range.
Profits from price oscillation within the grid.
"""

import numpy as np
import pandas as pd
from loguru import logger

from src.utils.config import INITIAL_CAPITAL, COMMISSION_RATE


def run_backtest(
    df: pd.DataFrame,
    num_grids: int = 20,
    range_pct: float = 0.20,
    capital: float = INITIAL_CAPITAL,
    commission: float = COMMISSION_RATE,
) -> dict:
    """Run grid trading backtest.

    Args:
        df: OHLCV DataFrame with columns [timestamp, open, high, low, close, volume]
        num_grids: Number of grid levels
        range_pct: Price range as percentage of median price (e.g. 0.20 = ±10%)
        capital: Starting capital in quote currency (USDT)
        commission: Commission rate per trade
    """
    prices = df["close"].values
    median_price = np.median(prices)
    upper_bound = median_price * (1 + range_pct / 2)
    lower_bound = median_price * (1 - range_pct / 2)
    grid_levels = np.linspace(lower_bound, upper_bound, num_grids)
    grid_spacing = grid_levels[1] - grid_levels[0]

    logger.info(
        f"Grid: {num_grids} levels, range [{lower_bound:.2f} - {upper_bound:.2f}], "
        f"spacing {grid_spacing:.2f}"
    )

    # State
    cash = capital
    position = 0.0  # base currency held
    order_size = capital / num_grids  # allocate equally across grid levels
    trades = []
    equity_curve = []

    # Track which grid levels have been "filled" (bought at)
    bought_levels = set()

    for i, price in enumerate(prices):
        # Check each grid level
        for j, level in enumerate(grid_levels):
            # Buy signal: price drops to or below a grid level we haven't bought
            if price <= level and j not in bought_levels and cash >= order_size:
                qty = (order_size * (1 - commission)) / price
                cash -= order_size
                position += qty
                bought_levels.add(j)
                trades.append({
                    "idx": i, "side": "buy", "price": price,
                    "qty": qty, "value": order_size,
                })

            # Sell signal: price rises to grid level + spacing for a level we bought
            elif price >= level + grid_spacing and j in bought_levels and position > 0:
                qty = order_size / level  # original qty bought at this level
                qty = min(qty, position)
                sell_value = qty * price * (1 - commission)
                cash += sell_value
                position -= qty
                bought_levels.discard(j)
                trades.append({
                    "idx": i, "side": "sell", "price": price,
                    "qty": qty, "value": sell_value,
                })

        equity = cash + position * price
        equity_curve.append(equity)

    # Final equity
    final_price = prices[-1]
    final_equity = cash + position * final_price
    total_return = (final_equity - capital) / capital
    equity_series = pd.Series(equity_curve)
    rolling_max = equity_series.cummax()
    drawdown = (equity_series - rolling_max) / rolling_max
    max_drawdown = drawdown.min()

    buy_trades = [t for t in trades if t["side"] == "buy"]
    sell_trades = [t for t in trades if t["side"] == "sell"]

    results = {
        "strategy": "Grid Trading",
        "initial_capital": capital,
        "final_equity": round(final_equity, 2),
        "total_return_pct": round(total_return * 100, 2),
        "max_drawdown_pct": round(max_drawdown * 100, 2),
        "total_trades": len(trades),
        "buy_trades": len(buy_trades),
        "sell_trades": len(sell_trades),
        "grid_levels": num_grids,
        "range": f"[{lower_bound:.2f} - {upper_bound:.2f}]",
        "remaining_position_value": round(position * final_price, 2),
        "cash": round(cash, 2),
    }

    logger.info(f"Grid results: return={results['total_return_pct']}%, "
                f"max_dd={results['max_drawdown_pct']}%, trades={results['total_trades']}")
    return results
