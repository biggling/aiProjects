"""Job 7: Content Optimization & Regeneration
Schedule: Daily at 02:00 UTC
"""
from datetime import datetime, timedelta
from database.models import SessionLocal, Publication, Analytics, Video, Script, Topic
from utils.ai_utils import generate_improved_hook
from config import UNDERPERFORM_VIEW_THRESHOLD, UNDERPERFORM_HOURS, VIRAL_VIEW_THRESHOLD, get_logger

logger = get_logger("job7_optimization")


def get_latest_analytics(session, pub_id: int) -> Analytics | None:
    return session.query(Analytics).filter_by(pub_id=pub_id).order_by(Analytics.collected_at.desc()).first()


def mark_for_remake(session, video: Video, script: Script, reason: str):
    """Duplicate script as a remake."""
    new_script = Script(
        topic_id=script.topic_id,
        hook=f"[REMAKE] {script.hook}",
        body=script.body,
        cta=script.cta,
        caption=script.caption,
        voiceover_text=script.voiceover_text,
        hashtags=script.hashtags,
        language=script.language,
        duration_target=script.duration_target,
        status="pending",
    )
    session.add(new_script)
    logger.info(f"Video {video.id} queued for remake: {reason}")


def replicate_successful_video(session, video: Video, script: Script, count: int = 3):
    """Create N new scripts similar to a viral video for scaling."""
    topic = script.topic
    niche = topic.topic if topic else "general"
    logger.info(f"Replicating viral video {video.id} ({count}x) on topic: {niche}")

    for i in range(count):
        new_script = Script(
            topic_id=script.topic_id,
            hook=f"Part {i + 2}: {script.hook}",
            body=script.body,
            cta=script.cta,
            caption=script.caption,
            voiceover_text=script.voiceover_text,
            hashtags=script.hashtags,
            language=script.language,
            duration_target=script.duration_target,
            status="pending",
        )
        session.add(new_script)


def run():
    logger.info("=== Job 7: Optimization started ===")

    session = SessionLocal()
    remade = 0
    replicated = 0

    try:
        cutoff = datetime.utcnow() - timedelta(hours=UNDERPERFORM_HOURS)
        publications = session.query(Publication).filter(
            Publication.status == "posted",
            Publication.posted_at <= cutoff,
        ).all()

        logger.info(f"Checking {len(publications)} publications for optimization.")

        for pub in publications:
            analytics = get_latest_analytics(session, pub.id)
            if not analytics:
                continue

            video = session.query(Video).get(pub.video_id)
            if not video:
                continue
            script = session.query(Script).get(video.script_id)
            if not script:
                continue

            views = analytics.views

            if views >= VIRAL_VIEW_THRESHOLD:
                replicate_successful_video(session, video, script, count=3)
                replicated += 3

            elif views < UNDERPERFORM_VIEW_THRESHOLD:
                # Generate improved hook
                try:
                    new_hooks = generate_improved_hook(script.hook or "", script.topic.topic if script.topic else "")
                    if new_hooks:
                        script_copy = Script(
                            topic_id=script.topic_id,
                            hook=new_hooks[0],
                            body=script.body,
                            cta=script.cta,
                            caption=script.caption,
                            voiceover_text=script.voiceover_text,
                            hashtags=script.hashtags,
                            language=script.language,
                            duration_target=script.duration_target,
                            status="pending",
                        )
                        session.add(script_copy)
                        remade += 1
                except Exception as e:
                    logger.error(f"Hook generation failed for script {script.id}: {e}")
                    mark_for_remake(session, video, script, f"< {UNDERPERFORM_VIEW_THRESHOLD} views after {UNDERPERFORM_HOURS}h")
                    remade += 1

        session.commit()
        logger.info(f"=== Job 7 complete — remade: {remade}, replicated: {replicated} ===")
    except Exception as e:
        session.rollback()
        logger.error(f"Job 7 failed: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    run()
