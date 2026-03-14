import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from sqlalchemy import select

from tools.shared.config import STABILITY_API_KEY
from tools.shared.db import get_session
from tools.shared.models import Prompt, Design
from tools.shared.logger import get_logger

logger = get_logger("image_generator")

BATCH_SIZE = 20
MAX_CONCURRENT = 5
MAX_RETRIES = 3
RAW_DIR = os.path.join("data", "designs", "raw")


def generate_image(prompt_text: str, output_path: str) -> bool:
    """Call Stability AI API to generate an image from a prompt."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    url = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"
    headers = {
        "Authorization": f"Bearer {STABILITY_API_KEY}",
        "Content-Type": "application/json",
        "Accept": "image/png",
    }
    body = {
        "text_prompts": [{"text": prompt_text, "weight": 1}],
        "cfg_scale": 7,
        "height": 1024,
        "width": 1024,
        "steps": 30,
        "samples": 1,
    }

    for attempt in range(MAX_RETRIES):
        try:
            resp = requests.post(url, headers=headers, json=body, timeout=120)
            if resp.status_code == 200:
                with open(output_path, "wb") as f:
                    f.write(resp.content)
                return True
            elif resp.status_code == 429:
                logger.warning(f"Rate limited, waiting 30s (attempt {attempt + 1})")
                time.sleep(30)
            else:
                logger.error(f"API error {resp.status_code}: {resp.text[:200]}")
                time.sleep(5)
        except Exception as e:
            logger.error(f"Request failed (attempt {attempt + 1}): {e}")
            time.sleep(5)

    return False


def process_prompt(prompt_id: int, niche_id: int, prompt_text: str) -> bool:
    """Generate image for a single prompt and update DB."""
    output_path = os.path.join(RAW_DIR, str(niche_id), f"{prompt_id}.png")

    success = generate_image(prompt_text, output_path)

    with get_session() as session:
        design = Design(
            prompt_id=prompt_id,
            niche_id=niche_id,
            raw_path=output_path if success else None,
            status="generated" if success else "failed",
        )
        session.add(design)

    return success


def run():
    """Generate images for pending prompts in batches."""
    logger.info("Starting image generation")

    with get_session() as session:
        prompts = session.execute(
            select(Prompt).where(Prompt.status == "pending").limit(BATCH_SIZE)
        ).scalars().all()
        prompt_data = [(p.id, p.niche_id, p.prompt_text) for p in prompts]

    if not prompt_data:
        logger.info("No pending prompts")
        return "0 images generated"

    generated = 0
    failed = 0

    with ThreadPoolExecutor(max_workers=MAX_CONCURRENT) as executor:
        futures = {
            executor.submit(process_prompt, pid, nid, text): pid
            for pid, nid, text in prompt_data
        }
        for future in as_completed(futures):
            pid = futures[future]
            try:
                if future.result():
                    generated += 1
                else:
                    failed += 1
            except Exception as e:
                logger.error(f"Prompt {pid} exception: {e}")
                failed += 1

    # Mark processed prompts
    with get_session() as session:
        for pid, _, _ in prompt_data:
            prompt = session.get(Prompt, pid)
            if prompt:
                prompt.status = "generated"

    logger.info(f"Image generation complete: {generated} generated, {failed} failed")
    return f"{generated} images generated, {failed} failed"
