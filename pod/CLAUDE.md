# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Purpose

Fully automated Print-on-Demand (POD) business pipeline: discovers trending niches → generates AI designs → writes Etsy copy → publishes to Printify + Etsy → tracks analytics. All orchestrated via Celery Beat on a schedule.

**Current status:** Phases 0–7 complete. Phase 8 (VPS deploy) and Phase 9 integration tests are pending. See `plan.md` for step-by-step implementation history and `dataflow.md` for architecture diagrams.

## Commands

```bash
# Activate virtualenv (always required)
source venv/bin/activate

# Run all tests
pytest tests/ -v --tb=short

# Run a single test file
pytest tests/test_trend_scraper.py -v

# Run a single test by name
pytest tests/test_trend_scraper.py::test_fetch_trends -v

# Run the FastAPI dashboard locally (requires .env)
uvicorn app.main:app --reload --port 8000

# Start Celery worker
celery -A celery_app worker --loglevel=info

# Start Celery Beat scheduler
celery -A celery_app beat --loglevel=info

# Flower monitoring UI (port 5555)
celery -A celery_app flower

# Run a tool manually (all tools expose a run() function)
python -c "from tools.trend.trend_scraper import run; run()"

# Trigger a Celery task manually
python -c "from tasks import run_trend_scraper; run_trend_scraper.delay()"

# DB migrations
alembic revision --autogenerate -m "description"
alembic upgrade head

# Docker (production-like)
docker compose up -d
docker compose ps
docker compose logs -f worker
```

## Architecture

### Pipeline Flow (linear dependency chain)

```
Phase 1 (Trend) → Phase 2 (Design) → Phase 3 (Copy) → Phase 4 (Upload) → Phase 5 (Analytics)
```

Each phase reads from and writes to SQLite (`data/pod.db`). Tools are stateless — they query by `status` field and process pending records.

### Key Conventions

**Every tool exposes a `run()` function** that is called by its corresponding Celery task in `tasks.py`. The `_run_with_logging()` wrapper in `tasks.py` handles `TaskLog` writes and Telegram failure notifications automatically — tool `run()` functions do not need to do this themselves.

**Status fields drive the pipeline.** Each table row's `status` column is the handoff signal between phases:
- `niches`: `active` → `paused` / `killed`
- `designs`: `pending` → `generated` → `processed` → `approved`/`rejected` → `mockup_ready`
- `listings`: `pending` → `copy_ready` → `uploaded` → `live` → `underperforming`

**DB sessions** always use `get_session()` as a context manager (auto-commit/rollback). Never use `SessionLocal()` directly.

**Config** is all in `tools/shared/config.py`. All env vars are optional (no startup crash if unset) except those checked at call time. `SEED_KEYWORDS` list lives here too.

### Module Map

| Directory | Responsibility |
|-----------|---------------|
| `tools/shared/` | DB engine, models, config, logger, notify, API clients |
| `tools/trend/` | Phase 1: pytrends, praw, Playwright scrapers, niche scorer |
| `tools/design/` | Phase 2: Claude prompt gen, Stability AI/DALL-E image gen, rembg + Pillow processor, CLIP filter, Printify mockup |
| `tools/copy/` | Phase 3: Claude listing copy + social caption |
| `tools/upload/` | Phase 4: Printify publish, Etsy upload, order webhook, price check, Buffer social |
| `tools/analytics/` | Phase 5: Etsy stats pull, performance flagging, weekly Claude summary |
| `app/routes/` | FastAPI routers: dashboard, tasks_view, designs, listings, niches, logs, report |
| `tasks.py` | All Celery task definitions (one per tool) |
| `schedule.py` | Celery Beat crontab schedule (19 entries) |
| `celery_app.py` | Celery instance + Beat config wiring |

### Testing Pattern

Tests use `unittest.mock.patch` to mock external APIs. The DB fixture pattern (used throughout) creates real SQLite tables before each test and drops them after:

```python
@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)
```

Tests run against the real SQLite engine (default `sqlite:///data/pod.db` from env). No separate test DB config — the drop-all teardown keeps it clean.

### External APIs Used

| API | Library | Used in |
|-----|---------|---------|
| Google Trends | `pytrends` | trend_scraper |
| Reddit | `praw` | reddit_scraper |
| Etsy pages | `playwright` | etsy_scraper, price_adjuster |
| Claude (Anthropic) | `anthropic` | reddit_scraper, prompt_generator, copy_generator, caption_generator, weekly_report |
| Stability AI / DALL-E | `openai` / `requests` | image_generator |
| CLIP | `transformers` (local) | clip_filter |
| Printify | `requests` | mockup_generator, printify_publisher, order_router |
| Etsy v3 | `requests` | etsy_uploader, analytics_puller |
| Buffer | `requests` | social_poster |
| Apprise | `apprise` | notify.py → Telegram |
