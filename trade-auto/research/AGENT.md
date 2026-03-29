# trade-auto — Research Agent

## Agent Instructions

1. **Read `## Known Facts` below first.** Do not re-research any fact already listed there.
2. Focus only on questions marked ❓ (unknown) or facts that may have changed since their `[date]`.
3. After saving findings, **update `## Known Facts`** — add new facts, update changed ones, remove stale ones.
4. Keep Known Facts concise: one line per fact, with date and source URL.

---

## Known Facts
<!-- Agent updates this section after each run. Date format: YYYY-MM-DD -->

### Market Conditions
- [2026-03-27] BTC fell to ~$69,036–$69,990; rejected at $72K; below all EMAs (50d $72,081 / 100d $77,846 / 200d $86,066). (cryptotimes.io)
- [2026-03-27] $14.16B options expiry occurred March 27; max pain $75K; post-expiry 3–7 day tradeable window active March 28 – April 3. (coindesk.com, coinpedia.org)
- [2026-03-27] Extreme Fear index reading of 10 — worst in 16 months; market cap contracted to $2.36–$2.48T. (blockchainmagazine.net)
- [2026-03-28] BTC Dominance 56.4%; Altcoin Season Index 27–35; firmly Bitcoin Season; altseason requires index >75. (coinmarketcap.com, ainvest.com)
- [2026-03-28] MACD + RSI Golden Cross on altcoin dominance monthly chart — potential rotation signal (not confirmed); last similar signal Nov 2023. (ainvest.com)
- [2026-03-28] Hyperliquid (HYPE) is breakout altcoin of 2026 YTD (L1 transition); AI (TAO) and RWA (ONDO) sectors continue outperforming. (cryptoticker.io)
- [2026-03-28] Spot BTC ETF inflows down 73% in March to ~$890M vs $3.3B in February; March 24 single-day flow: -$66.6M. (fensory.com, coinglass.com)
- [2026-03-28] Institutional capital rotating into tokenized treasury products ($12.8B March flows); ETF inflows = only 6.5% of digital asset flows vs 34% in January. (fensory.com)
- [2026-03-28] Large pension/sovereign wealth funds = 67% of BTC ETF AUM; institutional base stable but fresh inflows stalled. (fensory.com)
- [2026-03-28] April 2026 analyst consensus BTC range: $74K–$80K; regime = ranging/corrective. (investing.com, changelly.com)

### Key April 2026 Macro Events
- [2026-03-27] April 13–18: CLARITY Act Senate Banking Committee markup — last window before midterms. (phemex.com)
- [2026-03-27] April 27–29: Bitcoin Conference Las Vegas; April 28–29: FOMC; April 29–30: TOKEN2049 Dubai. (phemex.com)
- [2026-03-27] FOMC April 28–29: rates at 3.50–3.75%; only 1 cut projected for 2026; BTC fell after 8 of last 9 meetings. (phemex.com)
- [2026-03-27] Powell term expires May 15; Warsh transition adds additional uncertainty to April FOMC. (phemex.com)

### Trading Strategies
- [2026-03-26] Multi-timeframe aggregation with 0.6 threshold reduces false signals by 40%. (noows.com.tr)
- [2026-03-26] 2:1 Reward-to-Risk ratio now outperforms traditional 3:1 in efficient 2026 markets. (noows.com.tr)
- [2026-03-27] Mean reversion (RSI+BB) Sharpe ~2.3; momentum (EMA/MACD) Sharpe ~1.0; 50/50 blend = Sharpe 1.71. (medium.com/@briplotnik)
- [2026-03-27] Current sideways/downtrend regime explicitly favors mean reversion over momentum. (medium.com/@briplotnik)
- [2026-03-28] Adaptive dual-mode strategy (mean reversion + breakout, switching via Hilbert Transform + BB) showed strong ETH backtest results. (pyquantlab.medium.com)
- [2026-03-28] Jan 2026 week-1 backtest: Trend Following +3.0R vs Mean Reversion +1.45R; trend following 2x more profitable in trending periods. (medium.com/@tapu0531)
- [2026-03-28] Threshold rebalancing outperformed hold by 77.1% median return; RL models achieved 85% cumulative return vs 45% traditional (2020–2025). (darkbot.io)
- [2026-03-28] Freqtrade 2026.1 released: Hyperliquid HIP3 support, enhanced FreqUI metrics (CAGR, Calmar, Sortino, Sharpe, SQN), Python 3.13 support. (freqtrade.io)
- [2026-03-27] BBGO (c9s/bbgo) is actively maintained Go framework with KLine backtesting and dnum precision. (github.com)
- [2026-03-27] NostalgiaForInfinityX6 = recommended stable Freqtrade strategy; X7 = active dev version. (alexbobes.com)
- [2026-03-26] "Agentic trading" via autonomous execution is the new industry focal point. (binance.com)

