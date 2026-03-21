# Trade Automation — Session State

## Current Phase
Phase 1: Strategy Research & Backtest — IN PROGRESS

## Last Session
2026-03-22 — Project setup, 3 strategies implemented, tests written

## What Was Done
1. Created full project structure (src/, backtests/, docs/, tests/, data/)
2. Documented 3 trading strategies in docs/strategies.md
3. Implemented Grid Trading strategy (range-bound markets)
4. Implemented Mean Reversion strategy (RSI + Bollinger Bands)
5. Implemented Momentum strategy (EMA crossover + MACD)
6. Built OHLCV data downloader (Binance public API, no auth needed)
7. Built backtest runner with comparison table
8. Written tests with synthetic data (oscillating + trending)
9. Created CLAUDE.md, requirements.txt, .env.example
10. Installed dependencies in venv

## Next Actions (in order)
1. Download real BTC/ETH data: `source venv/bin/activate && python -m src.data.downloader`
2. Run backtests: `python backtests/run_all.py`
3. Analyze results and pick best strategy
4. Add Sharpe ratio and other risk metrics
5. Start Phase 2: paper trading with Binance testnet

## Blockers
_None — data download + backtests ready to run_

## Decisions Needed from BiG
- Which exchange to target for live trading? (Binance, Bybit, OKX?)
- Starting capital range? ($100? $500? $1000?)
- Risk tolerance? (max drawdown acceptable?)

## Notes
- All 3 strategies have tests passing with synthetic data
- Data downloader uses Binance public API (no key needed)
- Grid trading works best in ranging markets
- Mean Reversion best for oversold bounces
- Momentum best for trending markets
- Run all 3 and let data decide
