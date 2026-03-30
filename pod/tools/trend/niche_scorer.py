"""Niche scorer — combines multi-source snapshot history into a final_score.

Scoring formula:
  1. Composite score = weighted average of the latest snapshot per source
       gemini × 0.40 + pytrends × 0.30 + reddit × 0.15 + etsy × 0.15
  2. Velocity boost: × (1 + avg_velocity × 0.2)   [−20% to +20%]
  3. Upcoming bonus: × 1.15 if upcoming_score > trend_score
  4. Competition penalty: ÷ max(competition, 0.1)
  5. Normalise all final scores to 0-100
  6. Kill niches below KILL_THRESHOLD
"""
from sqlalchemy import select

from tools.shared.db import get_session
from tools.shared.models import Niche, TrendSnapshot
from tools.shared.logger import get_logger

logger = get_logger("niche_scorer")

SOURCE_WEIGHTS = {"gemini": 0.40, "pytrends": 0.30, "reddit": 0.15, "etsy": 0.15}
KILL_THRESHOLD = 10


def compute_score(
    trend_score: float | None,
    velocity: float | None,
    competition: float | None,
) -> float:
    """Pure-value scoring function (used by unit tests and legacy path).

    Formula: (trend_score * velocity) / max(competition, 0.1)
    """
    trend = trend_score or 0
    vel = velocity or 0
    comp = max(competition or 0.1, 0.1)
    return (trend * vel) / comp


def _latest_snapshots(niche: Niche) -> dict[str, TrendSnapshot]:
    """Return the most recent non-upcoming snapshot per source for a niche."""
    best: dict[str, TrendSnapshot] = {}
    for snap in niche.snapshots:
        if snap.is_upcoming:
            continue
        existing = best.get(snap.source)
        if not existing or snap.snapshot_date > existing.snapshot_date:
            best[snap.source] = snap
    return best


def _compute_niche_score(niche: Niche) -> float:
    """Compute enriched composite score using multi-source snapshot history."""
    source_data = _latest_snapshots(niche)

    if source_data:
        # Weighted composite from snapshot sources
        composite = 0.0
        total_weight = 0.0
        for src, snap in source_data.items():
            w = SOURCE_WEIGHTS.get(src, 0.10)
            composite += (snap.trend_score or 0) * w
            total_weight += w
        composite = composite / total_weight if total_weight else 0.0
        avg_vel = sum((s.velocity or 0) for s in source_data.values()) / len(source_data)
    else:
        # Fallback to direct niche fields (legacy / no snapshots yet)
        composite = niche.trend_score or 0
        avg_vel = niche.velocity or 0

    # Velocity boost: ±20%
    composite *= 1 + (avg_vel * 0.2)

    # Upcoming bonus: +15% if Gemini predicts a near-future surge
    if niche.upcoming_score and niche.upcoming_score > (niche.trend_score or 0):
        composite *= 1.15

    # Competition penalty
    comp = max(niche.competition or 0.1, 0.1)
    composite /= comp

    return composite


def run():
    """Score all active niches, normalise 0-100, kill low performers."""
    logger.info("Starting niche scoring (multi-source snapshot mode)")

    with get_session() as session:
        niches = session.execute(select(Niche)).scalars().all()

        if not niches:
            logger.info("No niches to score")
            return "0 niches scored"

        # Compute raw scores using enriched multi-source scorer
        raw_scores = {n.id: _compute_niche_score(n) for n in niches}

        # Normalise 0-100
        max_raw = max(raw_scores.values()) or 1

        killed = 0
        for niche in niches:
            normalised = round((raw_scores[niche.id] / max_raw) * 100, 2)
            niche.final_score = normalised

            if normalised < KILL_THRESHOLD and niche.status == "active":
                niche.status = "killed"
                killed += 1

            # Update source_scores breakdown for dashboard display
            source_data = _latest_snapshots(niche)
            scores = niche.source_scores or {}
            for src, snap in source_data.items():
                scores[src] = snap.trend_score
            if scores:
                niche.source_scores = scores

        # Log top 20
        sorted_niches = sorted(niches, key=lambda n: n.final_score or 0, reverse=True)
        logger.info("Top 20 niches:")
        for n in sorted_niches[:20]:
            sources = list((n.source_scores or {}).keys())
            upcoming = f" → upcoming {n.upcoming_score:.0f}" if n.upcoming_score else ""
            logger.info(
                f"  {n.keyword}: score={n.final_score:.1f}{upcoming} "
                f"(sources: {', '.join(sources) or 'legacy'})"
            )

    logger.info(f"Scoring complete: {len(niches)} scored, {killed} killed")
    return f"{len(niches)} niches scored, {killed} killed"
