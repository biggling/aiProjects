# CLAUDE.md — Python Data Pipeline

## Stack
Python 3.11+, SQLAlchemy 2.x, Alembic, Celery, PostgreSQL, Redis, loguru, python-dotenv.

## Commands
```bash
# Install
pip install -r requirements.txt

# DB migrations
alembic revision --autogenerate -m "description"
alembic upgrade head
alembic downgrade -1

# Run pipeline modules
python -m src.pipeline.collect
python -m src.pipeline.process
python -m src.pipeline.export

# Celery worker + beat
celery -A src.worker.app worker --loglevel=info
celery -A src.worker.app beat --loglevel=info

# Tests
pytest tests/ -v
pytest tests/test_pipeline.py::TestCollector -v

# Type check
mypy src/
```

## Code Conventions

### File Paths
- Always `pathlib.Path` — never raw strings for file operations
- Create output dirs at module import time: `Path("data/output").mkdir(parents=True, exist_ok=True)`
- Use `__file__` to build paths relative to the module: `ROOT = Path(__file__).parent.parent`

### Logging
- `loguru` everywhere: `from loguru import logger`
- `logger.info/warning/error/exception` — never `print()` in module code
- Use `logger.exception()` inside except blocks to capture full traceback
- Configure once at entry point: `logger.add("data/logs/{time}.log", rotation="1 day", serialize=True)`

### Environment / Config
- Load from `.env` via `python-dotenv` at module top-level
- Validate required vars at startup — raise `ValueError` with the var name if missing
- Never hardcode API keys, DB URLs, or secrets

### SQLAlchemy 2.x
- Use `Session` from `sqlalchemy.orm`, not the old `scoped_session`
- Always use context manager: `with SessionLocal() as session:`
- Prefer `session.execute(select(Model))` over legacy `session.query(Model)`
- Never share session objects across threads
- Keep transactions short — commit or rollback before returning
- Define models with `DeclarativeBase`, not the old `Base = declarative_base()`

```python
# Correct
with SessionLocal() as session:
    result = session.execute(select(User).where(User.id == user_id)).scalar_one_or_none()

# Wrong — don't do this
session = SessionLocal()
user = session.query(User).filter_by(id=user_id).first()
```

### Alembic Migrations
- Never edit existing migration files — always create a new one
- Migration filenames describe the change: `add_trend_snapshot_table`
- Import all models in `env.py` so autogenerate detects all changes
- Run `alembic upgrade head` before any test that touches the DB

### Celery Tasks
- Tasks must be idempotent — safe to run twice
- Use `bind=True` for access to `self.retry()`
- Always set `max_retries` and `default_retry_delay`
- Keep tasks small: one unit of work per task
- Use `apply_async(countdown=N)` for delayed retries, not `time.sleep()`

```python
@app.task(bind=True, max_retries=3, default_retry_delay=60)
def process_item(self, item_id: int) -> None:
    try:
        _do_work(item_id)
    except TransientError as e:
        raise self.retry(exc=e)
```

### Project Structure
```
src/
  pipeline/           ← pipeline stage modules (collect, process, export)
  models/             ← SQLAlchemy models
  worker/             ← Celery app and task definitions
  utils/              ← shared helpers, no pipeline logic
  config.py           ← env var loading and validation
data/
  logs/               ← loguru output
  raw/                ← downloaded/collected data
  processed/          ← transformed output
migrations/           ← Alembic migrations
tests/
```

### Error Handling
- Catch specific exceptions — never bare `except:`
- Use `logger.exception("context")` inside except to preserve traceback
- Re-raise if you can't recover: don't silently swallow errors
- For external API calls: catch `requests.exceptions.RequestException`, retry with backoff

### Testing
- Use `pytest` with `pytest-mock` for mocking
- Use `pytest.fixture` for DB sessions: create a test DB, rollback after each test
- Test pipeline stages with sample data in `tests/fixtures/`
- Never make real API calls in tests — mock at the HTTP client level

### What NOT to Do
- No `os.path.join()` — use `pathlib.Path / "subdir"`
- No `print()` in module code — use `logger`
- No bare `except:` or `except Exception:` without re-raising or logging
- No global mutable state outside of the configured singletons (DB engine, Celery app)
- No synchronous HTTP in Celery tasks without timeout — always set `timeout=` on requests

## Checkpointing (Long-Running Pipelines)
- Save progress after each successful batch — never reprocess from scratch on failure
- Write checkpoint to DB or a `data/checkpoints/<run_id>.json` file
- On restart, read checkpoint and skip already-processed records
- Log checkpoint state at INFO level so you can monitor progress remotely

```python
# Checkpoint pattern
def run_pipeline(items: list[Item]) -> None:
    checkpoint = load_checkpoint() or {"last_id": 0}
    for item in items:
        if item.id <= checkpoint["last_id"]:
            continue
        process(item)
        save_checkpoint({"last_id": item.id})
        logger.info("checkpoint saved", last_id=item.id)
```

## Data Validation (Pydantic)
- Define `pydantic.BaseModel` schemas for all external data (API responses, CSV rows, JSON files)
- Validate at the collection stage — fail loud on bad data, don't silently skip
- Use `model_validator(mode='after')` for cross-field validation
- Log validation failures with the raw data for debugging

```python
from pydantic import BaseModel, field_validator

class TrendRecord(BaseModel):
    keyword: str
    volume: int
    date: str

    @field_validator('volume')
    @classmethod
    def volume_must_be_positive(cls, v: int) -> int:
        if v < 0:
            raise ValueError('volume must be non-negative')
        return v
```

## Alerting
- Send a Telegram/Slack alert when a pipeline stage fails after max retries
- Include: stage name, error message, timestamp, and the run ID in the alert
- Alert on data anomalies too: zero rows collected, >50% records invalid, etc.

## Common Mistakes Claude Makes Without This Config
- Using `session.query(Model)` (legacy API) instead of `session.execute(select(Model))`
- Sharing a SQLAlchemy session across threads
- Writing bare `except:` that silently swallows pipeline failures
- Using `os.path.join` instead of `pathlib.Path`
- Celery tasks that aren't idempotent — fail on retry
- Not setting `timeout=` on `requests.get()` — hangs forever on slow APIs
