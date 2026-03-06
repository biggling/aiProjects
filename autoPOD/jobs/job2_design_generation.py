"""Job 2: AI Design Generation
Schedule: Daily at 08:00 UTC
"""
import re
import base64
import random
from pathlib import Path
from database.models import SessionLocal, Niche, Design
from utils.ai_utils import generate_design_brief, generate_dalle_image
from utils.image_utils import (
    create_typography_design, download_image, upscale_to_print,
    composite_on_canvas, save_design, validate_design
)
from config import MAX_DESIGNS_PER_DAY, get_logger

logger = get_logger("job2_design_generation")

DESIGN_STYLES = ["typography", "illustrated", "hybrid"]
PRODUCT_TYPES = ["tshirt", "mug", "sticker", "poster"]
COLOR_PALETTES = {
    "dark": ((30, 30, 30), (245, 245, 245)),
    "light": ((255, 255, 255), (40, 40, 40)),
    "vintage": ((245, 235, 200), (80, 40, 20)),
    "pastel": ((255, 220, 240), (80, 60, 100)),
}


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")


def generate_typography_design(niche: str, quote: str, design_id: int) -> Path | None:
    palette_name = random.choice(list(COLOR_PALETTES.keys()))
    bg_color, text_color = COLOR_PALETTES[palette_name]
    try:
        img = create_typography_design(quote, text_color=text_color, bg_color=bg_color)
        return save_design(img, slugify(niche), design_id)
    except Exception as e:
        logger.error(f"Typography design failed for '{niche}': {e}")
        return None


def generate_ai_design(niche: str, dalle_prompt: str, design_id: int) -> Path | None:
    try:
        url = generate_dalle_image(dalle_prompt)
        img = download_image(url)
        img = upscale_to_print(img)
        img = composite_on_canvas(img)
        return save_design(img, slugify(niche), design_id)
    except Exception as e:
        logger.error(f"DALL-E design failed for '{niche}': {e}")
        return None


def run():
    logger.info("=== Job 2: Design Generation started ===")

    session = SessionLocal()
    try:
        # Get active niches without enough designs
        niches = session.query(Niche).filter_by(status="active").all()
        logger.info(f"Found {len(niches)} active niches.")

        daily_count = 0
        for niche_row in niches:
            if daily_count >= MAX_DESIGNS_PER_DAY:
                logger.info(f"Daily limit ({MAX_DESIGNS_PER_DAY}) reached.")
                break

            niche = niche_row.niche
            logger.info(f"Generating designs for niche: {niche}")

            try:
                brief = generate_design_brief(niche)
            except Exception as e:
                logger.error(f"Brief generation failed for '{niche}': {e}")
                continue

            # Generate 1 typography + 1 AI design per niche (conserve DALL-E quota)
            for style in ["typography", "illustrated"]:
                if daily_count >= MAX_DESIGNS_PER_DAY:
                    break

                product_type = random.choice(PRODUCT_TYPES)
                design = Design(
                    niche_id=niche_row.id,
                    style=style,
                    product_type=product_type,
                    status="pending",
                )
                session.add(design)
                session.flush()  # get design.id

                file_path = None
                if style == "typography":
                    quote = brief.get("quotes", ["Be Awesome"])[0]
                    file_path = generate_typography_design(niche, quote, design.id)
                elif style == "illustrated":
                    prompts = brief.get("dalle_prompts", [])
                    if prompts:
                        file_path = generate_ai_design(niche, prompts[0], design.id)

                if file_path and validate_design(file_path):
                    design.file_path = str(file_path)
                    design.status = "ready"
                    design.dalle_prompt = brief.get("dalle_prompts", [""])[0] if style == "illustrated" else ""
                    daily_count += 1
                    logger.info(f"Design saved: {file_path}")
                else:
                    design.status = "rejected"
                    logger.warning(f"Design rejected for niche '{niche}' style '{style}'")

        session.commit()
        logger.info(f"=== Job 2 complete — {daily_count} designs generated ===")
    except Exception as e:
        session.rollback()
        logger.error(f"Job 2 failed: {e}")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    run()
