# CLAUDE.md

## Project Purpose
Polymarket prediction market data collector and analysis bot. Track markets, identify mispricing, and (eventually) place automated trades.

## Commands
```bash
# Install dependencies
pip install -r requirements.txt

# Collect current market data
python src/collector.py

# Run analysis
python src/analyzer.py

# Run tests
pytest tests/ -v
```

## Architecture

### Pipeline
```
Collect Market Data → Store in SQLite → Analyze for Mispricing → (Phase 2: Auto-trade)
```

### Polymarket API
- REST: `https://clob.polymarket.com` (CLOB API)
- Gamma API: `https://gamma-api.polymarket.com` (market metadata)
- No auth needed for reading market data

### Key Conventions
- Data stored in SQLite (`data/polymarket.db`)
- All paths use `pathlib.Path`
- Logging via `loguru`
- Config via `.env` + `python-dotenv`
- Rate limit: respect API limits, add delays between requests
