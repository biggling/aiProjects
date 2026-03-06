"""Text-to-speech helpers: ElevenLabs → OpenAI TTS → gTTS fallback."""
import io
from pathlib import Path
from config import OPENAI_API_KEY, ELEVENLABS_API_KEY, OPENAI_TTS_MODEL, OPENAI_TTS_VOICE, get_logger
import openai

logger = get_logger("tts_utils")
_openai = openai.OpenAI(api_key=OPENAI_API_KEY)


def generate_tts_openai(text: str, output_path: Path, voice: str = OPENAI_TTS_VOICE) -> Path:
    """Generate TTS using OpenAI TTS API."""
    response = _openai.audio.speech.create(
        model=OPENAI_TTS_MODEL,
        voice=voice,
        input=text,
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    response.stream_to_file(str(output_path))
    return output_path


def generate_tts_elevenlabs(text: str, output_path: Path, voice_id: str = "21m00Tcm4TlvDq8ikWAM") -> Path:
    """Generate TTS using ElevenLabs API."""
    try:
        from elevenlabs import ElevenLabs
        client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
        audio = client.text_to_speech.convert(
            text=text,
            voice_id=voice_id,
            model_id="eleven_turbo_v2",
        )
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "wb") as f:
            for chunk in audio:
                f.write(chunk)
        return output_path
    except Exception as e:
        logger.warning(f"ElevenLabs TTS failed: {e}, falling back to OpenAI")
        return generate_tts_openai(text, output_path)


def generate_tts_gtts(text: str, output_path: Path, lang: str = "en") -> Path:
    """Generate TTS using gTTS (free fallback)."""
    from gtts import gTTS
    tts = gTTS(text=text, lang=lang)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    tts.save(str(output_path))
    return output_path


def generate_tts(text: str, output_path: Path, language: str = "en") -> Path:
    """Generate TTS with priority: ElevenLabs → OpenAI → gTTS."""
    if ELEVENLABS_API_KEY:
        return generate_tts_elevenlabs(text, output_path)
    elif OPENAI_API_KEY:
        return generate_tts_openai(text, output_path)
    else:
        return generate_tts_gtts(text, output_path, lang=language)
