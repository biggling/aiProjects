"""Auto cover frame extractor and thumbnail generator."""

import subprocess
from pathlib import Path

from loguru import logger
from PIL import Image, ImageDraw, ImageFont


OUTPUT_DIR = Path("data/output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def generate_thumbnail(video_path: Path, script_id: int, product_name: str = "") -> Path:
    """Extract frame at 1.5s and overlay product name text."""
    thumb_path = OUTPUT_DIR / f"thumb_{script_id}.jpg"

    # Extract frame at 1.5 seconds
    _extract_frame(video_path, thumb_path, timestamp=1.5)

    # Overlay text if product name provided
    if product_name:
        _overlay_text(thumb_path, product_name)

    logger.info(f"Thumbnail generated: {thumb_path}")
    return thumb_path


def _extract_frame(video_path: Path, output_path: Path, timestamp: float = 1.5) -> None:
    """Extract a single frame from video using FFmpeg."""
    cmd = [
        "ffmpeg", "-y",
        "-ss", str(timestamp),
        "-i", str(video_path),
        "-vframes", "1",
        "-q:v", "2",
        str(output_path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    if result.returncode != 0:
        logger.warning(f"Frame extraction failed: {result.stderr}")
        # Create placeholder thumbnail
        img = Image.new("RGB", (1080, 1920), color=(30, 30, 30))
        img.save(str(output_path), quality=90)


def _overlay_text(thumb_path: Path, text: str) -> None:
    """Overlay product name text on thumbnail."""
    img = Image.open(str(thumb_path))
    draw = ImageDraw.Draw(img)

    # Try to use a bold font, fallback to default
    font_size = 60
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
    except (OSError, IOError):
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except (OSError, IOError):
            font = ImageFont.load_default()

    # Position text in bottom third
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (img.width - text_width) // 2
    y = img.height - (img.height // 3)

    # Draw outline
    outline_color = "black"
    for dx in [-3, 0, 3]:
        for dy in [-3, 0, 3]:
            draw.text((x + dx, y + dy), text, font=font, fill=outline_color)

    # Draw text
    draw.text((x, y), text, font=font, fill="white")

    img.save(str(thumb_path), quality=90)
