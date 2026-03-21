"""Momentum / Trend Following Strategy — EMA Crossover + MACD confirmation.

Buy when fast EMA crosses above slow EMA with MACD histogram positive.
Sell when fast EMA crosses below slow EMA or trailing stop hit.
"""

import pandas as pd
import ta
from loguru import logger

from src.utils.config import INITIAL_CAPITAL, COMMISSION_RATE


def run_backtest(
    df: pd.DataFrame,
    fast_ema: int = 12,
    slow_ema: int = 26,
    macd_signal: int = 9,
    trailing_stop_pct: float = 0.05,
    capital: float = INITIAL_CAPITAL,
    commission: float = COMMISSION_RATE,
) -> dict:
    """Run momentum/trend following backtest using EMA crossover + MACD."""
    data = df.copy()
    data["ema_fast"] = ta.trend.ema_indicator(data["close"], window=fast_ema)
    data["ema_slow"] = ta.trend.ema_indicator(data["close"], window=slow_ema)
    macd = ta.trend.MACD(data["close"], window_slow=slow_ema, window_fast=fast_ema, window_sign=macd_signal)
    data["macd_hist"] = macd.macd_diff()
    data = data.dropna().reset_index(drop=True)

    cash = capital
    position = 0.0
    entry_price = 0.0
    highest_since_entry = 0.0
    trades = []
    equity_curve = []
    wins = 0
    losses = 0

    prev_ema_fast = data["ema_fast"].iloc[0]
    prev_ema_slow = data["ema_slow"].iloc[0]

    for i in range(1, len(data)):
        price = data["close"].iloc[i]
        ema_f = data["ema_fast"].iloc[i]
        ema_s = data["ema_slow"].iloc[i]
        macd_h = data["macd_hist"].iloc[i]

        # Detect crossover
        cross_up = prev_ema_fast <= prev_ema_slow and ema_f > ema_s
        cross_down = prev_ema_fast >= prev_ema_slow and ema_f < ema_s

        if position > 0:
            highest_since_entry = max(highest_since_entry, price)
            trailing_stop = highest_since_entry * (1 - trailing_stop_pct)

        # Buy: EMA cross up + MACD histogram positive
        if position == 0 and cross_up and macd_h > 0:
            qty = (cash * (1 - commission)) / price
            position = qty
            entry_price = price
            highest_since_entry = price
            cash = 0.0
            trades.append({"idx": i, "side": "buy", "price": price, "qty": qty})

        # Sell: EMA cross down OR trailing stop hit
        elif position > 0 and (cross_down or price < trailing_stop):
            sell_value = position * price * (1 - commission)
            pnl = sell_value - (position * entry_price)
            if pnl > 0:
                wins += 1
            else:
                losses += 1
            reason = "cross_down" if cross_down else "trailing_stop"
            cash = sell_value
            trades.append({"idx": i, "side": "sell", "price": price, "qty": position, "reason": reason})
            position = 0.0

        prev_ema_fast = ema_f
        prev_ema_slow = ema_s

        equity = cash + position * price
        equity_curve.append(equity)

    final_price = data["close"].iloc[-1]
    final_equity = cash + position * final_price
    total_return = (final_equity - capital) / capital
    equity_series = pd.Series(equity_curve)
    rolling_max = equity_series.cummax()
    drawdown = (equity_series - rolling_max) / rolling_max
    max_drawdown = drawdown.min()
    total_closed = wins + losses
    win_rate = (wins / total_closed * 100) if total_closed > 0 else 0.0

    results = {
        "strategy": "Momentum (EMA Crossover + MACD)",
        "initial_capital": capital,
        "final_equity": round(final_equity, 2),
        "total_return_pct": round(total_return * 100, 2),
        "max_drawdown_pct": round(max_drawdown * 100, 2),
        "total_trades": len(trades),
        "wins": wins,
        "losses": losses,
        "win_rate_pct": round(win_rate, 2),
        "params": {
            "fast_ema": fast_ema, "slow_ema": slow_ema,
            "macd_signal": macd_signal, "trailing_stop_pct": trailing_stop_pct,
        },
    }

    logger.info(f"Momentum results: return={results['total_return_pct']}%, "
                f"win_rate={results['win_rate_pct']}%, max_dd={results['max_drawdown_pct']}%")
    return results
