"""Mean Reversion Strategy — RSI + Bollinger Bands.

Buy when RSI is oversold AND price is below lower Bollinger Band.
Sell when RSI is overbought AND price is above upper Bollinger Band.
"""

import pandas as pd
import ta
from loguru import logger

from src.utils.config import INITIAL_CAPITAL, COMMISSION_RATE


def run_backtest(
    df: pd.DataFrame,
    rsi_period: int = 14,
    bb_period: int = 20,
    bb_std: float = 2.0,
    oversold: float = 30.0,
    overbought: float = 70.0,
    capital: float = INITIAL_CAPITAL,
    commission: float = COMMISSION_RATE,
) -> dict:
    """Run mean reversion backtest using RSI + Bollinger Bands."""
    data = df.copy()
    data["rsi"] = ta.momentum.rsi(data["close"], window=rsi_period)
    bb = ta.volatility.BollingerBands(data["close"], window=bb_period, window_dev=bb_std)
    data["bb_upper"] = bb.bollinger_hband()
    data["bb_lower"] = bb.bollinger_lband()
    data["bb_mid"] = bb.bollinger_mavg()
    data = data.dropna().reset_index(drop=True)

    cash = capital
    position = 0.0
    entry_price = 0.0
    trades = []
    equity_curve = []
    wins = 0
    losses = 0

    for i in range(len(data)):
        price = data["close"].iloc[i]
        rsi = data["rsi"].iloc[i]
        bb_lower = data["bb_lower"].iloc[i]
        bb_upper = data["bb_upper"].iloc[i]

        # Buy signal: RSI oversold + price below lower BB
        if position == 0 and rsi < oversold and price < bb_lower:
            qty = (cash * (1 - commission)) / price
            position = qty
            entry_price = price
            cash = 0.0
            trades.append({"idx": i, "side": "buy", "price": price, "qty": qty})

        # Sell signal: RSI overbought + price above upper BB
        elif position > 0 and rsi > overbought and price > bb_upper:
            sell_value = position * price * (1 - commission)
            pnl = sell_value - (position * entry_price)
            if pnl > 0:
                wins += 1
            else:
                losses += 1
            cash = sell_value
            trades.append({"idx": i, "side": "sell", "price": price, "qty": position, "pnl": pnl})
            position = 0.0

        # Stop loss: -5% from entry
        elif position > 0 and price < entry_price * 0.95:
            sell_value = position * price * (1 - commission)
            losses += 1
            cash = sell_value
            trades.append({"idx": i, "side": "stop_loss", "price": price, "qty": position})
            position = 0.0

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
        "strategy": "Mean Reversion (RSI + BB)",
        "initial_capital": capital,
        "final_equity": round(final_equity, 2),
        "total_return_pct": round(total_return * 100, 2),
        "max_drawdown_pct": round(max_drawdown * 100, 2),
        "total_trades": len(trades),
        "wins": wins,
        "losses": losses,
        "win_rate_pct": round(win_rate, 2),
        "params": {
            "rsi_period": rsi_period, "bb_period": bb_period,
            "bb_std": bb_std, "oversold": oversold, "overbought": overbought,
        },
    }

    logger.info(f"Mean Reversion results: return={results['total_return_pct']}%, "
                f"win_rate={results['win_rate_pct']}%, max_dd={results['max_drawdown_pct']}%")
    return results
