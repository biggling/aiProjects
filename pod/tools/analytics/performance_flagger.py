from datetime import datetime, timezone, timedelta

from sqlalchemy import select

from tools.shared.db import get_session
from tools.shared.models import Listing
from tools.shared.notify import notify
from tools.shared.logger import get_logger

logger = get_logger("performance_flagger")

MIN_DAYS = 7
MIN_VIEWS = 50
MIN_FAVORITES = 3


def run():
    """Flag underperforming listings (>7 days, low views/favorites)."""
    logger.info("Starting performance flagging")

    cutoff = datetime.now(timezone.utc) - timedelta(days=MIN_DAYS)

    with get_session() as session:
        listings = session.execute(
            select(Listing).where(
                Listing.status == "live",
                Listing.uploaded_at.isnot(None),
                Listing.uploaded_at < cutoff,
            )
        ).scalars().all()

        flagged = 0
        for listing in listings:
            views = listing.views or 0
            favorites = listing.favorites or 0

            if views < MIN_VIEWS and favorites < MIN_FAVORITES:
                listing.status = "underperforming"
                flagged += 1
                logger.info(
                    f"  Flagged listing {listing.id}: {listing.title[:40]} "
                    f"(views={views}, fav={favorites})"
                )

    if flagged > 0:
        notify(
            "Low performers",
            f"{flagged} listings flagged for review",
            level="warning",
        )

    logger.info(f"Performance flagging complete: {flagged} flagged")
    return f"{flagged} listings flagged"
