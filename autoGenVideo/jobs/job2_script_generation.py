"""Job 2: Script & Content Generation
Schedule: Every 4 hours (triggered after Job 1)
"""
import json
from database.models import SessionLocal, Topic, Script
from utils.ai_utils import generate_video_script
from config import DEFAULT_LANGUAGE, get_logger

logger = get_logger("job2_script_generation")

PLATFORM_DURATIONS = {
    "tiktok": 30,
    "youtube": 60,
    "instagram": 30,
    "pinterest": 15,
}


def validate_script(script: dict) -> bool:
    return all(k in script for k in ["hook", "body", "cta", "caption", "voiceover_text", "hashtags"])


def run():
    logger.info("=== Job 2: Script Generation started ===")

    session = SessionLocal()
    generated = 0

    try:
        pending_topics = session.query(Topic).filter_by(status="pending").limit(10).all()
        logger.info(f"Found {len(pending_topics)} pending topics.")

        for topic_row in pending_topics:
            for platform, duration in PLATFORM_DURATIONS.items():
                try:
                    script_data = generate_video_script(
                        topic=topic_row.topic,
                        platform=platform,
                        duration=duration,
                        language=topic_row.language or DEFAULT_LANGUAGE,
                    )
                    if not validate_script(script_data):
                        logger.warning(f"Invalid script for {topic_row.topic} / {platform}")
                        continue

                    script = Script(
                        topic_id=topic_row.id,
                        hook=script_data["hook"],
                        body=json.dumps(script_data["body"]),
                        cta=script_data["cta"],
                        caption=script_data["caption"],
                        voiceover_text=script_data["voiceover_text"],
                        hashtags=",".join(script_data.get("hashtags", [])),
                        language=topic_row.language or DEFAULT_LANGUAGE,
                        duration_target=duration,
                        status="pending",
                    )
                    session.add(script)
                    generated += 1
                    logger.info(f"Script generated: {topic_row.topic[:40]} ({platform})")
                except Exception as e:
                    logger.error(f"Script gen failed for '{topic_row.topic}' / {platform}: {e}")

            topic_row.status = "scripted"

        session.commit()
        logger.info(f"=== Job 2 complete — {generated} scripts generated ===")
    except Exception as e:
        session.rollback()
        logger.error(f"Job 2 failed: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    run()
