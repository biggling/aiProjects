"""Job 1: Trend Research & Niche Discovery
Schedule: Daily at 06:00 UTC
"""
import time
import random
import requests
from bs4 import BeautifulSoup
from pytrends.request import TrendReq
from sqlalchemy.dialects.sqlite import insert as sqlite_insert
from database.models import SessionLocal, Niche
from config import (
    ETSY_API_KEY, ETSY_ACCESS_TOKEN, ETSY_BASE_URL,
    NICHE_SCORE_THRESHOLD, TOP_NICHES_PER_RUN,
    get_logger,
)

logger = get_logger("job1_trend_research")

SEED_KEYWORDS = [
    "funny dog mom", "hiking", "cat lover", "teacher gift",
    "nurse life", "veteran", "autism awareness", "book lover",
    "camping", "yoga", "fishing", "dad jokes", "retro 80s",
    "anime", "plant mom", "coffee addict",
]

BLACKLIST = {"generic", "test", "sample"}

ETSY_CATEGORIES = [
    "Clothing", "Art", "Home & Living", "Accessories",
]


def fetch_google_trends(keywords: list) -> dict:
    """Return {keyword: trend_score} using pytrends rising queries."""
    pytrends = TrendReq(hl="en-US", tz=360)
    scores = {}
    batch_size = 5
    for i in range(0, len(keywords), batch_size):
        batch = keywords[i:i + batch_size]
        try:
            pytrends.build_payload(batch, timeframe="now 7-d")
            data = pytrends.interest_over_time()
            if not data.empty:
                for kw in batch:
                    if kw in data.columns:
                        scores[kw] = float(data[kw].mean())
            time.sleep(random.uniform(4, 7))  # respect rate limit
        except Exception as e:
            logger.warning(f"pytrends error for {batch}: {e}")
    return scores


def fetch_etsy_bestsellers() -> list[str]:
    """Return list of trending keyword strings from Etsy."""
    if not ETSY_ACCESS_TOKEN:
        logger.info("Etsy token not set, skipping Etsy scrape.")
        return []
    niches = []
    headers = {
        "Authorization": f"Bearer {ETSY_ACCESS_TOKEN}",
        "x-api-key": ETSY_API_KEY,
    }
    for category in ETSY_CATEGORIES:
        try:
            url = f"{ETSY_BASE_URL}/application/listings/active"
            r = requests.get(url, headers=headers,
                             params={"keywords": category, "limit": 25, "sort_on": "score"},
                             timeout=15)
            if r.status_code == 200:
                for item in r.json().get("results", []):
                    tags = item.get("tags", [])
                    niches.extend(tags[:3])
            time.sleep(0.2)
        except Exception as e:
            logger.warning(f"Etsy fetch error for {category}: {e}")
    return list(set(niches))


def fetch_redbubble_trending() -> list[str]:
    """Scrape Redbubble trending tags."""
    niches = []
    try:
        headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}
        r = requests.get("https://www.redbubble.com/trending/", headers=headers, timeout=15)
        soup = BeautifulSoup(r.text, "html.parser")
        tags = soup.select("a[data-testid='tag']")
        niches = [t.get_text(strip=True).lower() for t in tags[:30]]
    except Exception as e:
        logger.warning(f"Redbubble scrape failed: {e}")
    return niches


def estimate_competition(keyword: str) -> float:
    """Rough competition score: number of active Etsy listings (normalized)."""
    if not ETSY_ACCESS_TOKEN:
        return 0.5
    try:
        headers = {
            "Authorization": f"Bearer {ETSY_ACCESS_TOKEN}",
            "x-api-key": ETSY_API_KEY,
        }
        r = requests.get(
            f"{ETSY_BASE_URL}/application/listings/active",
            headers=headers,
            params={"keywords": keyword, "limit": 1},
            timeout=10,
        )
        if r.status_code == 200:
            count = r.json().get("count", 0)
            return min(count / 50000.0, 1.0)  # normalize to 0-1
    except Exception:
        pass
    return 0.5


def score_niche(trend_score: float, competition: float) -> float:
    return (trend_score * 0.6) / (competition + 0.1)


def run():
    logger.info("=== Job 1: Trend Research started ===")

    # Collect candidates
    trend_scores = fetch_google_trends(SEED_KEYWORDS)
    etsy_niches = fetch_etsy_bestsellers()
    rb_niches = fetch_redbubble_trending()

    all_candidates = list(set(list(trend_scores.keys()) + etsy_niches + rb_niches))
    all_candidates = [n for n in all_candidates if n.lower() not in BLACKLIST and len(n) > 2]

    logger.info(f"Scoring {len(all_candidates)} niche candidates...")

    scored = []
    for niche in all_candidates:
        ts = trend_scores.get(niche, random.uniform(20, 60))  # default if not from pytrends
        comp = estimate_competition(niche)
        s = score_niche(ts, comp)
        if s >= NICHE_SCORE_THRESHOLD:
            scored.append({
                "niche": niche,
                "search_volume": int(ts),
                "competition_score": round(comp, 4),
                "trend_score": round(s, 4),
                "source": "pytrends+etsy+redbubble",
            })

    scored.sort(key=lambda x: x["trend_score"], reverse=True)
    top = scored[:TOP_NICHES_PER_RUN]
    logger.info(f"Top {len(top)} niches identified.")

    # Upsert to DB
    session = SessionLocal()
    try:
        for item in top:
            existing = session.query(Niche).filter_by(niche=item["niche"]).first()
            if existing:
                existing.trend_score = item["trend_score"]
                existing.competition_score = item["competition_score"]
            else:
                session.add(Niche(**item))
        session.commit()
        logger.info(f"Upserted {len(top)} niches to DB.")
    except Exception as e:
        session.rollback()
        logger.error(f"DB write failed: {e}")
    finally:
        session.close()

    logger.info("=== Job 1 complete ===")
    return top


if __name__ == "__main__":
    run()
