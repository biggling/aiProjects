"""Pillow helpers: typography designs, mockup compositing, upscaling."""
import io
import textwrap
from pathlib import Path
import requests
from PIL import Image, ImageDraw, ImageFont
from config import DESIGNS_DIR, ASSETS_DIR, get_logger

logger = get_logger("image_utils")

CANVAS_W, CANVAS_H = 4500, 5400
CANVAS_DPI = 300
FONTS_DIR = ASSETS_DIR / "fonts"


def create_typography_design(
    text: str,
    font_name: str = "default",
    text_color: tuple = (30, 30, 30),
    bg_color: tuple = (255, 255, 255),
) -> Image.Image:
    """Create a print-ready typography design (4500x5400px)."""
    img = Image.new("RGB", (CANVAS_W, CANVAS_H), color=bg_color)
    draw = ImageDraw.Draw(img)

    font_path = FONTS_DIR / f"{font_name}.ttf"
    font_size = 280
    try:
        font = ImageFont.truetype(str(font_path), font_size) if font_path.exists() else ImageFont.load_default()
    except Exception:
        font = ImageFont.load_default()

    # Word-wrap to fit canvas
    wrapped = textwrap.fill(text, width=20)
    lines = wrapped.split("\n")

    # Center vertically
    line_height = font_size + 40
    total_height = line_height * len(lines)
    y = (CANVAS_H - total_height) // 2

    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        text_w = bbox[2] - bbox[0]
        x = (CANVAS_W - text_w) // 2
        draw.text((x, y), line, fill=text_color, font=font)
        y += line_height

    return img


def download_image(url: str) -> Image.Image:
    """Download image from URL and return PIL Image."""
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return Image.open(io.BytesIO(response.content)).convert("RGBA")


def upscale_to_print(img: Image.Image, target_w: int = CANVAS_W) -> Image.Image:
    """Upscale image to print resolution using Lanczos."""
    ratio = target_w / img.width
    new_h = int(img.height * ratio)
    return img.resize((target_w, new_h), Image.LANCZOS)


def composite_on_canvas(
    design: Image.Image,
    canvas_size: tuple = (CANVAS_W, CANVAS_H),
    bg_color: tuple = (255, 255, 255),
) -> Image.Image:
    """Center design on a white print canvas."""
    canvas = Image.new("RGB", canvas_size, bg_color)
    # Scale design to fit with 5% padding
    max_w = int(canvas_size[0] * 0.90)
    max_h = int(canvas_size[1] * 0.90)
    design.thumbnail((max_w, max_h), Image.LANCZOS)
    if design.mode == "RGBA":
        canvas.paste(design, ((canvas_size[0] - design.width) // 2,
                               (canvas_size[1] - design.height) // 2),
                     mask=design.split()[3])
    else:
        canvas.paste(design, ((canvas_size[0] - design.width) // 2,
                               (canvas_size[1] - design.height) // 2))
    return canvas


def apply_design_to_mockup(
    design_path: Path,
    mockup_path: Path,
    output_path: Path,
    position: tuple = (800, 600),
    size: tuple = (900, 900),
) -> Path:
    """Composite design onto a product mockup template."""
    mockup = Image.open(mockup_path).convert("RGBA")
    design = Image.open(design_path).convert("RGBA")
    design = design.resize(size, Image.LANCZOS)
    mockup.paste(design, position, mask=design.split()[3])
    result = mockup.convert("RGB")
    result.save(str(output_path), "PNG", dpi=(72, 72))
    return output_path


def save_design(img: Image.Image, niche_slug: str, design_id: int) -> Path:
    """Save design PNG to designs/{niche_slug}/{design_id}.png"""
    niche_dir = DESIGNS_DIR / niche_slug
    niche_dir.mkdir(parents=True, exist_ok=True)
    path = niche_dir / f"{design_id}.png"
    img.save(str(path), "PNG", dpi=(CANVAS_DPI, CANVAS_DPI))
    return path


def validate_design(path: Path) -> bool:
    """Validate design meets POD requirements."""
    try:
        img = Image.open(path)
        if img.width < 4500 or img.height < 5400:
            logger.warning(f"{path}: too small ({img.width}x{img.height})")
            return False
        if img.mode not in ("RGB", "RGBA"):
            logger.warning(f"{path}: invalid color mode {img.mode}")
            return False
        size_mb = path.stat().st_size / 1_000_000
        if size_mb > 200:
            logger.warning(f"{path}: too large ({size_mb:.1f}MB)")
            return False
        return True
    except Exception as e:
        logger.error(f"Design validation failed for {path}: {e}")
        return False
