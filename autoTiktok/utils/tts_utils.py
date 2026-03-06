"""TTS helpers for autoTiktok: ElevenLabs → OpenAI TTS → gTTS fallback."""
from pathlib import Path
from config import OPENAI_API_KEY, ELEVENLABS_API_KEY, get_logger
import openai

logger = get_logger("tts_utils")
_openai = openai.OpenAI(api_key=OPENAI_API_KEY)


def generate_tts(text: str, output_path: Path, language: str = "en") -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if ELEVENLABS_API_KEY:
        try:
            from elevenlabs import ElevenLabs
            client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
            audio = client.text_to_speech.convert(
                text=text, voice_id="21m00Tcm4TlvDq8ikWAM", model_id="eleven_turbo_v2"
            )
            with open(output_path, "wb") as f:
                for chunk in audio:
                    f.write(chunk)
            return output_path
        except Exception as e:
            logger.warning(f"ElevenLabs failed: {e}")

    if OPENAI_API_KEY:
        try:
            response = _openai.audio.speech.create(model="tts-1", voice="nova", input=text)
            response.stream_to_file(str(output_path))
            return output_path
        except Exception as e:
            logger.warning(f"OpenAI TTS failed: {e}")

    # gTTS fallback
    try:
        from gtts import gTTS
        gTTS(text=text, lang=language).save(str(output_path))
    except Exception as e:
        logger.error(f"gTTS failed: {e}")
    return output_path
