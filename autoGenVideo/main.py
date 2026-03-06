"""autoGenVideo — Main Entry Point

Usage:
  python main.py --init-db          Initialize database
  python main.py --scheduler        Start job scheduler
  python main.py --api              Start FastAPI server
  python main.py --job 1            Run specific job (1-8)
  python main.py --status           Show system status
"""
import argparse
import sys
from config import get_logger

logger = get_logger("main")

JOB_MAP = {
    "1": ("job1_content_research", "Content Research"),
    "2": ("job2_script_generation", "Script Generation"),
    "3": ("job3_media_assembly", "Media Assembly"),
    "4": ("job4_video_rendering", "Video Rendering"),
    "5": ("job5_publishing", "Publishing"),
    "6": ("job6_analytics", "Analytics"),
    "7": ("job7_optimization", "Optimization"),
    "8": ("job8_trend_monitoring", "Trend Monitoring"),
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
    from database.models import SessionLocal, Topic, Script, Video, Publication
    s = SessionLocal()
    try:
        print("\n=== autoGenVideo Status ===")
        print(f"Pending topics:    {s.query(Topic).filter_by(status='pending').count()}")
        print(f"Pending scripts:   {s.query(Script).filter_by(status='pending').count()}")
        print(f"Ready videos:      {s.query(Video).filter_by(status='ready').count()}")
        print(f"Published videos:  {s.query(Video).filter_by(status='published').count()}")
        print(f"Total publications:{s.query(Publication).count()}")
        print("==========================\n")
    finally:
        s.close()


def main():
    parser = argparse.ArgumentParser(description="autoGenVideo Automation System")
    parser.add_argument("--init-db", action="store_true")
    parser.add_argument("--scheduler", action="store_true")
    parser.add_argument("--api", action="store_true", help="Start FastAPI server")
    parser.add_argument("--job", type=str)
    parser.add_argument("--status", action="store_true")
    args = parser.parse_args()

    if args.init_db:
        from database.init_db import init_db
        init_db()
    elif args.scheduler:
        from scheduler import start
        start()
    elif args.api:
        import uvicorn
        uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=False)
    elif args.job:
        run_job(args.job)
    elif args.status:
        show_status()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
