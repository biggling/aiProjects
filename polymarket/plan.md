# Polymarket Bot — Implementation Plan

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
