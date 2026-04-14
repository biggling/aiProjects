import json

from sqlalchemy import select

from tools.shared.api_clients import get_gemini
from tools.shared.db import get_session
from tools.shared.models import Design, Listing, Niche
from tools.shared.logger import get_logger

logger = get_logger("copy_generator")

_COPY_MODEL = "gemini-2.5-flash"


def generate_copy(keyword: str) -> dict:
    """Call Gemini to generate Etsy listing copy for a niche."""
    client = get_gemini()

    prompt = (
        "You are an Etsy SEO expert. Output ONLY valid JSON, no markdown, "
        "no code blocks, no explanation.\n\n"
        f'For the niche "{keyword}" and product type "t-shirt", '
        "write a JSON object with:\n"
        '- "title": 140-char Etsy title, front-load keywords\n'
        '- "description": 800-char description, 5 bullet points, benefits-focused\n'
        '- "tags": array of exactly 13 strings, mix long-tail and short keywords\n'
        "Output only valid JSON."
    )

    response = client.models.generate_content(model=_COPY_MODEL, contents=prompt)

    text = response.text.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    return json.loads(text)


def run():
    """Generate copy for designs that are mockup_ready but have no listing copy."""
    logger.info("Starting copy generation")

    with get_session() as session:
        # Find designs that are mockup_ready without a listing yet
        designs = session.execute(
            select(Design).where(Design.status == "mockup_ready")
        ).scalars().all()

        to_process = []
        for d in designs:
            existing = session.execute(
                select(Listing).where(
                    Listing.design_id == d.id,
                    Listing.title.isnot(None),
                )
            ).scalar_one_or_none()
            if not existing:
                niche = session.get(Niche, d.niche_id)
                to_process.append((d.id, d.niche_id, niche.keyword if niche else "design"))

    if not to_process:
        logger.info("No designs need copy")
        return "0 listings created"

    created = 0
    for design_id, niche_id, keyword in to_process:
        try:
            copy = generate_copy(keyword)

            title = copy.get("title", "")[:140]
            description = copy.get("description", "")
            tags = copy.get("tags", [])[:13]

            with get_session() as session:
                listing = Listing(
                    design_id=design_id,
                    niche_id=niche_id,
                    title=title,
                    description=description,
                    tags=tags,
                    status="copy_ready",
                )
                session.add(listing)

            created += 1
            logger.info(f"  Copy generated for design {design_id}: {title[:50]}...")
        except Exception as e:
            logger.error(f"  Failed for design {design_id}: {e}")

    logger.info(f"Copy generation complete: {created} listings")
    return f"{created} listings created"
