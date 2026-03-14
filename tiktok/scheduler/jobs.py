"""APScheduler job definitions for all automation modules."""

import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from loguru import logger

LOG_DIR = Path("data/logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)
logger.add(LOG_DIR / "scheduler.log", rotation="1 day", retention="7 days", serialize=True)

DRY_RUN = False


def _run_job(name: str, fn, *args, **kwargs):
    """Wrapper to log job execution and catch exceptions."""
    start = datetime.utcnow()
    logger.info(f"Job '{name}' started")
    try:
        result = fn(*args, **kwargs)
        elapsed = (datetime.utcnow() - start).total_seconds()
        logger.info(f"Job '{name}' completed in {elapsed:.1f}s: {result}")
        return result
    except Exception as e:
        elapsed = (datetime.utcnow() - start).total_seconds()
        logger.error(f"Job '{name}' failed after {elapsed:.1f}s: {e}")
        return None


def run_research():
    from modules.01_research.scraper import run_research
    return _run_job("research", run_research)


def run_strategy():
    from modules.01_research.strategy import generate_brief
    return _run_job("strategy", generate_brief)


def run_scriptgen():
    from modules.02_scriptgen.generator import generate_scripts
    return _run_job("scriptgen", generate_scripts)


def run_voiceover():
    from modules.03_voiceover.renderer import render_voiceovers
    return _run_job("voiceover", render_voiceovers)


def run_videogen():
    from modules.04_videogen.orchestrator import generate_videos
    return _run_job("videogen", generate_videos)


def run_editor():
    from modules.05_editor.editor import edit_videos
    return _run_job("editor", edit_videos)


def publish_slot(dry_run: bool = False):
    from modules.06_publisher.scheduler_jobs import publish_next_video
    return _run_job("publish", publish_next_video, dry_run=dry_run or DRY_RUN)


def run_crosspost(dry_run: bool = False):
    from modules.06_publisher.scheduler_jobs import crosspost_recent
    return _run_job("crosspost", crosspost_recent, dry_run=dry_run or DRY_RUN)


def run_analytics():
    from modules.07_analytics.puller import pull_metrics
    return _run_job("analytics", pull_metrics)


def run_weekly_score():
    from modules.07_analytics.scorer import score_videos
    return _run_job("weekly_score", score_videos)
