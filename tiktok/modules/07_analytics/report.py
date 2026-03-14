"""Generate weekly performance summary reports."""

import json
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from dotenv import load_dotenv
from loguru import logger

from modules.01_research.db import SessionLocal, init_db
from modules.06_publisher.models import PublishedVideo
from modules.07_analytics.models import VideoMetric

load_dotenv()

ANALYTICS_DIR = Path("data/analytics")
ANALYTICS_DIR.mkdir(parents=True, exist_ok=True)


def generate_weekly_report(week: str = "current") -> dict:
    """Generate weekly performance report."""
    init_db()
    db = SessionLocal()

    try:
        today = date.today()
        if week == "current":
            week_start = today - timedelta(days=today.weekday())
        else:
            week_start = date.fromisoformat(week)
        week_end = week_start + timedelta(days=6)
        week_num = week_start.isocalendar()[1]

        # Get published videos this week
        pubs = (
            db.query(PublishedVideo)
            .filter(
                PublishedVideo.published_at >= datetime.combine(week_start, datetime.min.time()),
                PublishedVideo.published_at <= datetime.combine(week_end, datetime.max.time()),
                PublishedVideo.status == "published",
            )
            .all()
        )

        # Get metrics for these videos
        pub_ids = [p.id for p in pubs]
        metrics = (
            db.query(VideoMetric)
            .filter(VideoMetric.published_video_id.in_(pub_ids))
            .all()
            if pub_ids
            else []
        )

        # Aggregate
        total_views = sum(m.views for m in metrics)
        total_gmv = sum(m.gmv for m in metrics)
        total_likes = sum(m.likes for m in metrics)
        total_shares = sum(m.shares for m in metrics)
        avg_ctr = sum(m.ctr for m in metrics) / len(metrics) if metrics else 0

        # Top 3 by views
        sorted_metrics = sorted(metrics, key=lambda m: m.views, reverse=True)
        top_3 = [
            {
                "published_video_id": m.published_video_id,
                "views": m.views,
                "gmv": m.gmv,
                "ctr": m.ctr,
                "winner": m.winner,
            }
            for m in sorted_metrics[:3]
        ]

        report = {
            "week": f"{week_start.year}-W{week_num:02d}",
            "period": f"{week_start.isoformat()} to {week_end.isoformat()}",
            "total_views": total_views,
            "total_gmv": total_gmv,
            "total_likes": total_likes,
            "total_shares": total_shares,
            "avg_ctr": round(avg_ctr, 4),
            "videos_published": len(pubs),
            "top_3_videos": top_3,
        }

        # Save report
        report_path = ANALYTICS_DIR / f"weekly_report_{week_start.year}-W{week_num:02d}.json"
        report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2))
        logger.info(f"Weekly report saved: {report_path}")

        return report

    finally:
        db.close()


def print_report(report: dict) -> None:
    """Pretty-print weekly report."""
    print("\n" + "=" * 60)
    print(f"  WEEKLY REPORT — {report['period']}")
    print("=" * 60)
    print(f"  Videos published: {report['videos_published']}")
    print(f"  Total views:      {report['total_views']:,}")
    print(f"  Total GMV:        ฿{report['total_gmv']:,.2f}")
    print(f"  Avg CTR:          {report['avg_ctr']:.2%}")
    print(f"  Total likes:      {report['total_likes']:,}")
    print(f"  Total shares:     {report['total_shares']:,}")
    print("-" * 40)
    print("  Top 3 Videos:")
    for i, v in enumerate(report.get("top_3_videos", []), 1):
        winner = " ★" if v.get("winner") else ""
        print(f"    {i}. Video {v['published_video_id']}: "
              f"{v['views']:,} views, ฿{v['gmv']:,.2f} GMV{winner}")
    print()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--week", default="current", help="Week start date or 'current'")
    args = parser.parse_args()

    report = generate_weekly_report(args.week)
    print_report(report)
