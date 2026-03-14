"""Nightly metrics collection from TikTok analytics."""

import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from dotenv import load_dotenv
import httpx
from loguru import logger

from modules.01_research.db import SessionLocal, init_db
from modules.06_publisher.models import PublishedVideo
from modules.07_analytics.models import VideoMetric

load_dotenv()


def pull_metrics() -> int:
    """Pull metrics for all videos published in last 14 days. Returns count pulled."""
    init_db()
    db = SessionLocal()
    count = 0

    try:
        cutoff = datetime.utcnow() - timedelta(days=14)
        recent_pubs = (
            db.query(PublishedVideo)
            .filter(
                PublishedVideo.published_at >= cutoff,
                PublishedVideo.platform == "tiktok",
                PublishedVideo.status == "published",
            )
            .all()
        )

        if not recent_pubs:
            logger.info("No recent publications to pull metrics for")
            return 0

        access_token = os.getenv("TIKTOK_ACCESS_TOKEN", "")

        for pub in recent_pubs:
            try:
                metrics = _fetch_video_metrics(access_token, pub.post_id)

                metric = VideoMetric(
                    published_video_id=pub.id,
                    pulled_at=datetime.utcnow(),
                    views=metrics.get("views", 0),
                    watch_time_avg=metrics.get("watch_time_avg", 0.0),
                    likes=metrics.get("likes", 0),
                    shares=metrics.get("shares", 0),
                    comments=metrics.get("comments", 0),
                    ctr=metrics.get("ctr", 0.0),
                    gmv=metrics.get("gmv", 0.0),
                )
                db.add(metric)
                count += 1

            except Exception as e:
                logger.error(f"Failed to pull metrics for pub {pub.id}: {e}")
                continue

        db.commit()
        logger.info(f"Pulled metrics for {count} videos")

    except Exception as e:
        db.rollback()
        logger.error(f"Metrics pull failed: {e}")
        raise
    finally:
        db.close()

    return count


def _fetch_video_metrics(access_token: str, post_id: str | None) -> dict:
    """Fetch metrics from TikTok Analytics API."""
    if not post_id:
        return {}

    url = "https://open.tiktokapis.com/v2/video/query/"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    try:
        with httpx.Client(timeout=30) as client:
            response = client.post(
                url,
                json={"filters": {"video_ids": [post_id]}},
                headers=headers,
            )
            response.raise_for_status()
            data = response.json()
            videos = data.get("data", {}).get("videos", [])
            if videos:
                v = videos[0]
                return {
                    "views": v.get("view_count", 0),
                    "watch_time_avg": v.get("average_watch_time", 0.0),
                    "likes": v.get("like_count", 0),
                    "shares": v.get("share_count", 0),
                    "comments": v.get("comment_count", 0),
                    "ctr": 0.0,  # Calculated separately from shop data
                    "gmv": 0.0,  # From affiliate API
                }
    except Exception as e:
        logger.warning(f"Failed to fetch metrics for {post_id}: {e}")

    return {}


if __name__ == "__main__":
    count = pull_metrics()
    print(f"Pulled metrics for {count} videos")
