"""autoTiktok — Main Entry Point

Usage:
  python main.py --init-db          Initialize database schema
  python main.py --scheduler        Start job scheduler
  python main.py --job 1            Run specific job (1-8)
  python main.py --status           Show system status
"""
import argparse
import sys
from config import get_logger

logger = get_logger("main")

JOB_MAP = {
    "1": ("job1_niche_research", "Niche Research"),
    "2": ("job2_content_research", "Content Research"),
    "3": ("job3_script_generation", "Script Generation"),
    "4": ("job4_video_production", "Video Production"),
    "5": ("job5_auto_post", "Auto-Post"),
    "6": ("job6_engagement_bot", "Engagement Bot"),
    "7": ("job7_affiliate_tracker", "Affiliate Tracker"),
    "8": ("job8_analytics", "Analytics"),
    "trend": ("job_trend_forecast", "Trend Forecast (3-6 Month)"),
}


def run_job(num: str):
    if num not in JOB_MAP:
        logger.error(f"Unknown job: {num}. Valid: 1-8")
        sys.exit(1)
    module_name, name = JOB_MAP[num]
    logger.info(f"Running {name}...")
    m = __import__(f"jobs.{module_name}", fromlist=["run"])
    m.run()


def show_status():
    from database.models import SessionLocal, Niche, Script, Video, Post, Affiliate
    s = SessionLocal()
    try:
        print("\n=== autoTiktok Status ===")
        print(f"Active products:   {s.query(Niche).filter_by(status='active').count()}")
        print(f"Pending scripts:   {s.query(Script).filter_by(status='pending').count()}")
        print(f"Approved scripts:  {s.query(Script).filter_by(status='approved').count()}")
        print(f"Ready videos:      {s.query(Video).filter_by(status='ready').count()}")
        print(f"Total posts:       {s.query(Post).count()}")
        commission = sum(a.commission for a in s.query(Affiliate).all())
        print(f"Total commission:  ${commission:.2f}")
        print("=========================\n")
    finally:
        s.close()


def main():
    parser = argparse.ArgumentParser(description="autoTiktok Automation System")
    parser.add_argument("--init-db", action="store_true")
    parser.add_argument("--scheduler", action="store_true")
    parser.add_argument("--job", type=str)
    parser.add_argument("--status", action="store_true")
    args = parser.parse_args()

    if args.init_db:
        from database.init_db import init_db
        init_db()
    elif args.scheduler:
        from scheduler import start
        start()
    elif args.job:
        run_job(args.job)
    elif args.status:
        show_status()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
