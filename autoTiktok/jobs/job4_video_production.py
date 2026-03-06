"""Job 4: Video Production
Schedule: Every 6 hours (after Job 3)
"""
import io
import json
import random
from pathlib import Path
import requests
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from database.models import SessionLocal, Script, Video, Niche
from utils.ai_utils import generate_dalle_scene
from config import VIDEOS_DIR, ASSETS_DIR, VIDEO_WIDTH, VIDEO_HEIGHT, PEXELS_API_KEY, get_logger

logger = get_logger("job4_video_production")


def fetch_product_image(product_url: str) -> bytes | None:
    """Try to download product image from product URL."""
    try:
        r = requests.get(product_url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        soup_module = __import__("bs4", fromlist=["BeautifulSoup"])
        soup = soup_module.BeautifulSoup(r.text, "html.parser")
        img_tag = soup.find("meta", property="og:image")
        if img_tag:
            img_r = requests.get(img_tag["content"], timeout=10)
            return img_r.content
    except Exception:
        pass
    return None


def fetch_pexels(query: str) -> bytes | None:
    if not PEXELS_API_KEY:
        return None
    try:
        r = requests.get(
            "https://api.pexels.com/v1/search",
            headers={"Authorization": PEXELS_API_KEY},
            params={"query": query, "orientation": "portrait", "per_page": 3},
            timeout=10,
        )
        photos = r.json().get("photos", [])
        if photos:
            img_r = requests.get(random.choice(photos)["src"]["large2x"], timeout=15)
            return img_r.content
    except Exception:
        pass
    return None


def image_bytes_to_pil(data: bytes) -> Image.Image:
    img = Image.open(io.BytesIO(data)).convert("RGB")
    # Resize to 1080x1920
    ratio = max(VIDEO_WIDTH / img.width, VIDEO_HEIGHT / img.height)
    img = img.resize((int(img.width * ratio), int(img.height * ratio)), Image.LANCZOS)
    left = (img.width - VIDEO_WIDTH) // 2
    top = (img.height - VIDEO_HEIGHT) // 2
    return img.crop((left, top, left + VIDEO_WIDTH, top + VIDEO_HEIGHT))


def add_hook_overlay(img: Image.Image, text: str) -> Image.Image:
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype(str(ASSETS_DIR / "fonts" / "bold.ttf"), 72)
    except Exception:
        font = ImageFont.load_default()

    import textwrap
    lines = textwrap.fill(text, width=18).split("\n")
    y = VIDEO_HEIGHT - 250
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        x = (VIDEO_WIDTH - (bbox[2] - bbox[0])) // 2
        draw.text((x + 2, y + 2), line, font=font, fill=(0, 0, 0))
        draw.text((x, y), line, font=font, fill=(255, 255, 255))
        y += 85
    return img


def generate_simple_video(script: Script, product: Niche) -> Path | None:
    """Generate a simple slideshow video with TTS voiceover."""
    try:
        from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
        from utils.tts_utils import generate_tts
    except ImportError as e:
        logger.error(f"moviepy not installed: {e}")
        return None

    video_dir = VIDEOS_DIR / str(script.id)
    video_dir.mkdir(parents=True, exist_ok=True)

    # Get scene texts
    body_scenes = json.loads(script.body) if script.body else ["product intro", "product demo", "CTA"]
    if isinstance(body_scenes, dict):
        body_scenes = body_scenes.get("scenes_text", ["product video"])

    # Generate scene images
    scene_paths = []
    for i, scene_text in enumerate(body_scenes[:3]):
        scene_path = video_dir / f"scene_{i}.png"
        img_data = (
            fetch_product_image(product.product_url) if product.product_url else None
            or fetch_pexels(f"{product.niche} {scene_text[:30]}")
        )

        if img_data:
            img = image_bytes_to_pil(img_data)
        else:
            # Create plain colored background as fallback
            img = Image.new("RGB", (VIDEO_WIDTH, VIDEO_HEIGHT), color=(30, 30, 50))

        if i == 0 and script.hook:
            img = add_hook_overlay(img, script.hook)
        img.save(str(scene_path), "PNG")
        scene_paths.append(scene_path)

    if not scene_paths:
        return None

    # Generate TTS
    audio_path = video_dir / "voiceover.mp3"
    voiceover = script.voiceover_text or f"{script.hook} {script.cta}"
    generate_tts(voiceover, audio_path)
    if not audio_path.exists():
        return None

    # Render video
    audio = AudioFileClip(str(audio_path))
    dur_per_scene = audio.duration / len(scene_paths)
    clips = [ImageClip(str(p), duration=dur_per_scene) for p in scene_paths]
    video = concatenate_videoclips(clips).set_audio(audio)

    output_path = video_dir / "final.mp4"
    video.write_videofile(str(output_path), fps=30, codec="libx264", audio_codec="aac", verbose=False, logger=None)
    audio.close()
    video.close()

    return output_path


def run():
    logger.info("=== Job 4: Video Production started ===")

    session = SessionLocal()
    rendered = 0

    try:
        scripts = session.query(Script).filter_by(status="approved").limit(5).all()
        logger.info(f"Found {len(scripts)} approved scripts for production.")

        for script in scripts:
            product = session.query(Niche).get(script.product_id)
            if not product:
                continue

            try:
                output_path = generate_simple_video(script, product)
                if output_path and output_path.exists():
                    video = Video(
                        script_id=script.id,
                        file_path=str(output_path),
                        duration=30.0,
                        status="ready",
                        created_at=datetime.utcnow(),
                    )
                    session.add(video)
                    script.status = "rendered"
                    rendered += 1
                    logger.info(f"Video rendered: {output_path}")
                else:
                    logger.warning(f"Video render returned None for script {script.id}")
            except Exception as e:
                logger.error(f"Production failed for script {script.id}: {e}")

        session.commit()
        logger.info(f"=== Job 4 complete — {rendered} videos rendered ===")
    except Exception as e:
        session.rollback()
        logger.error(f"Job 4 failed: {e}")
    finally:
        session.close()


def generate_tts(text: str, output_path: Path, language: str = "en") -> Path:
    """TTS helper — import from utils if available."""
    try:
        from utils.tts_utils import generate_tts as _tts
        return _tts(text, output_path, language)
    except Exception as e:
        logger.warning(f"TTS import failed, using gTTS: {e}")
        try:
            from gtts import gTTS
            tts = gTTS(text=text, lang=language)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            tts.save(str(output_path))
        except Exception as e2:
            logger.error(f"gTTS also failed: {e2}")
    return output_path


if __name__ == "__main__":
    run()
