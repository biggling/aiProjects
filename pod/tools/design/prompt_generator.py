import json

from sqlalchemy import select

from tools.shared.api_clients import get_anthropic
from tools.shared.db import get_session
from tools.shared.models import Niche, Prompt
from tools.shared.logger import get_logger

logger = get_logger("prompt_generator")

PROMPTS_PER_NICHE = 50


def generate_prompts_for_niche(keyword: str) -> list[str]:
    """Call Claude to generate design prompts for a niche keyword."""
    client = get_anthropic()

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        system=(
            "You are a POD design expert. Generate distinct Midjourney/Stable Diffusion prompts "
            "for print-on-demand designs. Each prompt must be print-ready, vector-friendly, "
            "no text in image, transparent background suitable. Output ONLY a JSON array of strings."
        ),
        messages=[{
            "role": "user",
            "content": (
                f'Generate {PROMPTS_PER_NICHE} distinct design prompts for the niche: "{keyword}". '
                "Output JSON array of strings only, no markdown."
            ),
        }],
    )

    text = response.content[0].text.strip()
    # Handle potential markdown wrapping
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    return json.loads(text)


def run():
    """Generate prompts for top 10 niches by final_score."""
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
                for prompt_text in prompts:
                    session.add(Prompt(
                        niche_id=niche_id,
                        prompt_text=prompt_text,
                        status="pending",
                    ))
            total += len(prompts)
            logger.info(f"  {keyword}: {len(prompts)} prompts generated")
        except Exception as e:
            logger.error(f"  Failed for {keyword}: {e}")

    logger.info(f"Prompt generation complete: {total} prompts")
    return f"{total} prompts generated"
