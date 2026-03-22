# trade-auto — Research Agent

## Context
Automated crypto trading bots. Currently implementing 3 strategies with backtesting.
Target: run unattended on VPS, trade on Binance/Bybit. Risk-managed, not high-frequency.

## Research Tasks

### 1. Market Conditions Overview
Search: "crypto market outlook 2026 Q2", "Bitcoin trend analysis March 2026", "altcoin season 2026"
- What is the current macro crypto market regime (trending up, trending down, ranging)?
- Which altcoins are outperforming BTC this month?
- Any major macro events (Fed, BTC halving effects, ETF flows) in the next 30 days?
- Current BTC dominance — altcoin season possible?

### 2. Trading Strategy Research
Search: "crypto momentum strategy backtest 2026", "mean reversion crypto 2026", "RSI divergence crypto strategy"
- Any new strategy papers or community backtests published recently?
- What strategies are trending in quant crypto communities (Hacker News, Reddit)?
- Any Go-based trading bot libraries or frameworks worth adopting?
- Backtesting results for momentum vs. mean-reversion in current regime?

### 3. Exchange API Updates
Search: "Binance API update 2026", "Bybit API v5 changes", "crypto exchange fees comparison 2026"
- Any breaking changes to Binance or Bybit APIs in the last month?
- Fee structure changes affecting profitability calculations?
- Any new exchanges with better fees or API reliability?

### 4. Risk Management Research
Search: "crypto bot drawdown management", "position sizing crypto bot", "Kelly criterion crypto"
- Current best practices for drawdown limits in automated bots?
- Any new position sizing approaches for volatile markets?
- What max drawdown thresholds do profitable bots operate at?

### 5. Community Signals
Search: site:reddit.com/r/algotrading "crypto" 2026, "quantconnect crypto 2026", "freqtrade strategy 2026"
- What strategies are working for the r/algotrading community right now?
- Any new open-source crypto bot frameworks to study?
- Sentiment around automated trading profitability in 2026?

## Sources to Check
- https://www.reddit.com/r/algotrading/
- https://www.reddit.com/r/CryptoCurrency/ (top posts this week)
- https://freqtrade.io/en/stable/ (strategy updates)
- CoinGecko trending page
- Glassnode or CryptoQuant free tier indicators

## Decision Triggers — Flag if Found
- Binance/Bybit API breaking change → must fix before next backtest
- Strong trend regime detected → momentum strategy should outperform
- BTC drops >15% in a week → pause live trading, review risk params
- New Go trading library with active maintenance → evaluate for adoption
