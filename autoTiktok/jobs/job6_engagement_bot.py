"""Job 6: Engagement Bot
Schedule: Every 30 minutes (comments) + 2× daily (follow activity)
"""
import time
import random
from datetime import datetime
from database.models import SessionLocal, Post
from utils.tiktok_api import TikTokClient
from utils.ai_utils import generate_comment_reply
from config import MAX_ENGAGEMENT_ACTIONS_PER_HOUR, get_logger

logger = get_logger("job6_engagement_bot")

_action_count = 0  # in-memory rate limit counter (resets per run)


def rate_check() -> bool:
    """Check if we're within the hourly action limit."""
    global _action_count
    if _action_count >= MAX_ENGAGEMENT_ACTIONS_PER_HOUR:
        logger.warning(f"Engagement rate limit reached ({MAX_ENGAGEMENT_ACTIONS_PER_HOUR}/hr). Pausing.")
        return False
    return True


def reply_to_new_comments(session, client: TikTokClient) -> int:
    global _action_count
    replied = 0

    # Get recent TikTok posts
    recent_posts = session.query(Post).filter(
        Post.platform == "tiktok",
        Post.status == "posted",
        Post.tiktok_video_id.isnot(None),
    ).order_by(Post.posted_at.desc()).limit(10).all()

    for post in recent_posts:
        if not rate_check():
            break

        comments = client.get_comments(post.tiktok_video_id)
        for comment in comments[:5]:
            comment_id = comment.get("id")
            comment_text = comment.get("text", "")
            already_replied = comment.get("owner_replied", False)

            if already_replied or not comment_text:
                continue

            # Get product context
            niche = "general"
            product_name = ""
            if post.video and post.video.script and post.video.script.product:
                p = post.video.script.product
                niche = p.niche
                product_name = p.product_name or ""

            try:
                reply = generate_comment_reply(comment_text, niche, product_name)
                if client.reply_to_comment(post.tiktok_video_id, comment_id, reply):
                    replied += 1
                    _action_count += 1
                    logger.info(f"Replied to comment on video {post.tiktok_video_id}")
                    time.sleep(random.uniform(10, 30))
            except Exception as e:
                logger.warning(f"Comment reply failed: {e}")

    return replied


def run():
    global _action_count
    _action_count = 0  # reset for this run

    logger.info("=== Job 6: Engagement Bot started ===")

    session = SessionLocal()
    try:
        client = TikTokClient()
        replied = reply_to_new_comments(session, client)
        logger.info(f"Replied to {replied} comments. Total actions: {_action_count}")
        logger.info("=== Job 6 complete ===")
    except Exception as e:
        logger.error(f"Job 6 failed: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    run()
