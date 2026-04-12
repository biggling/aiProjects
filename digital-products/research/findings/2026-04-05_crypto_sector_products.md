# Digital Products — Crypto Sector Research
> 2026-04-05 | 10 products at the intersection of crypto trading + BiG's actual trade-auto project

---

## BiG's Crypto Context (from trade-auto/continue.md)

BiG is actively building:
- Python trading bot with 3 strategies: Grid Trading, Mean Reversion (RSI + BB), Momentum (EMA + MACD)
- Binance API integration (OHLCV downloader, backtesting runner)
- CLAUDE.md already written for trading bot development
- Phase 1 backtesting in progress

**This is the key moat**: BiG isn't theorizing about trading bots — he's building one right now.
Every product below is derived from work he's doing anyway.

---

## Market Context

| Signal | Figure | Source |
|---|---|---|
| AI crypto trading bot market 2026 | $54.07B → $200.27B by 2035 (14% CAGR) | StreetInsider |
| Pine Script community scripts | 150,000+ published on TradingView | TradingView |
| BingX Grid Bot users | 160,000+ active, $670M+ allocated | BingX |
| Freqtrade GitHub stars | 30,000+ | GitHub |
| Confirmed Pine Script Etsy sales | Active listings found (scalping indicators, $15–$50) | Etsy |
| Paid quant signal subscriptions | $10–$200/month (Substack/Patreon) | Multiple |
| HaasScript / HaasOnline | Developer-grade crypto scripting — paid platform | HaasOnline |

---

## Product #C1 — CLAUDE.md Pack for Trading Bot Developers

**What is it:**
A CLAUDE.md (+ .cursorrules + AGENTS.md) specifically for developers building crypto trading bots in Python.

**Why this is BiG's strongest crypto product:**
- He has ALREADY written a CLAUDE.md for trade-auto
- He already knows the gotchas: exchange API rate limits, floating point errors in financial math, backtesting lookahead bias
- Zero competition confirmed — searched "crypto CLAUDE.md" and "trading bot CLAUDE.md" → zero results

**What goes in it:**
```markdown
## Gotchas (these will cost you real money if wrong)
- NEVER use float for price/quantity — use Decimal with precision=8
- Binance rate limit: 1200 requests/min weight — always check x-mbx-used-weight header
- Backtesting lookahead bias: indicators must use shift(1), never current candle close
- Order fills are NOT guaranteed at limit price — always use slippage buffer
- Exchange timestamps are in milliseconds, not seconds — always divide by 1000
- Paper trading results ≠ live results — slippage and partial fills matter

## Strategy Code Rules
- populate_indicators() must be pure — no side effects, no API calls
- Separate signal generation from order execution — never mix
- All strategies must implement: entry signal, exit signal, stop loss, position sizing
- Risk per trade: max 1–2% of portfolio — hardcode as constant, never magic number

## Testing Rules
- Backtest requires: in-sample period + out-of-sample validation (never test on same data)
- Synthetic tests for: trending up, trending down, ranging, flash crash scenarios
- Never commit a strategy without backtest Sharpe > 1.0 on out-of-sample data
```

**Platforms:** Gumroad (developer audience) + include in 5-tool AI Config Bundle

| Factor | Score | Notes |
|---|---|---|
| Market demand | 8/10 | Growing quant dev community; Python crypto dev = large segment |
| Competition | 10/10 | Zero paid crypto CLAUDE.md products found |
| BiG's moat | 10/10 | Building this RIGHT NOW — maximum authenticity |
| Build effort | Near-zero | Extract + clean existing trade-auto CLAUDE.md |
| Price ceiling | $19–$37 | Add-on to main Config Pack or standalone |
| Bundle synergy | Very High | Natural upsell from main Config Pack |

**Feasibility: GREEN — ship this week alongside main Config Pack. 2 hours work.**

---

## Product #C2 — Python Trading Bot Backtest Report Template

**What is it:**
A professional Notion + Google Sheets template for presenting backtest results clearly.
The "scientist's lab report" for trading strategies.

