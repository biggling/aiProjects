"""Job 6: Analytics & Performance Tracking
Schedule: Every 6 hours
"""
from datetime import datetime
from database.models import SessionLocal, Publication, Analytics, Video, Script
from utils.notify import alert_viral
from config import VIRAL_VIEW_THRESHOLD, UNDERPERFORM_VIEW_THRESHOLD, REPORTS_DIR, get_logger

logger = get_logger("job6_analytics")


def fetch_youtube_stats(post_id: str) -> dict:
    try:
        from utils.platform_api import YouTubeClient
        from config import YOUTUBE_REFRESH_TOKEN
        if not YOUTUBE_REFRESH_TOKEN or not post_id:
            return {}
        client = YouTubeClient()
        stats = client.get_video_stats(post_id)
        views = int(stats.get("viewCount", 0))
        likes = int(stats.get("likeCount", 0))
        comments = int(stats.get("commentCount", 0))
        return {"views": views, "likes": likes, "comments": comments, "shares": 0}
    except Exception as e:
        logger.warning(f"YouTube stats fetch failed: {e}")
        return {}


def fetch_tiktok_stats(post_id: str) -> dict:
    try:
        from utils.platform_api import TikTokClient
        from config import TIKTOK_ACCESS_TOKEN
        if not TIKTOK_ACCESS_TOKEN or not post_id:
            return {}
        client = TikTokClient()
        stats = client.get_video_stats(post_id)
        return {
            "views": stats.get("view_count", 0),
            "likes": stats.get("like_count", 0),
            "comments": stats.get("comment_count", 0),
            "shares": stats.get("share_count", 0),
        }
    except Exception as e:
        logger.warning(f"TikTok stats fetch failed: {e}")
        return {}


def calculate_engagement_rate(stats: dict) -> float:
    views = stats.get("views", 0)
    if views == 0:
        return 0.0
    interactions = stats.get("likes", 0) + stats.get("comments", 0) + stats.get("shares", 0)
    return round(interactions / views, 4)


def generate_daily_report(session) -> str:
    pubs = session.query(Publication).filter_by(status="posted").all()
    total_views = 0
    total_likes = 0
    best_video = None
    best_views = 0

    for pub in pubs:
        analytics = session.query(Analytics).filter_by(pub_id=pub.id).order_by(Analytics.collected_at.desc()).first()
        if analytics:
            total_views += analytics.views
            total_likes += analytics.likes
            if analytics.views > best_views:
                best_views = analytics.views
                best_video = pub

    report = [
        f"# autoGenVideo Analytics — {datetime.utcnow().date()}",
        f"- Total publications: {len(pubs)}",
        f"- Total views: {total_views:,}",
        f"- Total likes: {total_likes:,}",
        f"- Best video views: {best_views:,}",
    ]
    return "\n".join(report)


def run():
    logger.info("=== Job 6: Analytics started ===")

    session = SessionLocal()
    updated = 0

    try:
        publications = session.query(Publication).filter_by(status="posted").all()
        logger.info(f"Checking analytics for {len(publications)} publications.")

        for pub in publications:
            stats = {}
            if pub.platform == "youtube":
                stats = fetch_youtube_stats(pub.post_id)
            elif pub.platform == "tiktok":
                stats = fetch_tiktok_stats(pub.post_id)

            if not stats:
                continue

            engagement = calculate_engagement_rate(stats)
            record = Analytics(
                pub_id=pub.id,
                platform=pub.platform,
                views=stats.get("views", 0),
                likes=stats.get("likes", 0),
                comments=stats.get("comments", 0),
                shares=stats.get("shares", 0),
                engagement_rate=engagement,
                collected_at=datetime.utcnow(),
            )
            session.add(record)
            updated += 1

            if stats.get("views", 0) >= VIRAL_VIEW_THRESHOLD:
                video = session.query(Video).get(pub.video_id)
                script = session.query(Script).get(video.script_id) if video else None
                topic = script.topic.topic if script and script.topic else "unknown"
                alert_viral(pub.platform, topic, stats["views"], pub.url or "")

        session.commit()

        # Save daily report
        report = generate_daily_report(session)
        report_path = REPORTS_DIR / f"{datetime.utcnow().date()}.md"
        report_path.write_text(report)
        logger.info(f"Report saved: {report_path}")
        logger.info(f"=== Job 6 complete — {updated} analytics records updated ===")

    except Exception as e:
        session.rollback()
        logger.error(f"Job 6 failed: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    run()
