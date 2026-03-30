from datetime import datetime, timezone
from celery_app import app
from tools.shared.db import get_session
from tools.shared.models import TaskLog
from tools.shared.notify import notify
from tools.shared.logger import get_logger

logger = get_logger("tasks")


def _run_with_logging(task_name: str, func):
    """Wrapper: log start/end to TaskLog, notify on failure."""
    with get_session() as session:
        log_entry = TaskLog(
            task_name=task_name,
            status="running",
            started_at=datetime.now(timezone.utc),
        )
        session.add(log_entry)
        session.flush()
        log_id = log_entry.id

    try:
        result = func()
        with get_session() as session:
            entry = session.get(TaskLog, log_id)
            entry.status = "done"
            entry.finished_at = datetime.now(timezone.utc)
            entry.result_summary = str(result)[:500] if result else None
        logger.info(f"{task_name} completed")
        return result
    except Exception as e:
        with get_session() as session:
            entry = session.get(TaskLog, log_id)
            entry.status = "failed"
            entry.finished_at = datetime.now(timezone.utc)
            entry.error = str(e)[:1000]
        logger.error(f"{task_name} failed: {e}")
        notify(f"Task failed: {task_name}", str(e), level="failure")
        raise


# ── Phase 1: Trend Research ──────────────────────────────

@app.task(name="tasks.run_trend_scraper")
def run_trend_scraper():
    def _do():
        from tools.trend.trend_scraper import run
        return run()
    return _run_with_logging("trend_scraper", _do)


@app.task(name="tasks.run_gemini_trend_scraper")
def run_gemini_trend_scraper():
    """Fetch current + upcoming trends from Gemini, save snapshots to DB."""
    def _do():
        from tools.trend.gemini_trend_scraper import run
        return run()
    return _run_with_logging("gemini_trend_scraper", _do)


@app.task(name="tasks.run_blue_ocean_scraper")
def run_blue_ocean_scraper():
    """Discover low-competition blue ocean niches across all horizons (biweekly)."""
    def _do():
        from tools.trend.blue_ocean_scraper import run
        return run()
    return _run_with_logging("blue_ocean_scraper", _do)


@app.task(name="tasks.run_reddit_scraper")
def run_reddit_scraper():
    def _do():
        from tools.trend.reddit_scraper import run
        return run()
    return _run_with_logging("reddit_scraper", _do)


@app.task(name="tasks.run_etsy_scraper")
def run_etsy_scraper():
    def _do():
        from tools.trend.etsy_scraper import run
        return run()
    return _run_with_logging("etsy_scraper", _do)


@app.task(name="tasks.run_niche_scorer")
def run_niche_scorer():
    def _do():
        from tools.trend.niche_scorer import run
        return run()
    return _run_with_logging("niche_scorer", _do)


# ── Phase 2: Design Pipeline ────────────────────────────

@app.task(name="tasks.run_prompt_gen")
def run_prompt_gen():
    def _do():
        from tools.design.prompt_generator import run
        return run()
    return _run_with_logging("prompt_gen", _do)


@app.task(name="tasks.run_image_gen")
def run_image_gen():
    def _do():
        from tools.design.image_generator import run
        return run()
    return _run_with_logging("image_gen", _do)


@app.task(name="tasks.run_image_processor")
def run_image_processor():
    def _do():
        from tools.design.image_processor import run
        return run()
    return _run_with_logging("image_processor", _do)


@app.task(name="tasks.run_clip_filter")
def run_clip_filter():
    def _do():
        from tools.design.clip_filter import run
        return run()
    return _run_with_logging("clip_filter", _do)


@app.task(name="tasks.run_mockup_gen")
def run_mockup_gen():
    def _do():
        from tools.design.mockup_generator import run
        return run()
    return _run_with_logging("mockup_gen", _do)


# ── Phase 3: Copywriting ────────────────────────────────

@app.task(name="tasks.run_copy_gen")
def run_copy_gen():
    def _do():
        from tools.copy.copy_generator import run
        return run()
    return _run_with_logging("copy_gen", _do)


@app.task(name="tasks.run_caption_gen")
def run_caption_gen():
    def _do():
        from tools.copy.caption_generator import run
        return run()
    return _run_with_logging("caption_gen", _do)


# ── Phase 4: Upload & Automation ─────────────────────────

@app.task(name="tasks.run_printify_publish")
def run_printify_publish():
    def _do():
        from tools.upload.printify_publisher import run
        return run()
    return _run_with_logging("printify_publish", _do)


@app.task(name="tasks.run_etsy_upload")
def run_etsy_upload():
    def _do():
        from tools.upload.etsy_uploader import run
        return run()
    return _run_with_logging("etsy_upload", _do)


@app.task(name="tasks.run_social_post")
def run_social_post():
    def _do():
        from tools.upload.social_poster import run
        return run()
    return _run_with_logging("social_post", _do)


@app.task(name="tasks.run_price_check")
def run_price_check():
    def _do():
        from tools.upload.price_adjuster import run
        return run()
    return _run_with_logging("price_check", _do)


# ── Phase 5: Analytics ───────────────────────────────────

@app.task(name="tasks.run_analytics_pull")
def run_analytics_pull():
    def _do():
        from tools.analytics.analytics_puller import run
        return run()
    return _run_with_logging("analytics_pull", _do)


@app.task(name="tasks.run_performance_flag")
def run_performance_flag():
    def _do():
        from tools.analytics.performance_flagger import run
        return run()
    return _run_with_logging("performance_flag", _do)


@app.task(name="tasks.run_weekly_report")
def run_weekly_report():
    def _do():
        from tools.analytics.weekly_report import run
        return run()
    return _run_with_logging("weekly_report", _do)


# ── Maintenance ──────────────────────────────────────────

@app.task(name="tasks.run_backup")
def run_backup():
    import subprocess
    def _do():
        subprocess.run(["bash", "backup.sh"], check=True)
        return "backup completed"
    return _run_with_logging("backup", _do)
