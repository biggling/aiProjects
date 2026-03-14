"""Batch-render MP3 voiceovers from scripts using ElevenLabs."""

import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from dotenv import load_dotenv
import httpx
from loguru import logger
from mutagen.mp3 import MP3

from modules.01_research.db import SessionLocal, init_db
from modules.02_scriptgen.models import Script
from modules.03_voiceover.models import Voiceover

load_dotenv()

AUDIO_DIR = Path("data/assets/audio")
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

MAX_RETRIES = 3
RETRY_BACKOFF = 5


def render_voiceovers() -> int:
    """Render voiceovers for all scripts without one. Returns count rendered."""
    init_db()
    db = SessionLocal()
    count = 0

    try:
        # Find scripts without voiceovers
        existing_script_ids = [v.script_id for v in db.query(Voiceover.script_id).all()]
        scripts = db.query(Script).filter(Script.id.notin_(existing_script_ids) if existing_script_ids else True).all()

        if not scripts:
            logger.info("No scripts pending voiceover")
            return 0

        api_key = os.getenv("ELEVENLABS_API_KEY", "")
        voice_id = os.getenv("ELEVENLABS_VOICE_ID", "")

        for script in scripts:
            try:
                text = f"{script.hook} {script.body} {script.cta}"
                output_path = AUDIO_DIR / f"voice_{script.id}.mp3"

                _synthesize_speech(api_key, voice_id, text, output_path)

                # Get duration
                duration = _get_duration(output_path)

                # Save to DB
                voiceover = Voiceover(
                    script_id=script.id,
                    file_path=str(output_path),
                    duration_sec=duration,
                )
                db.add(voiceover)
                count += 1
                logger.info(f"Voiceover for script {script.id}: {duration:.1f}s")

            except Exception as e:
                logger.error(f"Failed voiceover for script {script.id}: {e}")
                continue

        db.commit()
        logger.info(f"Rendered {count} voiceovers")

    except Exception as e:
        db.rollback()
        logger.error(f"Voiceover rendering failed: {e}")
        raise
    finally:
        db.close()

    return count


def _synthesize_speech(api_key: str, voice_id: str, text: str, output_path: Path) -> None:
    """Call ElevenLabs TTS API with retry logic."""
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json",
    }
    payload = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.4,
            "similarity_boost": 0.8,
            "style": 0.3,
        },
    }

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            with httpx.Client(timeout=60) as client:
                response = client.post(url, json=payload, headers=headers)
                response.raise_for_status()
                output_path.write_bytes(response.content)
                return
        except Exception as e:
            logger.warning(f"ElevenLabs attempt {attempt}/{MAX_RETRIES} failed: {e}")
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_BACKOFF * attempt)
            else:
                raise


def _get_duration(file_path: Path) -> float:
    """Get MP3 duration in seconds."""
    try:
        audio = MP3(str(file_path))
        return audio.info.length
    except Exception:
        return 0.0


if __name__ == "__main__":
    count = render_voiceovers()
    print(f"Rendered {count} voiceovers")
