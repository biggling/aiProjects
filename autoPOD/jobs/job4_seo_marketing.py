"""Job 4: SEO & Marketing Automation
Schedule: Every 6 hours
"""
import time
import random
from datetime import datetime
from database.models import SessionLocal, Listing, MarketingLog
from utils.platform_api import PinterestClient
from utils.image_utils import apply_design_to_mockup
from utils.notify import slack
from config import ASSETS_DIR, DESIGNS_DIR, get_logger

logger = get_logger("job4_seo_marketing")

MOCKUP_TEMPLATES = {
    "tshirt": ASSETS_DIR / "mockups" / "tshirt_mockup.png",
    "mug": ASSETS_DIR / "mockups" / "mug_mockup.png",
    "poster": ASSETS_DIR / "mockups" / "poster_mockup.png",
}

REDDIT_SUBREDDITS = {
    "funny dog mom": ["r/dogs", "r/aww"],
    "hiking": ["r/hiking", "r/outdoors"],
    "cat lover": ["r/cats", "r/aww"],
    "teacher": ["r/Teachers"],
    "nurse": ["r/nursing"],
    "default": ["r/findfashion"],
}


def get_or_create_pinterest_board(client: PinterestClient, niche: str) -> str | None:
    """Return board_id for a niche, creating it if necessary."""
    try:
        boards = client.get_boards()
        board_name = f"POD - {niche.title()}"
        for board in boards:
            if board.get("name") == board_name:
                return board["id"]
        new_board = client.create_board(board_name, f"Print-on-demand designs for {niche}")
        return new_board["id"]
    except Exception as e:
        logger.error(f"Pinterest board create/fetch failed: {e}")
        return None


def post_to_pinterest(listing: Listing, mockup_path: str) -> bool:
    try:
        client = PinterestClient()
        board_id = get_or_create_pinterest_board(client, listing.title[:30])
        if not board_id:
            return False
        client.create_pin(
            board_id=board_id,
            media_url=f"file://{mockup_path}",  # In production: upload to S3 first
            title=listing.title[:100],
            description=f"{listing.title}\n\nShop now: {listing.url or ''}",
            link=listing.url or "",
        )
        return True
    except Exception as e:
        logger.error(f"Pinterest pin failed for listing {listing.id}: {e}")
        return False


def post_to_reddit(listing: Listing, niche: str) -> bool:
    try:
        import praw
        from config import validate_required_keys
        # Reddit requires client credentials in .env
        # REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USERNAME, REDDIT_PASSWORD
        import os
        reddit = praw.Reddit(
            client_id=os.getenv("REDDIT_CLIENT_ID", ""),
            client_secret=os.getenv("REDDIT_CLIENT_SECRET", ""),
            username=os.getenv("REDDIT_USERNAME", ""),
            password=os.getenv("REDDIT_PASSWORD", ""),
            user_agent="autoPOD/1.0",
        )
        subreddits = REDDIT_SUBREDDITS.get(niche.lower(), REDDIT_SUBREDDITS["default"])
        subreddit_name = random.choice(subreddits).lstrip("r/")
        sub = reddit.subreddit(subreddit_name)
        sub.submit(
            title=f"I made this {niche} design — thoughts?",
            url=listing.url or "",
        )
        return True
    except Exception as e:
        logger.warning(f"Reddit post skipped for listing {listing.id}: {e}")
        return False


def generate_mockup(listing: Listing) -> str | None:
    try:
        product_type = listing.design.product_type if listing.design else "tshirt"
        template = MOCKUP_TEMPLATES.get(product_type, MOCKUP_TEMPLATES["tshirt"])
        if not template.exists():
            logger.warning(f"Mockup template not found: {template}")
            return None
        from pathlib import Path
        design_path = Path(listing.design.file_path) if listing.design and listing.design.file_path else None
        if not design_path or not design_path.exists():
            return None
        output_path = design_path.parent / f"mockup_{listing.id}.png"
        apply_design_to_mockup(design_path, template, output_path)
        return str(output_path)
    except Exception as e:
        logger.error(f"Mockup generation failed for listing {listing.id}: {e}")
        return None


def run():
    logger.info("=== Job 4: SEO & Marketing started ===")

    session = SessionLocal()
    try:
        # Get recently published listings not yet marketed
        from sqlalchemy import not_, exists
        from database.models import MarketingLog

        marketed_ids = session.query(MarketingLog.listing_id).filter(
            MarketingLog.platform == "pinterest"
        ).subquery()
        listings = (
            session.query(Listing)
            .filter(Listing.status == "active")
            .filter(~Listing.id.in_(marketed_ids))
            .limit(20)
            .all()
        )
        logger.info(f"Found {len(listings)} listings to market.")

        for listing in listings:
            niche = listing.design.niche.niche if listing.design and listing.design.niche else "general"

            # Generate mockup
            mockup_path = generate_mockup(listing)

            # Pinterest
            if mockup_path:
                success = post_to_pinterest(listing, mockup_path)
                if success:
                    log = MarketingLog(
                        listing_id=listing.id,
                        platform="pinterest",
                        content=listing.title,
                        posted_at=datetime.utcnow(),
                    )
                    session.add(log)
                    logger.info(f"Pinned listing {listing.id}")
                time.sleep(random.uniform(90, 210))  # stagger 1.5–3.5 min

            # Reddit (limited to avoid spam flags)
            if random.random() < 0.2:  # 20% of listings get Reddit post
                post_to_reddit(listing, niche)
                time.sleep(random.uniform(30, 60))

        session.commit()
        logger.info("=== Job 4 complete ===")

    except Exception as e:
        session.rollback()
        logger.error(f"Job 4 failed: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    run()
