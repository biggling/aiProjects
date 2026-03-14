from sqlalchemy import select

from tools.shared.api_clients import get_anthropic
from tools.shared.db import get_session
from tools.shared.models import Listing, Niche
from tools.shared.logger import get_logger

logger = get_logger("caption_generator")


def generate_caption(title: str, keyword: str) -> str:
    """Generate a social media caption via Claude."""
    client = get_anthropic()

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=256,
        messages=[{
            "role": "user",
            "content": (
                f'Write ONE engaging social media caption (max 200 characters) for this product:\n'
                f'Title: {title}\nNiche: {keyword}\n'
                f'Include 3-5 relevant hashtags. Output ONLY the caption text, nothing else.'
            ),
        }],
    )

    caption = response.content[0].text.strip()
    return caption[:200]


def run():
    """Generate captions for listings that have titles but no captions."""
    logger.info("Starting caption generation")

    with get_session() as session:
        listings = session.execute(
            select(Listing).where(
                Listing.title.isnot(None),
                Listing.caption.is_(None),
            )
        ).scalars().all()
        listing_data = [(l.id, l.title, l.niche_id) for l in listings]

    if not listing_data:
        logger.info("No listings need captions")
        return "0 captions generated"

    # Load niche keywords
    niche_ids = {nid for _, _, nid in listing_data}
    with get_session() as session:
        niches = {n.id: n.keyword for n in session.execute(
            select(Niche).where(Niche.id.in_(niche_ids))
        ).scalars().all()}

    generated = 0
    for listing_id, title, niche_id in listing_data:
        keyword = niches.get(niche_id, "design")
        try:
            caption = generate_caption(title, keyword)
            with get_session() as session:
                listing = session.get(Listing, listing_id)
                listing.caption = caption
            generated += 1
            logger.info(f"  Caption for listing {listing_id}: {caption[:50]}...")
        except Exception as e:
            logger.error(f"  Failed for listing {listing_id}: {e}")

    logger.info(f"Caption generation complete: {generated}")
    return f"{generated} captions generated"
