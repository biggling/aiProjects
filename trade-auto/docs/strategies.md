# Trading Strategies Research

## 1. Grid Trading

**Logic:** Place buy and sell orders at fixed price intervals within a defined range. When price drops to a grid level, buy. When price rises one grid spacing above a bought level, sell. Profits from price oscillation.

**Parameters:**
- `num_grids`: Number of grid levels (default: 20)
- `range_pct`: Total range as % of median price (default: 20%)
- `order_size`: Capital / num_grids per level

**Best market conditions:** Sideways/ranging markets with clear support and resistance. Fails in strong trends (gets trapped on one side).

**Risk profile:**
- Low risk in ranging markets
- High risk in trending markets (inventory accumulates on wrong side)
- Max loss limited to capital deployed
- No leverage in our implementation

---

## 2. Mean Reversion (RSI + Bollinger Bands)

**Logic:** Buy when RSI indicates oversold AND price is below the lower Bollinger Band (double confirmation of oversold condition). Sell when RSI indicates overbought AND price is above upper Bollinger Band. Includes 5% stop loss.

**Parameters:**
- `rsi_period`: RSI calculation window (default: 14)
- `bb_period`: Bollinger Band moving average window (default: 20)
- `bb_std`: Standard deviations for bands (default: 2.0)
- `oversold`: RSI buy threshold (default: 30)
- `overbought`: RSI sell threshold (default: 70)

**Best market conditions:** Ranging markets with clear mean-reverting behavior. Works well when volatility is consistent.

**Risk profile:**
- Medium risk — stop loss limits downside per trade
- Can miss trends entirely if market doesn't mean-revert
- Win rate typically 40-55% but winners are larger than losers

---

## 3. Momentum / Trend Following (EMA Crossover + MACD)

**Logic:** Buy when fast EMA crosses above slow EMA with MACD histogram positive (confirming momentum). Sell when fast EMA crosses below slow EMA or trailing stop is hit. Trailing stop locks in profits during strong trends.

**Parameters:**
- `fast_ema`: Fast EMA period (default: 12)
- `slow_ema`: Slow EMA period (default: 26)
- `macd_signal`: MACD signal line period (default: 9)
- `trailing_stop_pct`: Trailing stop distance (default: 5%)

**Best market conditions:** Strong trending markets (both up and down). Fails in choppy sideways markets (whipsaw losses).

**Risk profile:**
- Medium-high risk — can accumulate whipsaw losses in ranging markets
- Large winners in trending markets compensate for frequent small losses
- Trailing stop provides dynamic risk management
- Win rate typically 30-45% but risk/reward ratio > 2:1

---

## Strategy Selection Guide

| Condition | Best Strategy |
|-----------|--------------|
| BTC ranging ±10% for weeks | Grid Trading |
| Post-crash recovery (oversold) | Mean Reversion |
| Bull/bear market (clear trend) | Momentum |
| Unknown | Run all three, let results decide |

## Next Steps
- Run backtests on 1 year of BTC/ETH data
- Compare risk-adjusted returns (Sharpe ratio)
- Select best performer for paper trading
- Implement live trading with Binance API (Phase 2)
