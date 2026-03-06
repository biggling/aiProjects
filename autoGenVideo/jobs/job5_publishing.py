"""Job 5: Multi-Platform Publishing
Schedule: Every 2 hours
"""
import time
from datetime import datetime
from pathlib import Path
from database.models import SessionLocal, Video, Script, Topic, Publication
from utils.platform_api import YouTubeClient, TikTokClient, InstagramClient, PinterestClient
from utils.notify import alert_posted
from config import YOUTUBE_REFRESH_TOKEN, TIKTOK_ACCESS_TOKEN, INSTAGRAM_ACCESS_TOKEN, PINTEREST_ACCESS_TOKEN, get_logger

logger = get_logger("job5_publishing")

PLATFORM_ORDER = ["youtube", "tiktok", "instagram", "pinterest"]
POST_DELAY_SECONDS = 90  # stagger between platforms


def get_script_meta(session, video: Video) -> dict:
    script = session.query(Script).get(video.script_id)
    topic = session.query(Topic).get(script.topic_id) if script else None
    return {
        "hook": script.hook if script else "Watch this!",
        "caption": script.caption if script else "",
        "hashtags": (script.hashtags or "").split(",") if script else [],
        "topic": topic.topic if topic else "video",
    }


def publish_to_youtube(video: Video, meta: dict) -> dict | None:
    if not YOUTUBE_REFRESH_TOKEN:
        logger.info("YouTube credentials not set, skipping.")
        return None
    try:
        client = YouTubeClient()
        result = client.upload_short(
            video_path=Path(video.file_path),
            title=meta["hook"][:100],
            description=meta["caption"],
            tags=meta["hashtags"][:15],
        )
        alert_posted("YouTube Shorts", meta["topic"], result.get("url", ""))
        return result
    except Exception as e:
        logger.error(f"YouTube publish failed: {e}")
        return None


def publish_to_tiktok(video: Video, meta: dict) -> dict | None:
    if not TIKTOK_ACCESS_TOKEN:
        logger.info("TikTok token not set, skipping.")
        return None
    try:
        client = TikTokClient()
        result = client.upload_video(
            video_path=Path(video.file_path),
            caption=meta["caption"],
            hashtags=meta["hashtags"][:5],
        )
        alert_posted("TikTok", meta["topic"])
        return result
    except Exception as e:
        logger.error(f"TikTok publish failed: {e}")
        return None


def run():
    logger.info("=== Job 5: Publishing started ===")

    session = SessionLocal()
    published = 0

    try:
        ready_videos = session.query(Video).filter_by(status="ready").limit(8).all()
        logger.info(f"Found {len(ready_videos)} videos ready to publish.")

        for video in ready_videos:
            meta = get_script_meta(session, video)
            results = {}

            # Publish to YouTube first (most reliable API)
            r = publish_to_youtube(video, meta)
            if r:
                results["youtube"] = r
                session.add(Publication(
                    video_id=video.id,
                    platform="youtube",
                    post_id=r.get("video_id", ""),
                    url=r.get("url", ""),
                    posted_at=datetime.utcnow(),
                    status="posted",
                ))
                published += 1
                time.sleep(POST_DELAY_SECONDS)

            # TikTok
            r = publish_to_tiktok(video, meta)
            if r:
                results["tiktok"] = r
                session.add(Publication(
                    video_id=video.id,
                    platform="tiktok",
                    post_id=r.get("publish_id", ""),
                    posted_at=datetime.utcnow(),
                    status="posted",
                ))
                published += 1
                time.sleep(POST_DELAY_SECONDS)

            if results:
                video.status = "published"

        session.commit()
        logger.info(f"=== Job 5 complete — {published} publications created ===")
    except Exception as e:
        session.rollback()
        logger.error(f"Job 5 failed: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    run()