### Exchange API Status
- [2026-03-27] Bybit: cancelled order history limited to 7 days (was 180 days) — BREAKING CHANGE March 26. (bybit-exchange.github.io)
- [2026-03-27] Bybit: `ips` request field removed; IP address API modification via API prohibited. (bybit-exchange.github.io)
- [2026-03-27] Bybit: Orderbook depth for Perps/Futures expanded from 200 to 500 (March 21). (bybit-exchange.github.io)
- [2026-03-28] Bybit March 26: New endpoints added (Spread Max Qty, Option Asset Info, Portfolio Margin Info, Total Members Assets); no breaking changes in March. (bybit-exchange.github.io)
- [2026-03-26] Binance !ticker@arr retired; must migrate to <symbol>@ticker or !miniTicker@arr. (binance.com)
- [2026-03-26] Binance Ai Pro launched 2026-03-25; supports isolated sub-account agentic trading. (binance.com)
- [2026-03-28] **BREAKING — Binance v1 endpoints retired March 25:** `/api/v1/ping`, `/api/v1/time`, v1 historical trade endpoints all dead. (developers.binance.com)
- [2026-03-28] **Upcoming April 2 — Binance:** Successful order endpoints weight=0; RAW_REQUESTS limit → 300K/5min; STP Transfer enabled all symbols. (developers.binance.com)
- [2026-03-28] Binance March 9 (live): New price range execution rule endpoints `GET /api/v3/executionRules`, `GET /api/v3/referencePrice`, stream `<symbol>@referencePrice`. (developers.binance.com)
- [2026-03-26] FIX TLS update scheduled for June 8, 2026; SNI support will be mandatory. (binance.com)
- [2026-03-27] MEXC offers 0% maker fees — relevant for limit-order-heavy strategies. (ventureburn.com)

### Risk Management
- [2026-03-27] Kelly criterion: 0.25x recommended in current extreme-fear + geopolitical regime (lower end of 0.25–0.5x range). (medium.com/@tmapendembe_28659)
- [2026-03-27] Half Kelly retains 75% of max growth rate at 25% of full Kelly variance — strong mathematical basis. (medium.com/@tmapendembe_28659)
- [2026-03-27] ATR-based volatility-adjusted position sizing is 2026 best practice — reduce size during high ATR. (darkbot.io)
- [2026-03-28] Max drawdown target: <15–20% in live trading; circuit breakers mandatory at predefined thresholds. (darkbot.io)
- [2026-03-28] Risk priority: (1) stop-loss, (2) take-profit, (3) portfolio exposure balance, (4) real-time drawdown circuit breaker. (darkbot.io)
- [2026-03-28] Key insight: risk management > entry signal optimization; robust controls outperform sophisticated entries with weak protection. (darkbot.io)
- [2026-03-26] Best-in-class: 25% undeployed capital reserve for capitalizing on market dislocations. (ph.org.tr)
- [2026-03-26] Failsafe: API latency >200ms should trigger automatic strategy halt or switch. (ph.org.tr)
- [2026-03-26] 8-10% drift tolerance for rebalancing is the current institutional standard. (xbto.com)
- [2026-03-28] Never risk >1–2% capital on any single trade; recalibrate settings monthly. (bitget.com)

### Opportunity Analysis
- [2026-03-28] Post-expiry tradeable window active: March 28 – April 3; next major event: April 28–29 FOMC. (coinpedia.org)
- [2026-03-28] AI (TAO), RWA (ONDO), and HYPE (Hyperliquid L1) are 2026 YTD outperformers vs BTC. (cryptoticker.io)

### Market Size & Edge
- [2026-03-26] Institutional HFT actively "hunting" simple bots; multi-signal confirmation is mandatory. (noows.com.tr)
- [2026-03-28] Algorithmic trading >80% of crypto volume in 2026; pure price-action single-indicator bots face intense competition. (darkbot.io)

---

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

## After Research — Update This File

After saving findings, edit this file (`trade-auto/research/AGENT.md`) and update `## Known Facts`:
- Add any new facts discovered (with date and source URL)
- Update facts that have changed (update the date)
- Mark ❓ any fact you couldn't verify this run
- Remove facts that are confirmed stale

## Output Instructions
1. Save your complete findings to the file: trade-auto/research/findings/2026-03-26_2300.md
2. Also write the same content to: trade-auto/research/findings/latest.md
3. Use this exact structure for the findings file:

```
# trade-auto Research — 2026-03-26_2300

## [Topic Section 1]
- Finding with source URL
- Finding with source URL

## [Topic Section 2]
...

## Action Items for Work Agent
- [ ] Specific action triggered by research
- [ ] Another action

## Sentiment
Overall: [Bullish / Neutral / Bearish / Opportunity / Risk]
Reasoning: one sentence
```

4. After saving both files, print a 5-bullet summary of the most important findings to stdout.
