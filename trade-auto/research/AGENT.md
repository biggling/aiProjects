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
- [2026-03-23] BTC trading in range $65k-$80k; institutional ETFs hold >$100B. (capitalstreetfx.com)
- [2026-03-23] BTC Dominance near 58.7%-60% resistance; Altcoin Season Index at 49. (thecoinrepublic.com)
- [2026-03-23] Sentiment neutral/bearish for majors; focus on RWAs and AI protocols. (reddit.com)

### Trading Strategies
- [2026-03-23] Top bots use hybrid momentum/mean-reversion with regime detection. (asutfiberglass.com)
- [2026-03-23] FreqAI (CatBoost/Random Forest) used for adaptive market learning. (bitget.com)
- [2026-03-23] GoCryptoTrader is the leading Go framework for high-concurrency HFT. (github.com)

### Exchange API Status
- [2026-03-23] Binance legacy api/v1 retires 2026-03-25; !ticker@arr retires 2026-03-26. (binance.com)
- [2026-03-23] Binance FIX TLS update requires SNI by 2026-06-08. (binance.com)
- [2026-03-23] Bybit V5 features APR history and autoReinvest for staking. (github.io)
- [2026-03-23] MEXC and Bitget offer lowest fees (0.01% - 0.05%). (coinbureau.com)

### Risk Management
- [2026-03-23] "Smart" DCA scales buys based on 200-day Moving Average distance. (bitget.com)
- [2026-03-23] Deep Reinforcement Learning (DRL) used for dynamic risk adjustment. (skywork.ai)
- [2026-03-23] Private mempools (Flashbots) used to prevent MEV sandwich attacks. (pto.org.tr)

### Opportunity Analysis
- [2026-03-23] Imminent altcoin rotation likely if BTC dominance fails at 60%. (capitalstreetfx.com)
- [2026-03-23] Institutional interest growing in tokenized Real-World Assets (RWAs). (svb.com)

### Market Size & Edge
- [2026-03-23] Total crypto market cap projected to exceed $4T in 2026. (bim.finance)

### Target Persona & Users
- [2026-03-23] Professional retail moving to high-performance Go/Rust bots over Python. (github.com)

### Community Signals
- [2026-03-23] Major crypto community migration from X to Threads (70% higher engagement). (posteverywhere.ai)

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
1. Save your complete findings to the file: trade-auto/research/findings/2026-03-23_2300.md
2. Also write the same content to: trade-auto/research/findings/latest.md
3. Use this exact structure for the findings file:

```
# trade-auto Research — 2026-03-23_2300

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
