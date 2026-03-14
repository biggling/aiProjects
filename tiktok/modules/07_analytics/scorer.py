"""Score and rank videos, flag winners for remix."""

import json
import sys
from datetime import datetime, date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from dotenv import load_dotenv
from loguru import logger

from modules.01_research.db import SessionLocal, init_db
from modules.07_analytics.models import VideoMetric

load_dotenv()

ANALYTICS_DIR = Path("data/analytics")
ANALYTICS_DIR.mkdir(parents=True, exist_ok=True)


def score_videos() -> list[dict]:
    """Score all recent videos and flag top 20% as winners."""
    init_db()
    db = SessionLocal()

    try:
        # Get latest metrics per video
        metrics = db.query(VideoMetric).order_by(VideoMetric.pulled_at.desc()).all()

        if not metrics:
            logger.info("No metrics to score")
            return []

        # Deduplicate to latest per published_video_id
        latest = {}
        for m in metrics:
            if m.published_video_id not in latest:
                latest[m.published_video_id] = m

        scored = []
        for pub_id, m in latest.items():
            # Composite score
            score = (
                (m.views * 0.3)
                + (m.watch_time_avg * 0.3)
                + (m.ctr * 0.2)
                + (m.gmv * 0.2)
            )
            scored.append({
                "published_video_id": pub_id,
                "views": m.views,
                "watch_time_avg": m.watch_time_avg,
                "ctr": m.ctr,
                "gmv": m.gmv,
                "likes": m.likes,
                "shares": m.shares,
                "score": score,
                "metric_id": m.id,
            })

        # Sort by score
        scored.sort(key=lambda x: x["score"], reverse=True)

        # Flag top 20% as winners
        winner_count = max(1, len(scored) // 5)
        for i, item in enumerate(scored):
            is_winner = i < winner_count
            item["winner"] = is_winner

            # Update DB
            metric = db.query(VideoMetric).filter(VideoMetric.id == item["metric_id"]).first()
            if metric:
                metric.winner = is_winner

        db.commit()
        logger.info(f"Scored {len(scored)} videos, {winner_count} winners")
        return scored

    except Exception as e:
        db.rollback()
        logger.error(f"Scoring failed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--approve-interactive", action="store_true")
    args = parser.parse_args()

    results = score_videos()

    if args.approve_interactive:
        winners = [r for r in results if r["winner"]]
        print(f"\nTop {len(winners)} winners:")
        for w in winners:
            print(f"  Video {w['published_video_id']}: score={w['score']:.2f}, "
                  f"views={w['views']}, GMV={w['gmv']:.2f}")
            approval = input("  Approve for remix? (y/n): ").strip().lower()
            if approval == "y":
                print("  → Approved for remix")
    else:
        for r in results:
            flag = " ★ WINNER" if r["winner"] else ""
            print(f"Video {r['published_video_id']}: score={r['score']:.2f}{flag}")
