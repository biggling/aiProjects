"""Job 8: Analytics & Optimization
Schedule: Daily at 23:00 UTC
"""
import json
from datetime import datetime, timedelta, date
from database.models import SessionLocal, Post, Analytics, Video, Script, Niche
from utils.tiktok_api import TikTokClient
from utils.notify import alert_winner
from config import (
    WINNER_VIEWS_24H, LOSER_VIEWS_48H, WINNER_FOLLOWS_24H,
    REPORTS_DIR, get_logger
)

logger = get_logger("job8_analytics")


def collect_tiktok_stats(client: TikTokClient, post: Post) -> dict | None:
    if not post.tiktok_video_id:
        return None
    try:
        stats = client.get_video_stats(post.tiktok_video_id)
        return {
            "views_24h": int(stats.get("view_count", 0)),
            "likes": int(stats.get("like_count", 0)),
            "comments": int(stats.get("comment_count", 0)),
            "shares": int(stats.get("share_count", 0)),
        }
    except Exception as e:
        logger.warning(f"Stats fetch failed for post {post.id}: {e}")
        return None


def build_action_queue(session, analytics_records: list) -> dict:
    """Build replication and remake queues."""
    replicate = []
    remake = []

    for record in analytics_records:
        post = session.query(Post).get(record.post_id)
        video = session.query(Video).get(post.video_id) if post else None
        script = session.query(Script).get(video.script_id) if video else None
        product = session.query(Niche).get(script.product_id) if script else None

        if record.views_24h >= WINNER_VIEWS_24H:
            replicate.append(post.video_id)
            if product:
                product.performance_score = product.performance_score * 0.5 + record.views_24h * 0.5
            alert_winner(post.video_id, record.views_24h, post.platform)
        elif record.views_24h < LOSER_VIEWS_48H:
            hook = script.hook if script else ""
            remake.append({
                "video_id": post.video_id,
                "reason": f"< {LOSER_VIEWS_48H} views in 24h",
                "original_hook": hook,
            })

    return {"replicate": replicate, "remake": remake}


def generate_report(session) -> str:
    today = date.today()
    pubs = session.query(Post).filter_by(status="posted").count()
    analytics = session.query(Analytics).all()
    total_views = sum(a.views_24h for a in analytics)
    total_likes = sum(a.likes for a in analytics)

    lines = [
        f"# autoTiktok Report — {today}",
        f"- Total posts: {pubs}",
        f"- Total views: {total_views:,}",
        f"- Total likes: {total_likes:,}",
        f"- Avg views/post: {int(total_views/max(pubs, 1)):,}",
    ]
    return "\n".join(lines)


def run():
    logger.info("=== Job 8: Analytics started ===")

    session = SessionLocal()
    try:
        client = TikTokClient()
        cutoff = datetime.utcnow() - timedelta(days=30)
        recent_posts = session.query(Post).filter(
            Post.status == "posted",
            Post.posted_at >= cutoff,
            Post.platform == "tiktok",
        ).all()

        new_records = []
        for post in recent_posts:
            stats = collect_tiktok_stats(client, post)
            if stats:
                views = stats.get("views_24h", 0)
                interactions = stats.get("likes", 0) + stats.get("comments", 0) + stats.get("shares", 0)
                engagement = round(interactions / max(views, 1), 4)
                record = Analytics(
                    post_id=post.id,
                    views_24h=stats.get("views_24h", 0),
                    likes=stats.get("likes", 0),
                    comments=stats.get("comments", 0),
                    shares=stats.get("shares", 0),
                    engagement_rate=engagement,
                    collected_at=datetime.utcnow(),
                )
                session.add(record)
                new_records.append(record)

        session.flush()
        action_queue = build_action_queue(session, new_records)

        # Save action queue for Job 3
        queue_path = REPORTS_DIR / "action_queue.json"
        queue_path.write_text(json.dumps(action_queue, indent=2))
        logger.info(f"Action queue: {len(action_queue['replicate'])} replicate, {len(action_queue['remake'])} remake")

        # Daily report
        report = generate_report(session)
        report_path = REPORTS_DIR / f"{date.today()}.md"
        report_path.write_text(report)

        session.commit()
        logger.info(f"=== Job 8 complete — {len(new_records)} analytics records saved ===")

    except Exception as e:
        session.rollback()
        logger.error(f"Job 8 failed: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    run()
