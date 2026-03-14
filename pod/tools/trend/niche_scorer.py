from sqlalchemy import select

from tools.shared.db import get_session
from tools.shared.models import Niche
from tools.shared.logger import get_logger

logger = get_logger("niche_scorer")

KILL_THRESHOLD = 10


def compute_score(trend_score: float, velocity: float, competition: float) -> float:
    """Compute final score: (trend_score × velocity) / max(competition, 0.1)."""
    trend = trend_score or 0
    vel = velocity or 0
    comp = max(competition or 0.1, 0.1)
    return (trend * vel) / comp


def run():
    """Score all niches, normalise 0-100, kill low performers."""
    logger.info("Starting niche scoring")

    with get_session() as session:
        niches = session.execute(select(Niche)).scalars().all()

        if not niches:
            logger.info("No niches to score")
            return "0 niches scored"

        # Compute raw scores
        raw_scores = {}
        for niche in niches:
            raw_scores[niche.id] = compute_score(
                niche.trend_score, niche.velocity, niche.competition
            )

        # Normalise to 0-100
        max_raw = max(raw_scores.values()) if raw_scores else 1
        if max_raw == 0:
            max_raw = 1

        killed = 0
        for niche in niches:
            normalised = (raw_scores[niche.id] / max_raw) * 100
            niche.final_score = round(normalised, 2)
            if normalised < KILL_THRESHOLD and niche.status == "active":
                niche.status = "killed"
                killed += 1

        # Log top 20
        sorted_niches = sorted(niches, key=lambda n: n.final_score or 0, reverse=True)
        logger.info("Top 20 niches:")
        for n in sorted_niches[:20]:
            logger.info(
                f"  {n.keyword}: score={n.final_score:.1f} "
                f"(trend={n.trend_score}, vel={n.velocity:.2f}, comp={n.competition})"
            )

    logger.info(f"Scoring complete: {len(niches)} scored, {killed} killed")
    return f"{len(niches)} niches scored, {killed} killed"
