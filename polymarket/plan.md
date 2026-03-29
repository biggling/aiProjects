# Polymarket Bot — Implementation Plan

## Phase 0: Deep Market Research & Target Strategy (DO FIRST)

**Goal:** Validate prediction market trading viability and define exact strategy focus before building the bot.

### Market Sizing & Validation
- [ ] Research Polymarket ecosystem:
  - Total daily trading volume (verify from Polymarket public data or Dune dashboards)
  - Number of active traders (unique wallets per day/week)
  - Average trade size and frequency per active trader
  - Liquidity depth: can a small trader ($100-$500) execute without moving price?
- [ ] Research prediction market profitability:
  - What % of Polymarket traders are profitable? (any public data or research papers?)
  - What strategies do profitable traders use? (arbitrage? news trading? market making?)
  - Is there academic research on prediction market efficiency? (check SSRN, arXiv)
- [ ] Analyze Polymarket fee structure:
  - Trading fees, withdrawal fees, gas fees
  - Net impact on small-capital strategies ($100-$500)
  - Minimum profitable trade size after fees
- [ ] Research automated Polymarket trading:
  - Are other bots active? (check on-chain data for bot-like trading patterns)
  - What edge can a small bot have vs institutional market makers?
  - Legal/regulatory considerations for automated prediction market trading

### Laser-Targeted Strategy Persona (BiG as Trader)
- [ ] **This project's customer is BiG himself** — define trading profile:
  - Capital allocation: how much to risk on Polymarket? ($100? $500?)
  - Time horizon: short-term (hours/days) or long-term (weeks/months)?
  - Risk tolerance: max acceptable loss before stopping
  - Information edge: what does BiG know better than the market? (Thai politics? tech? crypto?)
  - Time commitment: how much monitoring time is acceptable per day?
- [ ] **If productizing later — "Data Trader Dave" persona:**
  - Semi-technical trader who wants signals, not a full bot
  - Willing to pay $29-$99/month for prediction market analytics/signals
  - Currently uses: manually checking Polymarket, reading news
  - What they need: mispricing alerts, probability tracking, event correlation

### Strategy Research
- [ ] Research mispricing detection:
  - How often do sum-of-outcomes != 100% occur? (arbitrage opportunity frequency)
  - Average mispricing size and duration
  - Can a bot capture these before they close? (latency requirements)
- [ ] Research news event correlation:
  - Do markets react slowly to news? (minutes? hours? days?)
  - What news sources move markets most? (Twitter? mainstream media? on-chain data?)
  - Is there a viable "news front-running" strategy using NLP/sentiment?
- [ ] Research cross-market correlation:
  - Do related markets (e.g., "Will X win?" + "Will X's party win?") misprice relative to each other?
  - Can multi-market arbitrage work at small scale?
- [ ] Study historical Polymarket data:
  - Download historical prices for 100+ resolved markets
  - Analyze: did markets converge to correct outcome? How early? Were there exploitable patterns?

### Research Deliverables
- [ ] 1-page "Strategy Brief": which approach (arbitrage vs news vs mispricing), capital needed, expected returns
- [ ] Market analysis: mispricing frequency, avg size, duration
- [ ] Historical data analysis results
- [ ] Go/no-go decision: is automated Polymarket trading viable at BiG's capital level?

---

## Phase 1: Research & Data Pipeline ← CURRENT
- [x] Document Polymarket API endpoints
- [x] Set up project structure
- [ ] Build market data collector
- [ ] Store market snapshots in SQLite
- [ ] Build initial analysis tools

## Phase 2: Analysis & Signals
- [ ] Historical price analysis
- [ ] Volume spike detection
- [ ] Cross-market correlation analysis
- [ ] Mispricing detection (sum of outcomes != 100%)
- [ ] News event correlation

## Phase 3: Paper Trading
- [ ] Signal generation system
- [ ] Paper trading simulator
- [ ] Track hypothetical P&L
- [ ] Evaluate strategy performance

## Phase 4: Live Trading (requires BiG approval)
- [ ] Polymarket wallet integration
- [ ] Order placement via CLOB API
- [ ] Position management
- [ ] Risk limits and stop losses
- [ ] Real-time monitoring dashboard

## API Documentation

### Gamma API (Market Metadata)
- `GET /markets` — List all markets
- `GET /markets/{id}` — Single market details
- `GET /events` — List events with grouped markets

### CLOB API (Order Book)
- `GET /book` — Order book for a token
- `GET /price` — Current prices
- `GET /trades` — Recent trades

### Key Fields
- `question`: Market question text
- `outcomes`: YES/NO (or multiple)
- `outcomePrices`: Current prices (0.00-1.00)
- `volume`: Total volume traded
- `liquidity`: Current liquidity
- `endDate`: Resolution date
