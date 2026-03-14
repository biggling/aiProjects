"""APScheduler publish jobs for scheduled video posting."""

import json
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from dotenv import load_dotenv
from loguru import logger

from modules.01_research.db import SessionLocal, init_db
from modules.02_scriptgen.models import Script
from modules.05_editor.models import EditedVideo
from modules.06_publisher.models import PublishedVideo
from modules.06_publisher.link_tagger import format_affiliate_link
from modules.06_publisher import tiktok, instagram, youtube

load_dotenv()


def publish_next_video(dry_run: bool = False) -> dict | None:
    """Find next approved, unpublished video and publish to TikTok."""
    init_db()
    db = SessionLocal()

    try:
        # Find approved videos not yet published to TikTok
        published_ids = [
            p.edited_video_id
            for p in db.query(PublishedVideo.edited_video_id)
            .filter(PublishedVideo.platform == "tiktok")
            .all()
        ]

        video = (
            db.query(EditedVideo)
            .filter(
                EditedVideo.status == "approved",
                EditedVideo.id.notin_(published_ids) if published_ids else True,
            )
            .order_by(EditedVideo.created_at.asc())
            .first()
        )

        if not video:
            logger.info("No approved videos pending publish")
            return None

        script = db.query(Script).filter(Script.id == video.script_id).first()
        if not script:
            logger.error(f"Script not found for edited video {video.id}")
            return None

        # Build caption with affiliate link
        hashtags = json.loads(script.hashtags) if script.hashtags else []
        affiliate_link = format_affiliate_link(script.product_id or "", video.id)
        caption = f"{script.caption}\n\n{' '.join('#' + h for h in hashtags)}"
        if affiliate_link:
            caption += f"\n\n🔗 {affiliate_link}"

        result = {"video_id": video.id, "platform": "tiktok", "caption": caption}

        if dry_run:
            logger.info(f"[DRY RUN] Would publish video {video.id} to TikTok")
            result["status"] = "dry_run"
            return result

        # Publish
        post_id = tiktok.upload_video(
            file_path=Path(video.file_path),
            caption=caption,
            cover_path=Path(video.thumbnail_path) if video.thumbnail_path else None,
        )

        # Record publication
        pub = PublishedVideo(
            edited_video_id=video.id,
            platform="tiktok",
            post_id=post_id,
            published_at=datetime.utcnow(),
            status="published",
        )
        db.add(pub)
        db.commit()

        result["post_id"] = post_id
        result["status"] = "published"
        logger.info(f"Published video {video.id} to TikTok: {post_id}")
        return result

    except Exception as e:
        db.rollback()
        logger.error(f"Publish failed: {e}")
        raise
    finally:
        db.close()


def crosspost_recent(dry_run: bool = False) -> list[dict]:
    """Cross-post recent TikTok publishes to Instagram and YouTube."""
    init_db()
    db = SessionLocal()
    results = []

    try:
        # Find TikTok publishes not yet cross-posted
        tiktok_pubs = (
            db.query(PublishedVideo)
            .filter(
                PublishedVideo.platform == "tiktok",
                PublishedVideo.status == "published",
            )
            .all()
        )

        for pub in tiktok_pubs:
            video = db.query(EditedVideo).filter(EditedVideo.id == pub.edited_video_id).first()
            if not video:
                continue

            script = db.query(Script).filter(Script.id == video.script_id).first()
            if not script:
                continue

            caption = script.caption

            # Check if already cross-posted
            for platform in ["instagram", "youtube"]:
                existing = (
                    db.query(PublishedVideo)
                    .filter(
                        PublishedVideo.edited_video_id == video.id,
                        PublishedVideo.platform == platform,
                    )
                    .first()
                )
                if existing:
                    continue

                if dry_run:
                    logger.info(f"[DRY RUN] Would cross-post video {video.id} to {platform}")
                    results.append({"video_id": video.id, "platform": platform, "status": "dry_run"})
                    continue

                try:
                    if platform == "instagram":
                        post_id = instagram.post_reel(Path(video.file_path), caption)
                    else:
                        hashtags = json.loads(script.hashtags) if script.hashtags else []
                        post_id = youtube.upload_short(
                            Path(video.file_path),
                            title=script.hook[:100],
                            description=caption,
                            tags=hashtags,
                        )

                    cross_pub = PublishedVideo(
                        edited_video_id=video.id,
                        platform=platform,
                        post_id=post_id,
                        published_at=datetime.utcnow(),
                        status="published",
                    )
                    db.add(cross_pub)
                    results.append({"video_id": video.id, "platform": platform, "status": "published"})

                except Exception as e:
                    logger.error(f"Cross-post to {platform} failed for video {video.id}: {e}")
                    results.append({"video_id": video.id, "platform": platform, "status": f"failed: {e}"})

        db.commit()

    except Exception as e:
        db.rollback()
        logger.error(f"Cross-post failed: {e}")
        raise
    finally:
        db.close()

    return results
