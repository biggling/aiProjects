"""Image generator — supports Gemini (Imagen 3), Stability AI, and DALL-E 3.

Backend selection via IMAGE_BACKEND env var (default: "auto"):
  "auto"      — Gemini first, fallback to Stability AI, then DALL-E 3
  "gemini"    — Gemini Imagen 3 / Flash image gen only
  "stability" — Stability AI SDXL only
  "dalle"     — DALL-E 3 only

Per-prompt override: set Prompt.image_backend to any of the above values.
Prompt-level preference overrides the global IMAGE_BACKEND setting.
"""
import base64
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from sqlalchemy import select

from tools.shared.config import (
    GEMINI_API_KEY, GEMINI_IMAGE_MODEL,
    STABILITY_API_KEY, OPENAI_API_KEY,
    IMAGE_BACKEND,
)
from tools.shared.db import get_session
from tools.shared.models import Prompt, Design
from tools.shared.logger import get_logger

logger = get_logger("image_generator")

BATCH_SIZE = 20
MAX_CONCURRENT = 5
MAX_RETRIES = 3
RAW_DIR = os.path.join("data", "designs", "raw")


# ── Gemini / Imagen 3 ────────────────────────────────────────────────────────

def _generate_gemini(prompt_text: str, output_path: str) -> dict | None:
    """Generate image via Google Imagen 3 or Gemini 2.0 Flash image gen.

    Returns generation_params dict on success, None on failure.
    Imagen 3 ("imagen-3.0-generate-002") gives the best quality for
    clean transparent-background POD art.
    """
    if not GEMINI_API_KEY:
        return None

    try:
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=GEMINI_API_KEY)

        if GEMINI_IMAGE_MODEL.startswith("imagen"):
            # Imagen 3 — dedicated image generation model (highest fidelity)
            response = client.models.generate_images(
                model=GEMINI_IMAGE_MODEL,
                prompt=prompt_text,
                config=types.GenerateImagesConfig(
                    number_of_images=1,
                    aspect_ratio="1:1",
                    output_mime_type="image/png",
                ),
            )
            image_bytes = response.generated_images[0].image.image_bytes
        else:
            # Gemini Flash native image output
            response = client.models.generate_content(
                model=GEMINI_IMAGE_MODEL,
                contents=prompt_text,
                config=types.GenerateContentConfig(
                    response_modalities=["IMAGE"],
                ),
            )
            part = response.candidates[0].content.parts[0]
            inline = part.inline_data
            image_bytes = inline.data  # already bytes — no base64 decode needed
            # Adjust extension to match actual mime type
            if inline.mime_type == "image/jpeg":
                output_path = os.path.splitext(output_path)[0] + ".jpg"

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(image_bytes)
        return {"model": GEMINI_IMAGE_MODEL, "aspect_ratio": "1:1", "backend": "gemini"}

    except Exception as e:
        logger.warning(f"Gemini image generation failed: {e}")
        return None


# ── Stability AI ─────────────────────────────────────────────────────────────

def _generate_stability(prompt_text: str, output_path: str) -> dict | None:
    """Generate image via Stability AI SDXL 1.0.

    Returns generation_params dict on success, None on failure.
    """
    if not STABILITY_API_KEY:
        return None

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
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                with open(output_path, "wb") as f:
                    f.write(resp.content)
                return {
                    "model": "stable-diffusion-xl-1024-v1-0",
                    "cfg_scale": 7, "steps": 30, "backend": "stability",
                }
            elif resp.status_code == 429:
                logger.warning(f"Stability rate limited, waiting 30s (attempt {attempt + 1})")
                time.sleep(30)
            else:
                logger.error(f"Stability API error {resp.status_code}: {resp.text[:200]}")
                time.sleep(5)
        except Exception as e:
            logger.error(f"Stability request failed (attempt {attempt + 1}): {e}")
            time.sleep(5)

    return None


# ── DALL-E 3 ─────────────────────────────────────────────────────────────────

def _generate_dalle(prompt_text: str, output_path: str) -> dict | None:
    """Generate image via DALL-E 3.

    Returns generation_params dict on success, None on failure.
    """
    if not OPENAI_API_KEY:
        return None

    try:
        import openai
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt_text,
            size="1024x1024",
            quality="standard",
            n=1,
            response_format="b64_json",
        )
        image_data = base64.b64decode(response.data[0].b64_json)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(image_data)
        return {"model": "dall-e-3", "size": "1024x1024", "quality": "standard", "backend": "dalle"}
    except Exception as e:
        logger.warning(f"DALL-E image generation failed: {e}")
        return None


# ── Backend router ────────────────────────────────────────────────────────────

def generate_image(
    prompt_text: str,
    output_path: str,
    preferred_backend: str | None = None,
) -> tuple[bool, str, dict]:
    """Route to the right image backend.

    Returns (success, backend_used, generation_params).
    "auto" priority: Gemini → Stability → DALL-E (cheapest-first, best-first).
    """
    backend = (preferred_backend or IMAGE_BACKEND or "auto").lower()

    if backend == "gemini":
        sequence = ["gemini"]
    elif backend == "stability":
        sequence = ["stability"]
    elif backend == "dalle":
        sequence = ["dalle"]
    else:  # "auto"
        sequence = ["gemini", "stability", "dalle"]

    for name in sequence:
        if name == "gemini":
            params = _generate_gemini(prompt_text, output_path)
        elif name == "stability":
            params = _generate_stability(prompt_text, output_path)
        else:
            params = _generate_dalle(prompt_text, output_path)

        if params is not None:
            logger.info(f"Image generated via {name}: {output_path}")
            return True, name, params

    logger.error(f"All backends failed for: {prompt_text[:80]}...")
    return False, "none", {}


# ── Pipeline entrypoint ───────────────────────────────────────────────────────

def process_prompt(
    prompt_id: int,
    niche_id: int,
    prompt_text: str,
    preferred_backend: str | None,
) -> bool:
    """Generate image for one prompt and write a Design row."""
    output_path = os.path.join(RAW_DIR, str(niche_id), f"{prompt_id}.png")
    success, backend_used, params = generate_image(prompt_text, output_path, preferred_backend)

    with get_session() as session:
        design = Design(
            prompt_id=prompt_id,
            niche_id=niche_id,
            raw_path=output_path if success else None,
            image_backend=backend_used,
            generation_params=params or None,
            status="generated" if success else "failed",
        )
        session.add(design)

    return success


def run():
    """Generate images for all pending prompts in batches."""
    logger.info(f"Starting image generation (global backend: {IMAGE_BACKEND})")

    with get_session() as session:
        prompts = session.execute(
            select(Prompt).where(Prompt.status == "pending").limit(BATCH_SIZE)
        ).scalars().all()
        prompt_data = [
            (p.id, p.niche_id, p.prompt_text, p.image_backend)
            for p in prompts
        ]

    if not prompt_data:
        logger.info("No pending prompts")
        return "0 images generated"

    generated = 0
    failed = 0

    with ThreadPoolExecutor(max_workers=MAX_CONCURRENT) as executor:
        futures = {
            executor.submit(process_prompt, pid, nid, text, pref): pid
            for pid, nid, text, pref in prompt_data
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

    with get_session() as session:
        for pid, _, _, _ in prompt_data:
            prompt = session.get(Prompt, pid)
            if prompt:
                prompt.status = "generated"

    summary = f"{generated} images generated, {failed} failed"
    logger.info(f"Image generation complete: {summary}")
    return summary
