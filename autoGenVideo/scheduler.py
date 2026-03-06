"""APScheduler configuration for autoGenVideo."""
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor
from config import DATABASE_URL, get_logger

logger = get_logger("scheduler")

jobstores = {"default": SQLAlchemyJobStore(url=DATABASE_URL)}
executors = {"default": ThreadPoolExecutor(max_workers=4)}
job_defaults = {"coalesce": True, "max_instances": 1, "misfire_grace_time": 300}

scheduler = BlockingScheduler(
    jobstores=jobstores, executors=executors,
    job_defaults=job_defaults, timezone="UTC",
)


def register_jobs():
    from jobs.job1_content_research import run as job1
    from jobs.job2_script_generation import run as job2
    from jobs.job3_media_assembly import run as job3
    from jobs.job4_video_rendering import run as job4
    from jobs.job5_publishing import run as job5
    from jobs.job6_analytics import run as job6
    from jobs.job7_optimization import run as job7
    from jobs.job8_trend_monitoring import run as job8
    from jobs.job_upcoming_trends import run as job_upcoming_trends

    scheduler.add_job(job1, "interval", hours=4, id="job1_content_research", replace_existing=True)
    scheduler.add_job(job2, "interval", hours=4, id="job2_script_generation", replace_existing=True)
    scheduler.add_job(job3, "interval", hours=4, id="job3_media_assembly", replace_existing=True)
    scheduler.add_job(job4, "interval", hours=2, id="job4_video_rendering", replace_existing=True)
    scheduler.add_job(job5, "interval", hours=2, id="job5_publishing", replace_existing=True)
    scheduler.add_job(job6, "interval", hours=6, id="job6_analytics", replace_existing=True)
    scheduler.add_job(job7, "cron", hour=2, minute=0, id="job7_optimization", replace_existing=True)
    scheduler.add_job(job8, "interval", minutes=30, id="job8_trend_monitoring", replace_existing=True)
    # Weekly: 3–6 month forward-looking trend forecast (Monday 07:00 UTC)
    scheduler.add_job(job_upcoming_trends, "cron", day_of_week="mon", hour=7, minute=0,
                      id="job_upcoming_trends", replace_existing=True)
    logger.info("All 9 jobs registered (incl. weekly upcoming trends).")


def start():
    register_jobs()
    logger.info("Starting autoGenVideo scheduler... (Ctrl+C to stop)")
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Scheduler stopped.")
