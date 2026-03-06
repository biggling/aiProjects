"""Job 4: Video Rendering
Schedule: Triggered by Job 3
"""
import json
from pathlib import Path
from datetime import datetime
from database.models import SessionLocal, Script, Video
from utils.tts_utils import generate_tts
from utils.video_utils import render_video, generate_thumbnail
from config import VIDEOS_DIR, VIDEO_WIDTH, VIDEO_HEIGHT, get_logger

logger = get_logger("job4_video_rendering")


def run():
    logger.info("=== Job 4: Video Rendering started ===")

    session = SessionLocal()
    rendered = 0

    try:
        scripts = session.query(Script).filter_by(status="assets_ready").limit(10).all()
        logger.info(f"Found {len(scripts)} scripts ready for rendering.")

        for script in scripts:
            try:
                body_data = json.loads(script.body) if script.body else {}
                scene_paths = [Path(p) for p in body_data.get("scene_paths", [])]
                valid_scenes = [p for p in scene_paths if p.exists()]

                if not valid_scenes:
                    logger.warning(f"Script {script.id}: no valid scene images found")
                    continue

                # Generate TTS audio
                audio_path = VIDEOS_DIR / str(script.id) / "voiceover.mp3"
                voiceover = script.voiceover_text or script.hook or "Video content"
                generate_tts(voiceover, audio_path, language=script.language or "en")

                if not audio_path.exists():
                    logger.error(f"TTS generation failed for script {script.id}")
                    continue

                # Render video
                output_path = VIDEOS_DIR / str(script.id) / "final.mp4"
                render_video(
                    scene_images=valid_scenes,
                    audio_path=audio_path,
                    output_path=output_path,
                    hook_text=script.hook or "",
                )

                if not output_path.exists():
                    logger.error(f"Video render failed for script {script.id}")
                    continue

                # Generate thumbnail
                thumbnail_path = generate_thumbnail(output_path, script.hook or "")

                # Record in DB
                video = Video(
                    script_id=script.id,
                    file_path=str(output_path),
                    thumbnail_path=str(thumbnail_path),
                    resolution=f"{VIDEO_WIDTH}x{VIDEO_HEIGHT}",
                    status="ready",
                    created_at=datetime.utcnow(),
                )
                session.add(video)
                script.status = "rendered"
                rendered += 1
                logger.info(f"Video rendered: {output_path}")

            except Exception as e:
                logger.error(f"Rendering failed for script {script.id}: {e}")

        session.commit()
        logger.info(f"=== Job 4 complete — {rendered} videos rendered ===")
    except Exception as e:
        session.rollback()
        logger.error(f"Job 4 failed: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    run()
