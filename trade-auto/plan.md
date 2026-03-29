# Trade Automation — Implementation Plan

> Automated crypto trading bots in Python. Backtest strategies on historical data, paper trade, then deploy to live exchanges.
> Current status: 3 strategies implemented (Grid, Mean Reversion, Momentum), data downloader built, tests passing.
> Key insight from research: Mean reversion (Sharpe ~2.3) outperforms momentum (~1.0) in current ranging market.

---

## Phase 0: Deep Market Research & Target Customer (DO FIRST)

**Goal:** Validate strategy performance with real data and understand who profits from automated trading in 2026.

### Market Sizing & Validation
- [ ] Research total addressable market for retail crypto trading bots:
  - How many retail traders use automated strategies? (3Commas, Pionex, Bitsgap user counts)
  - What % of crypto trading volume is automated? (estimated 60-80% — verify for retail)
  - Revenue of top bot platforms: 3Commas, Cryptohopper, Pionex, Bitsgap (crunchbase, press releases)
- [ ] Analyze profitability claims: what % of retail bot users are actually profitable?
  - Research r/algotrading loss/win posts — track win/loss ratio in reported results
  - Check 3Commas / Cryptohopper public leaderboards for real performance data
- [ ] Research current BTC market regime in depth:
  - Historical performance of mean reversion vs momentum in similar conditions (2019, 2022 ranging periods)
  - Backtest data from FreqAI / NostalgiaForInfinity public results
- [ ] Map exchange fee structures for BiG's likely trading volume ($100-$1000 capital):
  - Net impact of fees on strategy returns at each capital level
  - Minimum capital needed for each strategy to be net-profitable after fees

### Laser-Targeted Customer Persona (BiG as Target)
- [ ] **This project's customer is BiG himself** — define personal trading profile:
  - Risk tolerance: max acceptable drawdown (5%? 10%? 15%?)
  - Capital allocation: how much to allocate to bot trading vs hold
  - Time commitment: how much monitoring time per day/week is acceptable?
  - Exchange preference: Binance (most liquid) vs Bybit (better UTA) vs MEXC (lowest fees)
  - Tax implications: Thailand 5-year crypto tax holiday covers gains from Thai-licensed exchanges only
  - What does "success" look like? (cover server costs? beer money? meaningful income?)