**What it includes:**
- Strategy hypothesis + rationale section
- Backtest parameters table (date range, initial capital, fee rate, slippage)
- Key metrics dashboard: Sharpe ratio, Sortino ratio, max drawdown, win rate, profit factor
- Equity curve chart template (Google Sheets with formulas)
- Monthly returns heatmap (like hedge fund reports)
- In-sample vs out-of-sample comparison table
- Checklist: 12 signs your backtest is curve-fitted (lookahead bias checklist)

**Why this sells:**
- Every developer building a trading bot eventually needs to present their results
- "Does this strategy actually work?" is the hardest question to answer properly
- Professional-looking reports make you take your own work seriously — and show it to others
- BiG needs this exact document for his own trade-auto project

**Market signal:**
- FreqST.com = marketplace for Freqtrade strategies — sellers need professional presentations
- Patreon quant signal sellers charge $200/month — they need credibility artifacts
- Zero professional backtest report templates found as a paid product

| Factor | Score | Notes |
|---|---|---|
| Market demand | 7/10 | Every quant dev needs this; not many know they can buy it |
| Competition | 9/10 | Near-zero professional backtest report templates |
| BiG's moat | 9/10 | BiG is building this for himself — dogfood product |
| Build effort | Low-Medium (1–2 days) | Notion + Google Sheets templates |
| Price ceiling | $19–$37 | Spreadsheet + Notion template tier |

**Feasibility: GREEN — BiG builds this for his own use, then sells it. Pure dogfood product.**

---

## Product #C3 — Pine Script Indicator Pack (TradingView)

**What is it:**
A pack of 5–10 Pine Script v6 indicators for crypto traders on TradingView.
Focus: the exact signals BiG is implementing in Python (RSI + BB, EMA crossover, MACD).

**Why Pine Script:**
- 150,000+ community scripts published — market is huge
- Confirmed active Etsy sales: "TradingView Scalping Indicator: Buy/Sell Signals, Non-repainting Pine Script" — actual listing found
- Pine Script v6 released — "v6" keyword in listings = modern positioning
- Paid indicator subscriptions go up to $200/month on TradingView itself
- BiG already implemented these signals in Python → trivial to port to Pine Script

**What the pack includes:**
- RSI + Bollinger Band confluence indicator (Mean Reversion signal)
- EMA crossover with MACD confirmation (Momentum signal)
- Grid level visualizer (shows grid trading zones on chart)
- Volume-weighted signal filter (reduces false signals)
- Multi-timeframe trend confirmation overlay
- Each indicator: non-repainting, with alerts, clean visual design

**Platforms:** Etsy (confirmed sales), Gumroad, TradingView protected scripts (subscription model)

**Key differentiator:** "Built by a developer who is running these same signals in a live Python bot" — authenticity that TradingView influencer accounts can't match

| Factor | Score | Notes |
|---|---|---|
| Market demand | 9/10 | Massive TradingView community; Etsy sales confirmed |
| Competition | 5/10 | 150K+ free scripts exist; non-repainting + quality = moat |
| BiG's moat | 8/10 | Same signals as Python bot = unique cross-validation story |
| Build effort | Medium (2–3 days) | Learn Pine Script v6, port existing signal logic |
| Price ceiling | $19–$49 (one-time) or $15–$29/mo subscription | |
| Revenue model | One-time Etsy/Gumroad OR recurring TradingView subscription | |

**Feasibility: YELLOW-GREEN — Phase 2. Requires Pine Script learning (1–2 days). High demand confirmed.**

---

## Product #C4 — Freqtrade Strategy Pack + Backtest Data

**What is it:**
3 production-ready Freqtrade strategies (Python) with documented backtest results.
The same 3 strategies BiG is building for trade-auto.

**Market signal:**
- FreqST.com = active marketplace for Freqtrade strategies
- Patreon seller "Quant Tactics" sells Freqtrade strategy walkthroughs
- Freqtrade has 30,000+ GitHub stars and a paying community
- "Strategy with documented Sharpe > 1.0 on out-of-sample data" = high credibility signal
- Free strategies on GitHub exist but lack: documentation, backtest reports, risk management

