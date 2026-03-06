"""Job 3: Media Asset Generation
Schedule: Triggered by Job 2
"""
import io
import json
import random
from pathlib import Path
import requests
from PIL import Image
from database.models import SessionLocal, Script
from utils.ai_utils import generate_dalle_image
from utils.video_utils import download_image_to_path, resize_to_portrait, add_text_overlay, fetch_pexels_image
from config import VIDEOS_DIR, get_logger

logger = get_logger("job3_media_assembly")


def get_scene_image(scene_text: str, script_id: int, scene_idx: int) -> Path | None:
    output_path = VIDEOS_DIR / str(script_id) / f"scene_{scene_idx}.png"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Try Pexels first (free)
    pexels_url = fetch_pexels_image(scene_text[:50])
    if pexels_url:
        try:
            return download_image_to_path(pexels_url, output_path)
        except Exception as e:
            logger.warning(f"Pexels download failed: {e}")

    # Fall back to DALL-E 3
    try:
        dalle_prompt = (
            f"Vertical 9:16 photo-realistic image of {scene_text}, "
            "professional photography, vibrant colors, no text, social media video background"
        )
        url = generate_dalle_image(dalle_prompt)
        return download_image_to_path(url, output_path)
    except Exception as e:
        logger.error(f"DALL-E failed for scene {scene_idx}: {e}")

    return None


def run():
    logger.info("=== Job 3: Media Assembly started ===")

    session = SessionLocal()
    assembled = 0

    try:
        scripts = session.query(Script).filter_by(status="pending").limit(20).all()
        logger.info(f"Found {len(scripts)} scripts needing media.")

        for script in scripts:
            try:
                body_scenes = json.loads(script.body) if script.body else [script.hook or "video scene"]
                scene_paths = []

                for i, scene_text in enumerate(body_scenes):
                    path = get_scene_image(scene_text, script.id, i)
                    if path:
                        scene_paths.append(path)

                if scene_paths:
                    # Store scene paths in script body (update)
                    script.body = json.dumps({
                        "scenes_text": body_scenes,
                        "scene_paths": [str(p) for p in scene_paths],
                    })
                    script.status = "assets_ready"
                    assembled += 1
                    logger.info(f"Script {script.id}: {len(scene_paths)} scenes assembled")
                else:
                    logger.warning(f"Script {script.id}: no scenes assembled")

            except Exception as e:
                logger.error(f"Media assembly failed for script {script.id}: {e}")

        session.commit()
        logger.info(f"=== Job 3 complete — {assembled} scripts with media ===")
    except Exception as e:
        session.rollback()
        logger.error(f"Job 3 failed: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    run()
