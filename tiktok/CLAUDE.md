# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common Commands

```bash
# Install Python dependencies
pip install -r requirements.txt

# Install dashboard dependencies
cd dashboard && npm install

# Start both servers in dev mode
bash scripts/dev.sh
# → FastAPI: http://localhost:8000
# → Dashboard: http://localhost:5173

# Run individual pipeline modules manually
python -m modules.01_research.scraper
python -m modules.01_research.strategy --print
python -m modules.02_scriptgen.generator
python -m modules.03_voiceover.renderer
python -m modules.04_videogen.orchestrator
python -m modules.05_editor.editor
python -m modules.07_analytics.report --week current
python -m modules.07_analytics.scorer --approve-interactive

# Start the scheduler (all cron jobs)
python -m scheduler.main
python -m scheduler.main --dry-run   # no actual API publish calls

# Verify all API keys work
python scripts/verify_env.py

# Daily health check
python scripts/daily_health_check.py

# Run tests
pytest tests/
pytest tests/test_research.py -v   # single test file

# Start FastAPI only
uvicorn api.main:app --reload

# Build dashboard for production
cd dashboard && npm run build
```

## Architecture

The system is a linear pipeline where each phase reads from the DB and writes its output for the next phase. Phases run on a cron schedule via APScheduler (`scheduler/main.py`).

**Phase execution order (daily, Asia/Bangkok):**
```
06:00 research → 07:00 strategy → 07:30 scriptgen → 08:00 voiceover →
09:00 videogen → 10:30 editor → 12:00/18:00 publish → 21:00 analytics
```

**Single shared DB session factory** lives in `modules/01_research/db.py`. All other modules import `SessionLocal` and `Base` from there — do not create a second engine. `init_db()` in that file imports all models to trigger table creation; add new models there.

**Module pattern:** every module has `models.py` (SQLAlchemy), a main logic file, and is invokable as `python -m modules.XX_name.entrypoint`. Each orchestrator queries for records without a downstream record (e.g., scripts without a voiceover) to make reruns idempotent.

**API key loading:** always via `python-dotenv` at module top-level. Never pass keys as arguments — read from `os.getenv()`. Copy `.env.example` to `.env` and fill values before running anything.

**File paths:** always `pathlib.Path`, never raw strings. Output directories are created with `mkdir(parents=True, exist_ok=True)` at module import time.

**FastAPI backend** (`api/`) uses `asyncio.to_thread()` for all synchronous SQLAlchemy calls inside async route handlers. `api/ws.py` holds a singleton `ConnectionManager`; import `manager` from there to broadcast events. All routes require `verify_api_key` dependency except the WebSocket.

**React dashboard** (`dashboard/src/`) — all server state via React Query hooks in `api/hooks.ts`. WebSocket events in `hooks/useWebSocket.ts` invalidate React Query keys so components re-render automatically. The axios client in `api/client.ts` reads `VITE_API_KEY` from env for the Bearer token.

**Config files** (`config/settings.yaml`, `config/products.yaml`) are human-edited YAML. The products API router reads/writes `products.yaml` directly — there is no products DB table.

**Logging:** `loguru` everywhere. Logs write to `data/logs/` as structured JSON with daily rotation. Use `logger.info/warning/error` — do not use `print` in module code.

**Fallback data:** research scrapers (`tiktok_trends.py`, `shop_products.py`, `competitor.py`) have `_fallback_*` functions that return dev data when the TikTok API is unavailable. This lets the pipeline run end-to-end without live credentials during development.

**Video generation** (`modules/04_videogen/`) is async by design — Kling/Runway jobs poll for completion. The orchestrator tries Kling first; on any exception it falls back to Runway. Both clients share the same interface: `generate(prompt, duration) → Path`.

**Publisher dry-run:** `scheduler/jobs.py` sets `DRY_RUN = False` at module level. `scheduler/main.py --dry-run` sets it to `True`, which passes through to `publish_next_video(dry_run=True)` and `crosspost_recent(dry_run=True)`.
