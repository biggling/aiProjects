# CLAUDE.md

## Project Purpose
Automated crypto trading bots — backtest strategies on historical data, then deploy to live exchanges.

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Download OHLCV data from Binance (no auth needed)
python -m src.data.downloader

# Run all backtests
python backtests/run_all.py

# Run tests
pytest tests/ -v

# Run single strategy test
pytest tests/test_strategies.py::TestMomentumStrategy -v
```

## Architecture

### Pipeline
```
Download Data → Run Backtests → Compare Results → (Phase 2: Paper Trade → Live Trade)
```

### Strategies
- **Grid Trading** (`src/strategies/grid.py`): Range-bound markets, buy/sell at fixed intervals
- **Mean Reversion** (`src/strategies/mean_reversion.py`): RSI + Bollinger Bands, buy oversold / sell overbought
- **Momentum** (`src/strategies/momentum.py`): EMA crossover + MACD confirmation, trend following

### Key Conventions
- Config in `src/utils/config.py` — loads from `.env` via `python-dotenv`
- All paths use `pathlib.Path`
- Logging via `loguru` to `data/logs/`
- Data stored as CSV in `data/ohlcv/`
- Backtest results saved as JSON in `backtests/results/`
- Commission rate: 0.1% per trade (Binance spot default)
- Initial capital: $10,000 USDT (configurable)

### Data Source
Binance public REST API (`/api/v3/klines`) — no API key required for historical data.
