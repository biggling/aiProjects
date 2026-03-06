"""Job 5: Auto-Post & Hashtags
Schedule: 3× daily at 07:00, 13:00, 19:00 UTC
"""
import time
from datetime import datetime
from pathlib import Path
from database.models import SessionLocal, Video, Script, Post
from utils.tiktok_api import TikTokClient
from utils.notify import alert_posted
from config import MAX_POSTS_PER_DAY, get_logger

logger = get_logger("job5_auto_post")


def already_posted_today(session) -> int:
    from datetime import date
    today_start = datetime.combine(date.today(), datetime.min.time())
    return session.query(Post).filter(
        Post.posted_at >= today_start,
        Post.platform == "tiktok",
    ).count()


def run():
    logger.info("=== Job 5: Auto-Post started ===")

    session = SessionLocal()
    posted = 0

    try:
        posts_today = already_posted_today(session)
        if posts_today >= MAX_POSTS_PER_DAY:
            logger.info(f"Daily limit reached ({posts_today}/{MAX_POSTS_PER_DAY}). Skipping.")
            return

        remaining = MAX_POSTS_PER_DAY - posts_today
        ready_videos = session.query(Video).filter_by(status="ready").limit(remaining).all()
        logger.info(f"Found {len(ready_videos)} videos to post (remaining today: {remaining}).")

        client = TikTokClient()

        for video in ready_videos:
            script = session.query(Script).get(video.script_id)
            if not script:
                continue

            caption = script.caption or ""
            hashtags = [h.strip() for h in (script.hashtags or "").split(",") if h.strip()]

            try:
                result = client.upload_video(
                    video_path=Path(video.file_path),
                    caption=caption,
                    hashtags=hashtags[:5],
                )

                post = Post(
                    video_id=video.id,
                    platform="tiktok",
                    tiktok_video_id=result.get("publish_id", ""),
                    caption=caption,
                    hashtags=",".join(hashtags),
                    posted_at=datetime.utcnow(),
                    status="posted",
                )
                session.add(post)
                video.status = "posted"
                posted += 1

                product_name = script.product.product_name if script.product else "product"
                alert_posted("TikTok", product_name or caption[:50])
                logger.info(f"Posted video {video.id} to TikTok")
                time.sleep(30)  # Brief pause between posts

            except Exception as e:
                logger.error(f"Post failed for video {video.id}: {e}")
                session.add(Post(
                    video_id=video.id,
                    platform="tiktok",
                    posted_at=datetime.utcnow(),
                    status="failed",
                ))

        session.commit()
        logger.info(f"=== Job 5 complete — {posted} videos posted ===")
    except Exception as e:
        session.rollback()
        logger.error(f"Job 5 failed: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    run()
