"""Prompt generator — produces image-generation prompts with full metadata.

Each Prompt row now stores:
  - prompt_text       : the actual text sent to the image generator
  - keywords          : SEO-ready Etsy search terms derived from the niche
  - design_style      : visual style tag (vintage, minimalist, maximalist, etc.)
  - product_types     : list of applicable POD products
  - target_persona    : buyer persona (gen_x_women, millennials, gen_z)
  - color_palette     : suggested color palette for the design
  - image_backend     : preferred generator (auto / gemini / stability / dalle)
"""
import json

from sqlalchemy import select

from tools.shared.api_clients import get_anthropic
from tools.shared.config import IMAGE_BACKEND
from tools.shared.db import get_session
from tools.shared.models import Niche, Prompt
from tools.shared.logger import get_logger

logger = get_logger("prompt_generator")

PROMPTS_PER_NICHE = 50


def generate_prompts_for_niche(keyword: str) -> list[dict]:
    """Call Claude to generate enriched design prompts for a niche keyword.

    Returns a list of dicts with keys:
      prompt_text, keywords, design_style, product_types,
      target_persona, color_palette
    """
    client = get_anthropic()

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=8000,
        system=(
            "You are a POD design expert and Etsy SEO specialist. "
            "Generate distinct image-generation prompts for print-on-demand products. "
            "Each prompt must be: print-ready, vector-friendly, no text in image, "
            "transparent-background suitable, commercially safe (no copyrighted elements). "
            "Output ONLY a valid JSON array of objects, no markdown."
        ),
        messages=[{
            "role": "user",
            "content": (
                f'Generate {PROMPTS_PER_NICHE} distinct design prompts for the niche: "{keyword}".\n\n'
                "Each object must have these exact keys:\n"
                '  "prompt_text"    : detailed image-gen prompt (describe visuals, style, colors, composition)\n'
                '  "keywords"       : array of 5-8 Etsy SEO keywords for this design\n'
                '  "design_style"   : one of: vintage | minimalist | maximalist | romantic_goth | '
                'cottagecore | dark_academia | retro | modern | watercolor | hand_drawn\n'
                '  "product_types"  : array from: t-shirt | hoodie | mug | tote | poster | sticker | '
                'notebook | phone_case | crossbody_bag | canvas_print\n'
                '  "target_persona" : one of: gen_x_women | millennials | gen_z | universal\n'
                '  "color_palette"  : comma-separated palette suggestion (e.g. "Sage Green, Warm Cream, Terracotta")\n\n'
                "Output JSON array only, no markdown."
            ),
        }],
    )

    text = response.content[0].text.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    return json.loads(text)


def run():
    """Generate enriched prompts for top 10 niches by final_score."""
    logger.info("Starting prompt generation")

    with get_session() as session:
        niches = session.execute(
            select(Niche)
            .where(Niche.status == "active")
            .order_by(Niche.final_score.desc())
            .limit(10)
        ).scalars().all()
        niche_data = [(n.id, n.keyword) for n in niches]

    if not niche_data:
        logger.info("No active niches found")
        return "0 prompts generated"

    total = 0
    for niche_id, keyword in niche_data:
        try:
            prompts = generate_prompts_for_niche(keyword)
            with get_session() as session:
                for p in prompts:
                    # Accept both legacy string format and new dict format
                    if isinstance(p, str):
                        session.add(Prompt(
                            niche_id=niche_id,
                            prompt_text=p,
                            image_backend=IMAGE_BACKEND,
                            status="pending",
                        ))
                    else:
                        session.add(Prompt(
                            niche_id=niche_id,
                            prompt_text=p.get("prompt_text", ""),
                            keywords=p.get("keywords"),
                            design_style=p.get("design_style"),
                            product_types=p.get("product_types"),
                            target_persona=p.get("target_persona"),
                            color_palette=p.get("color_palette"),
                            image_backend=IMAGE_BACKEND,
                            status="pending",
                        ))
            total += len(prompts)
            logger.info(f"  {keyword}: {len(prompts)} prompts generated")
        except Exception as e:
            logger.error(f"  Failed for {keyword}: {e}")

    logger.info(f"Prompt generation complete: {total} prompts")
    return f"{total} prompts generated"