- [ ] **If productizing later — "Algo Alex" persona:**
  - Semi-technical trader (can run a bot, can't code one)
  - Willing to pay $29-$99/month for a managed bot service
  - Currently uses 3Commas or Pionex — what's their top complaint?
  - Where they hang out: r/algotrading, Crypto Twitter, TradingView community

### Competitor Deep-Dive
- [ ] Test 3Commas free tier — document UX, strategy options, actual performance
- [ ] Test Pionex built-in bots — document grid bot performance on BTC/USDT
- [ ] Research GoCryptoTrader in depth: active development? community size? production-ready?
- [ ] Research Ninjabot: last commit date, features, ease of integration
- [ ] Compare FreqAI (ML-based) vs simple indicator strategies: which has better risk-adjusted returns?
- [ ] Document exact Binance v3 API changes and test migration path
- [ ] Research Binance April 2 changes: RAW_REQUESTS limit, order weight changes — impact on bot

### Strategy Validation Research
- [ ] Download 1 year of BTC/USDT 1h data and analyze:
  - What % of time is market ranging vs trending?
  - Optimal lookback period for mean reversion (current RSI/BB parameters correct?)
  - Correlation between Fear & Greed Index and strategy performance
- [ ] Research optimal Kelly fraction for crypto (academic papers, backtest blogs)
- [ ] Study circuit breaker implementations in production bots (3Commas, Cryptohopper)
- [ ] Research slippage and execution quality on Binance at small order sizes ($10-$50)

### Research Deliverables
- [ ] 1-page "Strategy Brief": which strategy, which exchange, which pairs, what capital, what risk limits
- [ ] Competitor comparison matrix (3Commas vs Pionex vs custom bot)
- [ ] Backtest results on real data with realistic fee/slippage assumptions
- [ ] Go/no-go decision: is automated trading worth the time investment at BiG's capital level?

---

## Tech Stack

| Layer | Tool |
|---|---|
| Language | Python 3.11+ |
| Exchange APIs | Binance v3, Bybit V5, MEXC |
| Data | OHLCV CSV files → SQLite for signals |
| Backtesting | Custom runner (backtests/run_all.py) |
| Logging | loguru → data/logs/ |
| Config | python-dotenv + config.py |
| Future: Framework | GoCryptoTrader or Ninjabot (Go) for low-latency |

---

## Phase 1: Backtest & Strategy Validation ← CURRENT

**Goal:** Run backtests on real data, compare strategies, pick the best performer.

### Tasks
- [x] Create project structure (src/, backtests/, docs/, tests/, data/)
- [x] Implement Grid Trading strategy
- [x] Implement Mean Reversion strategy (RSI + Bollinger Bands)
- [x] Implement Momentum strategy (EMA crossover + MACD)
- [x] Build OHLCV data downloader (Binance public API)
- [x] Build backtest runner with comparison table
- [x] Write tests with synthetic data
- [ ] **CRITICAL: Update Binance API endpoints from v1 to v3** (v1 retired March 25, 2026)
- [ ] **CRITICAL: Replace `!ticker@arr` stream with `<symbol>@ticker`** (retired March 26, 2026)
- [ ] Download real BTC/USDT 1h data (last 6 months)
- [ ] Download real ETH/USDT 1h data (last 6 months)
- [ ] Run backtests on all 3 strategies
- [ ] Add Sharpe ratio, max drawdown, win rate, profit factor metrics
- [ ] Add sortino ratio and calmar ratio
- [ ] Compare results — expect mean reversion to lead
- [ ] Generate backtest report (JSON + terminal summary)

### Deliverable
Backtest results with clear winner strategy. All metrics documented.

---

## Phase 2: Risk Management & Regime Detection

**Goal:** Add adaptive risk management and market regime detection to prevent losses in wrong conditions.

### Tasks
- [ ] Implement regime detection filter (volatility-based):
  - Low volatility → Mean Reversion mode
  - High volatility / trending → Momentum mode
  - Extreme fear (Fear & Greed < 20) → reduce position size to 0.25x Kelly
- [ ] Implement fractional Kelly criterion position sizing (0.25x default)
- [ ] Implement the 1% rule: max 1% of equity per trade
- [ ] Implement ATR-based dynamic stop-loss (not fixed %)
- [ ] Implement staggered exits: 25% at 2x target, 25% at 5x target
- [ ] Add circuit breakers:
  - Max daily loss: 3% of portfolio → halt trading for 24h
  - Max drawdown: 15% → halt all trading, alert BiG
  - Max consecutive losses: 5 → reduce position size 50%
- [ ] Implement 2:1 reward-to-risk ratio (outperforms 3:1 in 2026 per research)
- [ ] Add multi-timeframe signal aggregation (0.6 threshold — reduces false signals 40%)
- [ ] Backtest risk management overlay on winning strategy
- [ ] Write tests for all risk management rules

### Deliverable
Strategy + risk management running in backtest with improved risk-adjusted returns.

---

## Phase 3: Paper Trading (Binance Testnet)

**Goal:** Run winning strategy on Binance testnet for 2 weeks minimum before any real money.

### Tasks
- [ ] Set up Binance testnet API credentials
- [ ] Implement live data feed via WebSocket (`<symbol>@kline_1h`)
- [ ] Implement order placement (testnet): market and limit orders
- [ ] Implement position tracking and P&L calculation
- [ ] Add logging: every signal, order, fill, and P&L update
- [ ] Run paper trading for 14+ days
- [ ] Track metrics: win rate, avg P&L per trade, max drawdown, Sharpe
- [ ] Implement Telegram notifications for:
  - Trade opened/closed
  - Circuit breaker triggered
  - Daily P&L summary
- [ ] Compare paper results to backtest expectations
- [ ] Write paper trading analysis report

### Deliverable
2+ weeks of paper trading data. Strategy performing within backtest expectations.

---

## Phase 4: Live Trading (Requires BiG Approval)

**Goal:** Deploy to live exchange with real capital. Start small.

### Decisions needed from BiG before starting:
- [ ] Exchange choice (Binance recommended — cheapest with BNB, best API)
- [ ] Starting capital ($100-$500 recommended for initial validation)
- [ ] Risk tolerance confirmation (max 15% drawdown, 1% per trade)

### Tasks
- [ ] Set up live exchange API keys (read + trade, NOT withdraw)
- [ ] Implement live order execution with Binance v3 API
- [ ] Ensure TLS SNI support (mandatory by June 8, 2026)
- [ ] Start with minimum position sizes (0.001 BTC or equivalent)
- [ ] Run for 7 days at minimum size before scaling
- [ ] If profitable after 7 days, scale to target position size
- [ ] Implement daily automated P&L reporting
- [ ] Set up VPS deployment (24/7 uptime required)
- [ ] Add health monitoring and auto-restart on crash

### Deliverable
Live bot running profitably with real capital. Automated monitoring and alerts.

---

## Phase 5: Advanced Strategies & Scaling

**Goal:** Add more strategies and exchanges for diversification.

### Tasks
- [ ] Implement Cash-and-Carry strategy (spot long + futures short, 8-20% APY)
- [ ] Implement Smart DCA (buy size scaled by distance from 200-day MA)
- [ ] Add Bybit V5 API support (Unified Trading Account for better capital efficiency)
- [ ] Add MEXC support (0% maker fees)
- [ ] Evaluate FreqAI integration (CatBoost/Random Forest for regime learning)
- [ ] Implement sector rotation: AI (TAO, FET), RWA (ONDO, LINK), DePIN (AKT, HNT)
- [ ] Consider migration to Go (GoCryptoTrader) for production latency
- [ ] Add portfolio-level risk management across strategies
- [ ] Track and report tax implications (synergy with mcp-apps crypto tax MCP)

### Deliverable
Multiple strategies running across multiple exchanges with portfolio-level risk management.

---

## Key Research Insights Driving This Plan

- **BTC regime**: Ranging $65K-$80K, extreme fear (index 11), institutional floor via ETFs ($100B+)
- **Mean reversion favored**: Sharpe ~2.3 vs momentum ~1.0 in current ranging market
- **Optimal holding window**: 48-120 hours for best risk-adjusted returns
- **Regime detection critical**: Hybrid momentum/mean-reversion with explicit regime switching
- **Binance API breaking changes**: v1 endpoints retired March 25, ticker stream retired March 26
- **Binance April 2 changes**: RAW_REQUESTS limit increases to 300K/5min, order weight changes
- **Fractional Kelly**: 0.25x is consensus for extreme-fear regime
- **2:1 R:R outperforms 3:1**: Validated for 2026 market conditions
- **Multi-timeframe aggregation**: 0.6 threshold reduces false signals by 40%
- **Fee optimization**: Binance 0.075% (with BNB), MEXC 0% maker, Bybit UTA for derivatives

---

## Notes for Claude

- All paths use `pathlib.Path`
- Logging via `loguru` to `data/logs/`
- Config via `python-dotenv` — never hardcode keys
- Commission rate: 0.1% default (0.075% with BNB)
- Initial capital: $10,000 USDT in backtests (configurable)
- Data stored as CSV in `data/ohlcv/`
- Backtest results saved as JSON in `backtests/results/`
- Always validate API response before acting on data
- Never place market orders in live mode without explicit confirmation
- Circuit breakers are non-negotiable — never skip them
