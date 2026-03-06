"""APScheduler configuration for all autoPOD jobs."""
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor
from config import DATABASE_URL, get_logger

logger = get_logger("scheduler")

jobstores = {
    "default": SQLAlchemyJobStore(url=DATABASE_URL)
}
executors = {
    "default": ThreadPoolExecutor(max_workers=4)
}
job_defaults = {
    "coalesce": True,       # merge missed runs into one
    "max_instances": 1,     # no concurrent runs of same job
    "misfire_grace_time": 600,
}

scheduler = BlockingScheduler(
    jobstores=jobstores,
    executors=executors,
    job_defaults=job_defaults,
    timezone="UTC",
)


def register_jobs():
    from jobs.job1_trend_research import run as job1
    from jobs.job2_design_generation import run as job2
    from jobs.job3_listing_publisher import run as job3
    from jobs.job4_seo_marketing import run as job4
    from jobs.job5_order_monitor import run as job5
    from jobs.job6_analytics import run as job6
    from jobs.job7_competitor_intel import run as job7
    from jobs.job8_listing_refresh import run as job8

    # Daily jobs
    scheduler.add_job(job1, "cron", hour=6, minute=0, id="job1_trend_research", replace_existing=True)
    scheduler.add_job(job2, "cron", hour=8, minute=0, id="job2_design_generation", replace_existing=True)
    scheduler.add_job(job3, "cron", hour=10, minute=0, id="job3_listing_publisher", replace_existing=True)
    scheduler.add_job(job6, "cron", hour=23, minute=59, id="job6_analytics", replace_existing=True)

    # Interval jobs
    scheduler.add_job(job4, "interval", hours=6, id="job4_seo_marketing", replace_existing=True)
    scheduler.add_job(job5, "interval", hours=2, id="job5_order_monitor", replace_existing=True)

    # Weekly jobs
    scheduler.add_job(job7, "cron", day_of_week="sun", hour=7, id="job7_competitor_intel", replace_existing=True)
    scheduler.add_job(job8, "cron", day_of_week="wed", hour=9, id="job8_listing_refresh", replace_existing=True)

    logger.info("All 8 jobs registered.")


def start():
    register_jobs()
    logger.info("Starting scheduler... (Ctrl+C to stop)")
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Scheduler stopped.")
