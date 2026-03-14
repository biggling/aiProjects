"""Auto-editor — assembles final 9:16 TikTok-ready MP4 from clips + voice + captions."""

import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from dotenv import load_dotenv
from loguru import logger

from modules.01_research.db import SessionLocal, init_db
from modules.02_scriptgen.models import Script
from modules.03_voiceover.models import Voiceover
from modules.04_videogen.models import VideoClip
from modules.05_editor.models import EditedVideo
from modules.05_editor.caption_generator import generate_captions
from modules.05_editor.thumbnail import generate_thumbnail

load_dotenv()

OUTPUT_DIR = Path("data/output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

MAX_DURATION_SEC = 60
MAX_FILE_SIZE_MB = 100


def edit_videos() -> int:
    """Edit all videos that have clips and voiceover but no edited version. Returns count."""
    init_db()
    db = SessionLocal()
    count = 0

    try:
        existing_script_ids = [e.script_id for e in db.query(EditedVideo.script_id).all()]

        # Find scripts with both voiceover and video clips ready
        scripts_with_voice = db.query(Voiceover.script_id).all()
        voice_ids = {v.script_id for v in scripts_with_voice}

        scripts_with_clips = (
            db.query(VideoClip.script_id)
            .filter(VideoClip.status == "completed")
            .all()
        )
        clip_ids = {c.script_id for c in scripts_with_clips}

        ready_ids = voice_ids & clip_ids
        if existing_script_ids:
            ready_ids -= set(existing_script_ids)

        if not ready_ids:
            logger.info("No videos ready for editing")
            return 0

        for script_id in ready_ids:
            try:
                script = db.query(Script).filter(Script.id == script_id).first()
                voiceover = db.query(Voiceover).filter(Voiceover.script_id == script_id).first()
                clips = (
                    db.query(VideoClip)
                    .filter(VideoClip.script_id == script_id, VideoClip.status == "completed")
                    .all()
                )

                if not script or not voiceover or not clips:
                    continue

                voice_path = Path(voiceover.file_path)
                clip_paths = [Path(c.file_path) for c in clips]
                output_path = OUTPUT_DIR / f"video_{script_id}.mp4"

                # Generate captions from voiceover
                try:
                    ass_path = generate_captions(voice_path, script_id)
                except Exception as e:
                    logger.warning(f"Caption generation failed for script {script_id}: {e}")
                    ass_path = None

                # Assemble video
                _assemble_video(
                    clip_paths=clip_paths,
                    voice_path=voice_path,
                    ass_path=ass_path,
                    output_path=output_path,
                    target_duration=voiceover.duration_sec,
                )

                # Validate output
                duration = _get_video_duration(output_path)
                file_size_mb = output_path.stat().st_size / (1024 * 1024)

                if duration > MAX_DURATION_SEC:
                    logger.warning(f"Video {script_id} exceeds {MAX_DURATION_SEC}s ({duration:.1f}s)")
                if file_size_mb > MAX_FILE_SIZE_MB:
                    logger.warning(f"Video {script_id} exceeds {MAX_FILE_SIZE_MB}MB ({file_size_mb:.1f}MB)")

                # Generate thumbnail
                product_name = ""
                if script.product_id:
                    product_name = script.hook[:50]  # Use hook as fallback
                thumb_path = generate_thumbnail(output_path, script_id, product_name)

                # Save to DB
                edited = EditedVideo(
                    script_id=script_id,
                    file_path=str(output_path),
                    thumbnail_path=str(thumb_path),
                    duration_sec=duration,
                    status="pending_review",
                )
                db.add(edited)
                count += 1
                logger.info(f"Edited video {script_id}: {duration:.1f}s, {file_size_mb:.1f}MB")

            except Exception as e:
                logger.error(f"Editing failed for script {script_id}: {e}")
                continue

        db.commit()
        logger.info(f"Edited {count} videos")

    except Exception as e:
        db.rollback()
        logger.error(f"Video editing failed: {e}")
        raise
    finally:
        db.close()

    return count


def _assemble_video(
    clip_paths: list[Path],
    voice_path: Path,
    ass_path: Path | None,
    output_path: Path,
    target_duration: float,
) -> None:
    """Assemble final video using FFmpeg."""
    # Create concat file for video clips
    concat_path = output_path.parent / f"concat_{output_path.stem}.txt"
    with open(concat_path, "w") as f:
        for clip_path in clip_paths:
            f.write(f"file '{clip_path.resolve()}'\n")

    # Build FFmpeg command
    filter_parts = []

    # Scale and pad to 1080x1920
    filter_parts.append(
        "[0:v]scale=1080:1920:force_original_aspect_ratio=decrease,"
        "pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black,"
        "fps=30,fade=in:0:9[v]"  # 0.3s fade-in at 30fps
    )

    # Add captions if available
    if ass_path and ass_path.exists():
        filter_parts[-1] = filter_parts[-1].replace("[v]", "[v0]")
        filter_parts.append(f"[v0]ass='{ass_path}'[v]")

    filter_complex = ";".join(filter_parts)

    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", str(concat_path),
        "-i", str(voice_path),
        "-filter_complex", filter_complex,
        "-map", "[v]",
        "-map", "1:a",
        "-c:v", "libx264", "-preset", "medium", "-crf", "23",
        "-c:a", "aac", "-b:a", "128k",
        "-t", str(min(target_duration, MAX_DURATION_SEC)),
        "-movflags", "+faststart",
        str(output_path),
    ]

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    if result.returncode != 0:
        logger.error(f"FFmpeg error: {result.stderr[-500:]}")
        raise RuntimeError(f"FFmpeg failed with return code {result.returncode}")

    # Clean up concat file
    concat_path.unlink(missing_ok=True)


def _get_video_duration(video_path: Path) -> float:
    """Get video duration using FFprobe."""
    cmd = [
        "ffprobe", "-v", "quiet",
        "-print_format", "json",
        "-show_format",
        str(video_path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    if result.returncode == 0:
        data = json.loads(result.stdout)
        return float(data.get("format", {}).get("duration", 0))
    return 0.0


if __name__ == "__main__":
    count = edit_videos()
    print(f"Edited {count} videos")
