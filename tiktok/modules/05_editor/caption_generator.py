"""Generate styled captions from voiceover audio using Whisper."""

import os
from pathlib import Path

from loguru import logger
from openai import OpenAI


CAPTIONS_DIR = Path("data/assets/captions")
CAPTIONS_DIR.mkdir(parents=True, exist_ok=True)


def generate_captions(audio_path: Path, script_id: int) -> Path:
    """Transcribe audio and generate styled ASS subtitle file."""
    client = OpenAI()

    # Transcribe with Whisper
    with open(audio_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="srt",
            language="th",
        )

    # Save SRT
    srt_path = CAPTIONS_DIR / f"captions_{script_id}.srt"
    srt_path.write_text(transcript)

    # Convert SRT to ASS
    ass_path = CAPTIONS_DIR / f"captions_{script_id}.ass"
    _srt_to_ass(srt_path, ass_path)

    logger.info(f"Captions generated: {ass_path}")
    return ass_path


def _srt_to_ass(srt_path: Path, ass_path: Path) -> None:
    """Convert SRT to ASS format with styled fonts."""
    header = """[Script Info]
Title: TikTok Captions
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,72,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,4,0,2,40,40,120,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

    srt_content = srt_path.read_text()
    events = _parse_srt(srt_content)

    with open(ass_path, "w", encoding="utf-8") as f:
        f.write(header)
        for event in events:
            start = _time_to_ass(event["start"])
            end = _time_to_ass(event["end"])
            text = event["text"].replace("\n", "\\N")
            f.write(f"Dialogue: 0,{start},{end},Default,,0,0,0,,{text}\n")


def _parse_srt(srt_text: str) -> list[dict]:
    """Parse SRT text into list of {start, end, text} dicts."""
    events = []
    blocks = srt_text.strip().split("\n\n")

    for block in blocks:
        lines = block.strip().split("\n")
        if len(lines) >= 3:
            time_line = lines[1]
            parts = time_line.split(" --> ")
            if len(parts) == 2:
                events.append({
                    "start": parts[0].strip(),
                    "end": parts[1].strip(),
                    "text": "\n".join(lines[2:]),
                })

    return events


def _time_to_ass(srt_time: str) -> str:
    """Convert SRT timestamp (00:00:01,500) to ASS format (0:00:01.50)."""
    srt_time = srt_time.replace(",", ".")
    parts = srt_time.split(":")
    if len(parts) == 3:
        h, m, s = parts
        return f"{int(h)}:{m}:{s[:5]}"
    return srt_time