**What makes BiG's pack different from free GitHub strategies:**
- Real backtest results on BTC/ETH data (not synthetic)
- Includes the backtest report template (from #C2) showing methodology
- Written by someone who actually ran these strategies (when trade-auto Phase 2 completes)
- CLAUDE.md included: how to ask Claude Code to modify/extend each strategy safely
- Risk management parameters documented: position sizing, stop loss logic, max drawdown rules

**Important note:** Only sell strategies AFTER running live/paper trading (Phase 2 of trade-auto). Selling untested strategies = liability. Wait for real data.

| Factor | Score | Notes |
|---|---|---|
| Market demand | 8/10 | Active Freqtrade community, confirmed marketplace |
| Competition | 6/10 | Free strategies exist; quality + documentation = moat |
| BiG's moat | 9/10 | Real backtest data + live trade experience |
| Build effort | Low (documentation only — code already exists) | |
| Price ceiling | $37–$79 | Strategies with proven backtest data |
| Timing | Phase 3 — after live trading data collected | |

**Feasibility: YELLOW-GREEN — Phase 3. Can't ship until trade-auto Phase 2 completes. But the content builds itself as BiG works on trade-auto.**

---

## Product #C5 — Crypto Portfolio Tracker (Google Sheets)

**What is it:**
A Google Sheets tracker for multi-exchange crypto portfolios.
Automated formulas, not manual entry.

**What it tracks:**
- Holdings across Binance, Bybit, OKX (manual entry per exchange, automated math)
- Cost basis and average buy price per coin (DCA calculator)
- Unrealized PnL in USD and % (live price formula via GOOGLEFINANCE or IMPORTDATA)
- Portfolio allocation pie chart (auto-updated)
- Monthly PnL summary tab
- Bot performance tab: track paper/live bot trades from trade-auto
- Thai Baht column (BiG is based in Bangkok — THB conversion built in)

**Market signal:**
- "Budget tracker with automated formulas outsells a cute PDF every time" — confirmed buyer preference
- Google Sheets trackers: $15–$29 price point, proven seller category
- "Indie hacker financial tracking is an underserved niche" — from v2 research
- Crypto-specific tracker with bot performance tab = unique angle

**Differentiation from free CoinGecko/CoinMarketCap portfolio tools:**
- Works offline, fully owned
- Tracks bot performance alongside manual holdings
- DCA cost basis calculation (most free tools don't do this correctly)
- Customizable for any exchange/coin pair

| Factor | Score | Notes |
|---|---|---|
| Market demand | 7/10 | Every crypto holder tracks portfolio; free tools exist |
| Competition | 6/10 | Many generic trackers; bot performance tab = unique |
| BiG's moat | 8/10 | Builds this anyway for trade-auto tracking |
| Build effort | Low (1 day) | Google Sheets + documentation |
| Price ceiling | $15–$29 | Spreadsheet category norm |
| THB angle | Bonus | Thai crypto traders = underserved niche |

**Feasibility: YELLOW-GREEN — Phase 2. Low effort, dogfood product, Thai market angle is bonus.**

---

## Product #C6 — Trading Bot Risk Management Checklist

**What is it:**
A Notion checklist + PDF guide: the 25 things to verify before going live with a trading bot.
The "pre-flight checklist" for automated trading.

**What it covers:**

**Financial safety:**
- [ ] Position sizing: max 1–2% portfolio risk per trade
- [ ] Daily drawdown circuit breaker: auto-pause if portfolio drops >5% in 24h
- [ ] Max concurrent open positions cap
- [ ] Emergency kill switch: single command to cancel all orders and close positions

**Technical safety:**
- [ ] Exchange rate limit handling (exponential backoff on 429 errors)
- [ ] Network disconnect handling (what happens if bot loses connection mid-order?)
- [ ] Duplicate order prevention (idempotency keys on order submission)
- [ ] Decimal precision: using Decimal, not float, for all financial math

**Backtest validity:**
- [ ] Out-of-sample test on data NOT used for optimization
- [ ] Slippage model included (0.1–0.5% realistic for crypto)
- [ ] Transaction fees included in backtest
- [ ] Lookahead bias check: no future data used in signals

**Operational:**
- [ ] Alerts configured: Telegram/Discord on trade execution + errors
- [ ] Logging: every order, every signal, every error logged with timestamps
- [ ] Monitoring: uptime checks, Grafana/simple dashboard

**Market signal:**
- Zero paid trading bot safety checklists found
- "Don't let Claude delete my database" = same safety anxiety exists in trading ("don't let my bot blow my account")
- Risk management is the #1 thing new quant developers get wrong

| Factor | Score | Notes |
|---|---|---|
| Market demand | 7/10 | Every trading bot developer needs this |
| Competition | 9/10 | Near-zero paid safety checklists |
| BiG's moat | 9/10 | Building trade-auto = knows every failure mode |
| Build effort | Very Low (half a day) | Document checklist BiG already uses mentally |
| Price ceiling | $15–$29 | Checklist + guide category |
| Bundle synergy | Very High | Bundle with CLAUDE.md pack (#C1) and Backtest Template (#C2) |

**Feasibility: GREEN — easiest crypto product to build. Write the checklist BiG uses for trade-auto, sell it.**

---

## Product #C7 — Crypto n8n Automation Workflow Pack

**What is it:**
Developer-specific n8n workflows for crypto traders and bot builders.
NOT generic price alerts — these are for people running their own bots.

**Workflows included:**
- Binance order fill → Telegram notification with trade details + PnL
- Bot drawdown alert: daily portfolio check → if >5% down → pause bot + alert
- Weekly strategy performance report → auto-generate from trade history → Notion log
- TradingView webhook → trigger Freqtrade strategy manually
- Exchange API error → auto-retry with backoff + Slack alert if fails 3 times
- New Gumroad sale alert → log in Google Sheets (for when BiG sells his own products!)
- Crypto tax event logger: every trade → tagged log for annual tax filing

**Market signal:**
- n8n AI Agent Workflow Blueprint (JSON) actively selling on Gumroad: limitlessai.gumroad.com
- Developer-niche n8n pack already identified as YELLOW-GREEN from #14 research
- Crypto-specific = narrower than generic "developer n8n" → even less competition
- "Bot performance monitoring" workflow = unique, not found in n8n community library

| Factor | Score | Notes |
|---|---|---|
| Market demand | 6/10 | Narrower niche than developer n8n generally |
| Competition | 8/10 | Very few crypto-specific n8n packs |
| BiG's moat | 8/10 | Builds these workflows for trade-auto anyway |
| Build effort | Low (1 day) | JSON exports + documentation |
| Price ceiling | $29–$49 | Niche workflow pack |
| Bundle synergy | Bundle with Freqtrade pack (#C4) | |

**Feasibility: YELLOW-GREEN — Phase 2. Bundle with Freqtrade Strategy Pack.**

---

## Product #C8 — Dune Analytics SQL Query Pack (On-Chain Intel)

**What is it:**
Pre-written Dune Analytics SQL queries for monitoring on-chain market intelligence.
Queries that give trading signal context — not just charts, but actionable data.

**Query pack contents:**
- DEX volume vs CEX volume ratio (high DEX = retail risk-on signal)
- Exchange net flow (BTC inflows to exchanges = sell pressure incoming)
- Stablecoin supply growth rate (new USDC/USDT minting = buying power incoming)
- Whale wallet accumulation tracker (wallets >1000 BTC adding/removing)
- Funding rate vs open interest correlation (overheated futures market signal)
- Fear & Greed on-chain proxy (computed from on-chain metrics, not survey)

**Market signal:**
- Dune has 100+ blockchains, active community, free tier available
- "As of 2026: tighter integration between AI and on-chain analytics" — blog.sablier.com
- Zero paid Dune SQL query packs found on Gumroad
- On-chain data is the "alpha" that separates quant traders from chart watchers
- BiG's trade-auto COULD use these signals as inputs — natural product-to-project synergy

**Consideration:** Requires DeFi/on-chain knowledge. BiG's background is more CEX/Python. Medium fit.

| Factor | Score | Notes |
|---|---|---|
| Market demand | 7/10 | On-chain analytics growing fast |
| Competition | 8/10 | Free Dune community queries exist; curated pack = gap |
| BiG's moat | 5/10 | Less direct — needs Dune SQL learning |
| Build effort | Medium-High (3–4 days) | Dune SQL is distinct skill |
| Price ceiling | $29–$49 | SQL query template category |

**Feasibility: YELLOW — Phase 3. Lower BiG fit than others. Only pursue if on-chain work interests BiG.**

---

## Product #C9 — Crypto Trading Strategy CLAUDE.md for Claude Code + Cursor

**What is it:**
A specialized CLAUDE.md for when you ask Claude to ANALYZE or IMPROVE trading strategies — not build the bot, but reason about strategy logic.

**This is different from #C1 (which is for building the bot):**
- #C1 = "Help me write clean Python trading bot code"
- #C9 = "Help me think through whether this strategy has edge"

**What it includes:**
```markdown
## Strategy Analysis Mode
When reviewing a trading strategy, always check for:
1. Lookahead bias: does the signal use future data?
2. Overfitting: are there too many parameters vs. data points?
3. Transaction cost sensitivity: does it survive 0.1% fees per trade?
4. Market regime dependency: does it only work in trending/ranging markets?
5. Correlation to BTC: does it have independent alpha or is it just leveraged BTC?

## When backtesting code:
- Walk-forward validation > simple train/test split
- Minimum 2 years data for daily strategies; 3 months for hourly
- Out-of-sample period = last 20% of data, never touched during development

## Red flags to always call out:
- Sharpe > 3 on daily data = almost certainly overfitted
- Win rate > 70% with small average win = martingale-style risk
- Strategy that works on BTC but not ETH/SOL = market-specific, not edge
```

**Why this is valuable:**
"Help me review my strategy" is a VERY common ask — Claude gives generic responses without this context
With this CLAUDE.md, Claude becomes a proper quant reviewer, not a yes-man

| Factor | Score | Notes |
|---|---|---|
| Market demand | 7/10 | Every quant dev reviews strategies |
| Competition | 10/10 | Zero paid "strategy review CLAUDE.md" found |
| BiG's moat | 9/10 | BiG is literally applying these exact checks in trade-auto |
| Build effort | Very Low (half a day) | Encode existing mental checklist |
| Bundle synergy | Very High | Natural bundle with #C1 as "Trading Bot Dev Bundle" |

**Feasibility: GREEN — trivial to build, strong bundle with #C1. Package as "Trading Bot Developer Bundle".**

---

## Product #C10 — "From Backtest to Live Bot" Guide (PDF/Notion)

**What is it:**
A step-by-step guide covering the full journey from strategy idea to live trading.
Not a course — a reference guide with checklists, templates, and code patterns.

**Chapters:**
1. Strategy hypothesis: how to state a testable edge
2. Data sourcing: Binance public API, data cleaning, OHLCV quality checks
3. Backtesting with Freqtrade: setup, configuration, running
4. Reading backtest results: which metrics matter, which lie
5. Paper trading: Binance testnet setup, what to watch for
6. Going live: position sizing, circuit breakers, monitoring
7. Iteration loop: how to improve a strategy without overfitting
8. CLAUDE.md prompts for each phase (using Claude Code to assist at each step)

**Market signal:**
- "ChatGPT Crypto Trading Mastery" at $50 with 328 ratings = top paid AI+crypto product on Gumroad
- That product is generic; this is Python + Freqtrade + real data specific
- BiG IS going through this exact journey with trade-auto — write the guide AS he does it
- "Write the guide as you go" = zero extra research needed, just document the work

**Pricing:** $37–$49. Longer/more valuable than single templates.

| Factor | Score | Notes |
|---|---|---|
| Market demand | 8/10 | "ChatGPT Crypto Trading Mastery" proves buyers exist |
| Competition | 7/10 | Generic guides exist; Python + Freqtrade specific = gap |
| BiG's moat | 10/10 | Literally living this journey right now |
| Build effort | Medium (ongoing — write as you go) | |
| Price ceiling | $37–$49 | Comprehensive guide format |
| Timing | Phase 2-3 — after paper trading completes | |

**Feasibility: YELLOW-GREEN — write the guide as BiG completes trade-auto Phases 2–3. Zero extra research.**

---

## Summary — All 10 Crypto Products Ranked

| Rank | Product | Market Demand | Competition | BiG's Moat | Build Effort | Phase | Feasibility |
|---|---|---|---|---|---|---|---|
| **#C1** | CLAUDE.md Pack for Trading Bot Devs | 8/10 | 10/10 | 10/10 | Near-zero | **Now** | **GREEN** |
| **#C6** | Trading Bot Risk Management Checklist | 7/10 | 9/10 | 9/10 | Very Low | **Now** | **GREEN** |
| **#C9** | Strategy Analysis CLAUDE.md | 7/10 | 10/10 | 9/10 | Very Low | **Now** | **GREEN** |
| **#C2** | Backtest Report Template | 7/10 | 9/10 | 9/10 | Low | Phase 2 | **GREEN** |
| **#C5** | Crypto Portfolio Tracker (Google Sheets) | 7/10 | 6/10 | 8/10 | Low | Phase 2 | **YELLOW-GREEN** |
| **#C3** | Pine Script Indicator Pack | 9/10 | 5/10 | 8/10 | Medium | Phase 2 | **YELLOW-GREEN** |
| **#C7** | Crypto n8n Automation Pack | 6/10 | 8/10 | 8/10 | Low | Phase 2 | **YELLOW-GREEN** |
| **#C10** | From Backtest to Live Bot Guide | 8/10 | 7/10 | 10/10 | Medium (ongoing) | Phase 3 | **YELLOW-GREEN** |
| **#C4** | Freqtrade Strategy Pack | 8/10 | 6/10 | 9/10 | Low (docs only) | Phase 3 | **YELLOW-GREEN** |
| **#C8** | Dune Analytics SQL Query Pack | 7/10 | 8/10 | 5/10 | Medium-High | Phase 3 | **YELLOW** |

---

## Bundle Strategy — "Trading Bot Developer Bundle"

3 GREEN products ship together as one bundle for $37–$49:

```
Trading Bot Developer Bundle ($37)
├── #C1 — CLAUDE.md + .cursorrules for trading bot development
│         (Python, ccxt/Binance, Freqtrade stack)
├── #C6 — Pre-live checklist: 25 things to verify before going live
└── #C9 — Strategy Analysis CLAUDE.md
          (how Claude should review strategy edge, bias, overfitting)
```

This bundle costs BiG ~2 hours total to build (all three come from documenting existing trade-auto work) and sells to the same buyer: a developer building their first crypto trading bot.

**Gumroad launch post:** r/algotrading + r/freqtrade + r/learnpython

---

## Key Insight: The "Build Once, Sell Twice" Loop

BiG's trade-auto project is both a product AND a content factory:

```
trade-auto project work →  document it → sell the documentation

Phase 1 (backtesting)   → #C2 Backtest Report Template
                        → #C6 Risk Management Checklist
                        → #C1 Trading Bot CLAUDE.md
                        → #C9 Strategy Analysis CLAUDE.md

Phase 2 (paper trading) → #C5 Portfolio Tracker
                        → #C7 n8n Automation Pack
                        → #C3 Pine Script (port Python signals)

Phase 3 (live trading)  → #C4 Freqtrade Strategy Pack
                        → #C10 "From Backtest to Live Bot" Guide
```

Every hour spent on trade-auto produces sellable documentation.
The guide (#C10) written at the END is the highest-value product because it covers the whole journey.

---

*Sources: StreetInsider (AI trading bot market $54B), crypto.news (leading bots 2026), tradingview.com (150K+ scripts), etsy.com (Pine Script active listings), freqst.com (Freqtrade marketplace), patreon.com/quanttactics, bingx.com (160K Grid Bot users), coinbureau.com (AI trading bots review), dune.com, blog.sablier.com (on-chain analytics 2026)*
