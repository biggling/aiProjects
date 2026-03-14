"""Scheduler entrypoint — registers all cron jobs with APScheduler."""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dotenv import load_dotenv
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from loguru import logger

from scheduler import jobs

load_dotenv()

TIMEZONE = "Asia/Bangkok"


def create_scheduler(dry_run: bool = False) -> BlockingScheduler:
    """Create and configure the scheduler with all jobs."""
    scheduler = BlockingScheduler(timezone=TIMEZONE)
    jobs.DRY_RUN = dry_run

    # Daily jobs
    schedule = [
        ("run_research",    jobs.run_research,    {"hour": 6, "minute": 0}),
        ("run_strategy",    jobs.run_strategy,    {"hour": 7, "minute": 0}),
        ("run_scriptgen",   jobs.run_scriptgen,   {"hour": 7, "minute": 30}),
        ("run_voiceover",   jobs.run_voiceover,   {"hour": 8, "minute": 0}),
        ("run_videogen",    jobs.run_videogen,    {"hour": 9, "minute": 0}),
        ("run_editor",      jobs.run_editor,      {"hour": 10, "minute": 30}),
        ("publish_slot_1",  jobs.publish_slot,    {"hour": 12, "minute": 0}),
        ("run_crosspost",   jobs.run_crosspost,   {"hour": 15, "minute": 30}),
        ("publish_slot_2",  jobs.publish_slot,    {"hour": 18, "minute": 0}),
        ("run_analytics",   jobs.run_analytics,   {"hour": 21, "minute": 0}),
    ]

    for name, func, time_kwargs in schedule:
        scheduler.add_job(
            func,
            trigger=CronTrigger(**time_kwargs, timezone=TIMEZONE),
            id=name,
            name=name,
            replace_existing=True,
        )
        logger.info(f"Registered job: {name} at {time_kwargs}")

    # Weekly job (Friday)
    scheduler.add_job(
        jobs.run_weekly_score,
        trigger=CronTrigger(day_of_week="fri", hour=21, minute=0, timezone=TIMEZONE),
        id="run_weekly_score",
        name="run_weekly_score",
        replace_existing=True,
    )
    logger.info("Registered job: run_weekly_score at Friday 21:00")

    return scheduler


def main():
    parser = argparse.ArgumentParser(description="TikTok Automation Scheduler")
    parser.add_argument("--dry-run", action="store_true", help="Run without actual API calls")
    args = parser.parse_args()

    mode = "DRY RUN" if args.dry_run else "LIVE"
    logger.info(f"Starting scheduler in {mode} mode")

    scheduler = create_scheduler(dry_run=args.dry_run)

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Scheduler stopped")


if __name__ == "__main__":
    main()
