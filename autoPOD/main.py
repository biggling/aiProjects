"""autoPOD — Main Entry Point

Usage:
  python main.py --init-db          Initialize database schema
  python main.py --scheduler        Start the full job scheduler
  python main.py --job 1            Run job 1 manually (1-8)
  python main.py --status           Show status of all jobs
"""
import argparse
import sys
from config import get_logger

logger = get_logger("main")

JOB_MAP = {
    "1": ("job1_trend_research", "Trend Research"),
    "2": ("job2_design_generation", "Design Generation"),
    "3": ("job3_listing_publisher", "Listing Publisher"),
    "4": ("job4_seo_marketing", "SEO & Marketing"),
    "5": ("job5_order_monitor", "Order Monitor"),
    "6": ("job6_analytics", "Analytics"),
    "7": ("job7_competitor_intel", "Competitor Intel"),
    "8": ("job8_listing_refresh", "Listing Refresh"),
}


def run_job(job_num: str):
    if job_num not in JOB_MAP:
        logger.error(f"Unknown job number: {job_num}. Valid: 1-8")
        sys.exit(1)
    module_name, friendly_name = JOB_MAP[job_num]
    logger.info(f"Running {friendly_name} manually...")
    module = __import__(f"jobs.{module_name}", fromlist=["run"])
    module.run()


def show_status():
    from database.models import SessionLocal, Niche, Design, Listing, Order
    session = SessionLocal()
    try:
        print("\n=== autoPOD Status ===")
        print(f"Niches tracked:    {session.query(Niche).filter_by(status='active').count()}")
        print(f"Designs ready:     {session.query(Design).filter_by(status='ready').count()}")
        print(f"Designs published: {session.query(Design).filter_by(status='published').count()}")
        print(f"Active listings:   {session.query(Listing).filter_by(status='active').count()}")
        print(f"Total orders:      {session.query(Order).count()}")
        orders = session.query(Order).all()
        total_revenue = sum(o.revenue for o in orders)
        total_profit = sum(o.profit for o in orders)
        print(f"Total revenue:     ${total_revenue:.2f}")
        print(f"Total profit:      ${total_profit:.2f}")
        print("=====================\n")
    finally:
        session.close()


def main():
    parser = argparse.ArgumentParser(description="autoPOD Automation System")
    parser.add_argument("--init-db", action="store_true", help="Initialize database schema")
    parser.add_argument("--scheduler", action="store_true", help="Start job scheduler")
    parser.add_argument("--job", type=str, help="Run specific job (1-8)")
    parser.add_argument("--status", action="store_true", help="Show system status")
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
