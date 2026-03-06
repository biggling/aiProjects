"""MoviePy video rendering helpers."""
import io
import random
from pathlib import Path
import requests
from PIL import Image, ImageDraw, ImageFont
from config import (
    VIDEO_WIDTH, VIDEO_HEIGHT, VIDEO_FPS, VIDEO_BITRATE,
    ASSETS_DIR, get_logger
)

logger = get_logger("video_utils")

CAPTION_FONT_SIZE = 60
HOOK_FONT_SIZE = 90


def download_image_to_path(url: str, output_path: Path) -> Path:
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    img = Image.open(io.BytesIO(r.content)).convert("RGB")
    img = resize_to_portrait(img)
    img.save(str(output_path), "PNG")
    return output_path


def resize_to_portrait(img: Image.Image) -> Image.Image:
    """Resize and crop image to 1080x1920 (9:16)."""
    target_w, target_h = VIDEO_WIDTH, VIDEO_HEIGHT
    ratio = max(target_w / img.width, target_h / img.height)
    new_w = int(img.width * ratio)
    new_h = int(img.height * ratio)
    img = img.resize((new_w, new_h), Image.LANCZOS)
    left = (new_w - target_w) // 2
    top = (new_h - target_h) // 2
    return img.crop((left, top, left + target_w, top + target_h))


def add_text_overlay(
    img: Image.Image, text: str, font_size: int = CAPTION_FONT_SIZE,
    color: tuple = (255, 255, 255), shadow: bool = True,
    position: str = "bottom"
) -> Image.Image:
    """Add text overlay to image with optional shadow."""
    draw = ImageDraw.Draw(img)
    try:
        font_path = ASSETS_DIR / "fonts" / "bold.ttf"
        font = ImageFont.truetype(str(font_path), font_size) if font_path.exists() else ImageFont.load_default()
    except Exception:
        font = ImageFont.load_default()

    # Word wrap
    import textwrap
    wrapped = textwrap.fill(text, width=22)
    lines = wrapped.split("\n")
    line_h = font_size + 10
    total_h = line_h * len(lines)

    y = VIDEO_HEIGHT - total_h - 120 if position == "bottom" else 80

    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        text_w = bbox[2] - bbox[0]
        x = (VIDEO_WIDTH - text_w) // 2
        if shadow:
            draw.text((x + 3, y + 3), line, font=font, fill=(0, 0, 0, 180))
        draw.text((x, y), line, font=font, fill=color)
        y += line_h
    return img


def fetch_pexels_image(query: str, orientation: str = "portrait") -> str | None:
    """Return image URL from Pexels API."""
    from config import PEXELS_API_KEY
    if not PEXELS_API_KEY:
        return None
    try:
        r = requests.get(
            "https://api.pexels.com/v1/search",
            headers={"Authorization": PEXELS_API_KEY},
            params={"query": query, "orientation": orientation, "per_page": 5},
            timeout=10,
        )
        photos = r.json().get("photos", [])
        if photos:
            return random.choice(photos)["src"]["large2x"]
    except Exception as e:
        logger.warning(f"Pexels fetch failed: {e}")
    return None


def render_video(
    scene_images: list[Path],
    audio_path: Path,
    output_path: Path,
    hook_text: str = "",
    music_path: Path | None = None,
    watermark_text: str = "",
) -> Path:
    """Assemble scenes + audio into final MP4."""
    try:
        from moviepy.editor import (
            ImageClip, AudioFileClip, concatenate_videoclips,
            CompositeAudioClip, TextClip, CompositeVideoClip
        )
        from pydub import AudioSegment
    except ImportError as e:
        logger.error(f"moviepy/pydub not installed: {e}")
        raise

    audio = AudioFileClip(str(audio_path))
    total_duration = audio.duration
    num_scenes = len(scene_images)
    scene_duration = total_duration / num_scenes if num_scenes > 0 else total_duration

    clips = []
    for i, img_path in enumerate(scene_images):
        clip = ImageClip(str(img_path), duration=scene_duration)
        clips.append(clip)

    video = concatenate_videoclips(clips, method="compose")
    video = video.set_audio(audio)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    video.write_videofile(
        str(output_path),
        fps=VIDEO_FPS,
        bitrate=VIDEO_BITRATE,
        codec="libx264",
        audio_codec="aac",
        verbose=False,
        logger=None,
    )
    audio.close()
    video.close()
    return output_path


def generate_thumbnail(video_path: Path, hook_text: str = "") -> Path:
    """Extract first frame and add hook text for thumbnail."""
    try:
        from moviepy.editor import VideoFileClip
        clip = VideoFileClip(str(video_path))
        frame = clip.get_frame(0.5)
        clip.close()
        img = Image.fromarray(frame)
        if hook_text:
            img = add_text_overlay(img, hook_text, font_size=HOOK_FONT_SIZE, position="bottom")
        thumb_path = video_path.parent / "thumbnail.jpg"
        img.save(str(thumb_path), "JPEG", quality=90)
        return thumb_path
    except Exception as e:
        logger.error(f"Thumbnail generation failed: {e}")
        return video_path
