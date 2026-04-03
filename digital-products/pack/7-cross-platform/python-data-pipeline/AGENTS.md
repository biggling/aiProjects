# Agent Instructions — Python Data Pipeline

## allowed_tools
read, write, edit, bash, search

## context_files
- memory-bank/projectBrief.md
- memory-bank/activeContext.md
- memory-bank/progress.md
- memory-bank/systemPatterns.md
- continue.md

## conventions

### File Paths
- Always `pathlib.Path` — never raw strings for file operations
- Create dirs at import: `Path("data/output").mkdir(parents=True, exist_ok=True)`

### Logging
- `loguru` everywhere — never `print()` in module code
- `logger.exception()` inside except blocks to capture traceback

### SQLAlchemy 2.x
- Context manager always: `with SessionLocal() as session:`
- `session.execute(select(Model))` — not legacy `session.query()`
- Never share sessions across threads
- Keep transactions short

### Alembic
- Never edit existing migration files — always create new
- Import all models in env.py

### Celery
- Tasks must be idempotent
- `bind=True` for retry access
- Always set `max_retries` and `default_retry_delay`

### What Not To Do
- No `os.path.join()` — use `pathlib.Path / "subdir"`
- No bare `except:` — always catch specific exceptions
- No global mutable state
- No synchronous HTTP in Celery tasks without timeout

## workflow
1. Read context_files first
2. Run `pytest tests/ -v` after any changes
3. Run `alembic upgrade head` if models changed
4. Update continue.md when done
