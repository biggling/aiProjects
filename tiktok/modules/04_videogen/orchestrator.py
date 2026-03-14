"""Video generation orchestrator — coordinates clip generation across providers."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from dotenv import load_dotenv
from loguru import logger

from modules.01_research.db import SessionLocal, init_db
from modules.02_scriptgen.models import Script
from modules.04_videogen.models import VideoClip
from modules.04_videogen.prompt_builder import build_video_prompt
from modules.04_videogen import kling, runway

load_dotenv()


def generate_videos() -> int:
    """Generate video clips for all scripts without clips. Returns count generated."""
    init_db()
    db = SessionLocal()
    count = 0

    try:
        existing_script_ids = [v.script_id for v in db.query(VideoClip.script_id).all()]
        scripts = db.query(Script).filter(
            Script.id.notin_(existing_script_ids) if existing_script_ids else True
        ).all()

        if not scripts:
            logger.info("No scripts pending video generation")
            return 0

        for script in scripts:
            try:
                # Build visual prompt from script body
                video_prompt = build_video_prompt(script.body)
                prompt_text = video_prompt["scene"]

                # Try Kling first, fallback to Runway
                provider = "kling"
                try:
                    clip_path = kling.generate(prompt_text)
                except Exception as e:
                    logger.warning(f"Kling failed for script {script.id}: {e}. Trying Runway...")
                    provider = "runway"
                    clip_path = runway.generate(prompt_text)

                # Save to DB
                clip = VideoClip(
                    script_id=script.id,
                    provider=provider,
                    file_path=str(clip_path),
                    status="completed",
                )
                db.add(clip)
                count += 1
                logger.info(f"Video clip generated for script {script.id} via {provider}")

            except Exception as e:
                logger.error(f"Video generation failed for script {script.id}: {e}")
                # Record failure
                clip = VideoClip(
                    script_id=script.id,
                    provider="none",
                    file_path="",
                    status="failed",
                )
                db.add(clip)
                continue

        db.commit()
        logger.info(f"Generated {count} video clips")

    except Exception as e:
        db.rollback()
        logger.error(f"Video generation orchestration failed: {e}")
        raise
    finally:
        db.close()

    return count


if __name__ == "__main__":
    count = generate_videos()
    print(f"Generated {count} video clips")
