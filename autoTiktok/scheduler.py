"""APScheduler for autoTiktok."""
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor
from config import DATABASE_URL, get_logger

logger = get_logger("scheduler")

scheduler = BlockingScheduler(
    jobstores={"default": SQLAlchemyJobStore(url=DATABASE_URL)},
    executors={"default": ThreadPoolExecutor(max_workers=4)},
    job_defaults={"coalesce": True, "max_instances": 1, "misfire_grace_time": 300},
    timezone="UTC",
)


def register_jobs():
    from jobs.job1_niche_research import run as job1
    from jobs.job2_content_research import run as job2
    from jobs.job3_script_generation import run as job3
    from jobs.job4_video_production import run as job4
    from jobs.job5_auto_post import run as job5
    from jobs.job6_engagement_bot import run as job6
    from jobs.job7_affiliate_tracker import run as job7
    from jobs.job8_analytics import run as job8
    from jobs.job_upcoming_trends import run as job_upcoming_trends

    scheduler.add_job(job1, "cron", hour=6, minute=0, id="job1_niche_research", replace_existing=True)
    scheduler.add_job(job2, "interval", hours=4, id="job2_content_research", replace_existing=True)
    scheduler.add_job(job3, "interval", hours=6, id="job3_script_generation", replace_existing=True)
    scheduler.add_job(job4, "interval", hours=6, id="job4_video_production", replace_existing=True)
    scheduler.add_job(job5, "cron", hour="7,13,19", minute=0, id="job5_auto_post", replace_existing=True)
    scheduler.add_job(job6, "interval", minutes=30, id="job6_engagement_bot", replace_existing=True)
    scheduler.add_job(job7, "interval", hours=6, id="job7_affiliate_tracker", replace_existing=True)
    scheduler.add_job(job8, "cron", hour=23, minute=0, id="job8_analytics", replace_existing=True)
    # Weekly: 3–6 month forward-looking affiliate trend forecast (Monday 06:30 UTC)
    scheduler.add_job(job_upcoming_trends, "cron", day_of_week="mon", hour=6, minute=30,
                      id="job_upcoming_trends", replace_existing=True)
    logger.info("All 9 TikTok jobs registered (incl. weekly upcoming trends).")


def start():
    register_jobs()
    logger.info("Starting autoTiktok scheduler... (Ctrl+C to stop)")
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Scheduler stopped.")
