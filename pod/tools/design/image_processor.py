import os

from PIL import Image
from rembg import remove
from sqlalchemy import select

from tools.shared.db import get_session
from tools.shared.models import Design
from tools.shared.logger import get_logger

logger = get_logger("image_processor")

PROCESSED_DIR = os.path.join("data", "designs", "processed")
TARGET_WIDTH = 4500
TARGET_HEIGHT = 5400


def process_image(raw_path: str, output_path: str) -> bool:
    """Remove background and upscale image to print dimensions."""
    if not os.path.exists(raw_path):
        logger.error(f"Raw image not found: {raw_path}")
        return False

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Step 1: Remove background
    with open(raw_path, "rb") as f:
        input_data = f.read()
    nobg_data = remove(input_data)

    # Step 2: Upscale to print dimensions
    from io import BytesIO
    img = Image.open(BytesIO(nobg_data)).convert("RGBA")
    img = img.resize((TARGET_WIDTH, TARGET_HEIGHT), Image.LANCZOS)

    # Step 3: Save
    img.save(output_path, "PNG")
    return True


def run():
    """Process all generated designs that haven't been processed yet."""
    logger.info("Starting image processing")

    with get_session() as session:
        designs = session.execute(
            select(Design).where(
                Design.status == "generated",
                Design.raw_path.isnot(None),
            )
        ).scalars().all()
        design_data = [(d.id, d.raw_path) for d in designs]

    if not design_data:
        logger.info("No designs to process")
        return "0 designs processed"

    processed = 0
    for design_id, raw_path in design_data:
        output_path = os.path.join(PROCESSED_DIR, f"{design_id}.png")
        try:
            if process_image(raw_path, output_path):
                with get_session() as session:
                    design = session.get(Design, design_id)
                    design.processed_path = output_path
                    design.status = "processed"
                processed += 1
                logger.info(f"  Processed design {design_id}")
        except Exception as e:
            logger.error(f"  Failed design {design_id}: {e}")

    logger.info(f"Processing complete: {processed}/{len(design_data)}")
    return f"{processed} designs processed"
