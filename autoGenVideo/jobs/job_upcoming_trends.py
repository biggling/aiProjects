"""Job: Upcoming Trends Research (Weekly)

Forecasts hot content topics for the next 3-6 months using:
  - Google Trends 12-month seasonal pattern analysis (pytrends)
  - Rising breakout keyword detection
  - Seasonal event calendar
  - Claude AI synthesis into actionable content forecast

Schedule: Weekly on Monday at 07:00 UTC
"""
import time
import random
from datetime import date, datetime

from pytrends.request import TrendReq
from database.models import SessionLocal, Topic
from utils.ai_utils import ask_claude_json
from config import REPORTS_DIR, get_logger

logger = get_logger("job_upcoming_trends")

# Content categories → seed keywords for Google Trends analysis
CONTENT_CATEGORIES = {
    "lifestyle": ["morning routine", "self improvement", "minimalism", "slow living", "daily habits"],
    "fitness": ["home workout", "weight loss tips", "gym motivation", "yoga for beginners", "running tips"],
    "tech": ["AI tools 2025", "productivity apps", "smartphone tips", "best gadgets", "ChatGPT tips"],
    "finance": ["saving money tips", "investing for beginners", "side hustle ideas", "passive income", "budgeting tips"],
    "food": ["meal prep ideas", "healthy recipes", "easy cooking", "smoothie recipes", "high protein meals"],
    "travel": ["travel tips", "budget travel", "summer vacation", "road trip ideas", "hidden gems"],
    "mental health": ["anxiety relief", "meditation for beginners", "stress management", "sleep tips", "mindfulness"],
    "fashion": ["summer outfits", "thrift shopping", "style tips", "capsule wardrobe", "outfit ideas"],
    "beauty": ["skincare routine", "sunscreen tips", "hair care tips", "natural makeup", "beauty hacks"],
    "education": ["study tips", "learn new skills", "online courses", "reading habits", "productivity hacks"],
}

# Seasonal calendar: month → events/themes that drive content demand
SEASONAL_MAP = {
    1:  ["New Year motivation", "January reset", "winter wellness", "dry January"],
    2:  ["Valentine's Day", "self love", "winter skincare", "relationship tips"],
    3:  ["Spring cleaning", "spring reset", "outdoor prep", "St Patrick's Day"],
    4:  ["Easter", "spring fashion", "outdoor activities", "spring break travel"],
    5:  ["Mother's Day", "spring fitness", "Memorial Day", "graduation season"],
    6:  ["Father's Day", "summer kickoff", "Pride Month", "summer body"],
    7:  ["4th of July", "summer travel", "outdoor adventures", "summer recipes"],
    8:  ["Back to School", "late summer", "school supplies", "college prep"],
    9:  ["Fall fashion", "autumn lifestyle", "Back to School", "Labor Day"],
    10: ["Halloween", "fall decor", "cozy season", "pumpkin recipes"],
    11: ["Thanksgiving", "Black Friday", "holiday prep", "gratitude"],
    12: ["Christmas", "holiday gifts", "New Year prep", "year in review"],
}


def get_upcoming_months(start: int = 3, end: int = 6) -> list[date]:
    """Return first-of-month dates for 3–6 months from today."""
    today = date.today()
    result = []
    for delta in range(start, end + 1):
        yr = today.year + (today.month + delta - 1) // 12
        mo = (today.month + delta - 1) % 12 + 1
        result.append(date(yr, mo, 1))
    return result


def get_seasonal_events(upcoming_months: list[date]) -> list[str]:
    """Return seasonal themes for the upcoming window, deduplicated."""
    events = []
    for m in upcoming_months:
        events.extend(SEASONAL_MAP.get(m.month, []))
    return list(dict.fromkeys(events))


def fetch_pytrends_seasonal(keywords: list[str], upcoming_months: list[date]) -> dict:
    """
    Fetch 12-month Google Trends and score keywords by seasonal fit:
      - seasonal_score: how strongly the keyword peaks in target months vs annual avg
      - momentum: recent 3-month activity vs annual avg
      - rising_related: breakout related queries
    """
    pytrends = TrendReq(hl="en-US", tz=0)
    target_month_nums = {m.month for m in upcoming_months}
    results = {}

    for i in range(0, len(keywords), 5):
        batch = keywords[i:i + 5]
        try:
            pytrends.build_payload(batch, timeframe="today 12-m")
            df = pytrends.interest_over_time()
            related = pytrends.related_queries()

            for kw in batch:
                if df.empty or kw not in df.columns:
                    continue
                series = df[kw]
                overall_avg = series.mean()
                if overall_avg < 1:
                    continue

                # Seasonal score: avg interest in target months vs full-year avg
                monthly_avg = series.groupby(series.index.month).mean()
                target_vals = [float(monthly_avg.get(m, 0)) for m in target_month_nums]
                peak_seasonal = max(target_vals) if target_vals else 0.0
                seasonal_score = min(peak_seasonal / (overall_avg + 0.01), 5.0)

                # Momentum: last ~13 weeks vs full-year avg
                recent_avg = float(series.tail(13).mean())
                momentum = min(recent_avg / (overall_avg + 0.01), 3.0)

                # Rising related queries (breakout terms)
                rising_terms = []
                if kw in related and related[kw].get("rising") is not None:
                    rising_df = related[kw]["rising"]
                    if not rising_df.empty:
                        rising_terms = rising_df["query"].head(3).tolist()

                results[kw] = {
                    "seasonal_score": round(seasonal_score, 2),
                    "momentum": round(momentum, 2),
                    "overall_avg": round(float(overall_avg), 1),
                    "rising_related": rising_terms,
                }

            time.sleep(random.uniform(5, 9))

        except Exception as e:
            logger.warning(f"pytrends error for batch {batch}: {e}")

    return results


def build_claude_forecast(
    trend_data: dict,
    seasonal_events: list[str],
    upcoming_months: list[date],
) -> dict:
    """Synthesize trend data into a Claude-powered 3–6 month content forecast."""
    month_labels = [m.strftime("%B %Y") for m in upcoming_months]

    # Rank by combined seasonal + momentum score
    ranked = sorted(
        [
            (kw, d["seasonal_score"] * 0.6 + d["momentum"] * 0.4)
            for kw, d in trend_data.items()
        ],
        key=lambda x: x[1],
        reverse=True,
    )[:30]

    trend_summary = "\n".join(
        f"- {kw}: seasonal_score={trend_data[kw]['seasonal_score']}, "
        f"momentum={trend_data[kw]['momentum']}, "
        f"rising_related={trend_data[kw].get('rising_related', [])}"
        for kw, _ in ranked
    )

    prompt = f"""You are a digital content strategist specializing in short-form video (TikTok, YouTube Shorts, Instagram Reels).

Target forecast window: {', '.join(month_labels)}
Upcoming seasonal events/themes: {', '.join(seasonal_events[:15])}

Google Trends 12-month analysis (seasonal_score = how strongly keyword peaks in target months relative to annual average; momentum = recent 3-month growth; rising_related = breakout search terms):
{trend_summary}

Task: Forecast the TOP 15 video content topics that will perform best during {month_labels[0]}–{month_labels[-1]}.

For each topic, provide a specific, actionable content angle (not just a generic keyword). Return ONLY valid JSON:
{{
  "forecast_period": "{month_labels[0]} — {month_labels[-1]}",
  "generated_at": "{datetime.utcnow().strftime('%Y-%m-%d')}",
  "topics": [
    {{
      "topic": "specific video topic angle (e.g. '5 summer skincare mistakes everyone makes')",
      "category": "lifestyle|tech|fitness|finance|food|travel|fashion|beauty|mental_health|education",
      "trend_score": 85,
      "rationale": "1-2 sentences: why this will peak in the target window",
      "platform": "tiktok|youtube_shorts|instagram_reels|all",
      "hook_style": "question|bold_claim|tutorial|curiosity_gap|reaction",
      "hashtags": ["#tag1", "#tag2", "#tag3", "#tag4"]
    }}
  ]
}}"""

    return ask_claude_json(prompt, max_tokens=3000)


def save_to_db(session, topics: list[dict]) -> int:
    """Upsert upcoming-trend topics into the Topic table."""
    saved = 0
    for item in topics:
        topic_text = item.get("topic", "").strip()
        if not topic_text:
            continue
        existing = session.query(Topic).filter_by(
            topic=topic_text, source="upcoming_trends"
        ).first()
        if not existing:
            session.add(Topic(
                topic=topic_text,
                platform=item.get("platform", ""),
                trend_score=float(item.get("trend_score", 50)),
                hashtags=",".join(item.get("hashtags", [])),
                source="upcoming_trends",
                status="pending",
            ))
            saved += 1
    return saved


def save_report(forecast: dict) -> None:
    """Write a markdown forecast report to reports/."""
    today = date.today()
    path = REPORTS_DIR / f"upcoming_trends_{today}.md"

    lines = [
        "# Upcoming Content Trends Forecast",
        f"**Period:** {forecast.get('forecast_period', 'N/A')}",
        f"**Generated:** {forecast.get('generated_at', today)}",
        "",
        "| # | Topic | Category | Score | Platform | Hook Style |",
        "|---|-------|----------|-------|----------|------------|",
    ]
    for i, t in enumerate(forecast.get("topics", []), 1):
        lines.append(
            f"| {i} | {t.get('topic', '')} | {t.get('category', '')} "
            f"| {t.get('trend_score', '')} | {t.get('platform', '')} "
            f"| {t.get('hook_style', '')} |"
        )

    lines += ["", "## Rationale", ""]
    for i, t in enumerate(forecast.get("topics", []), 1):
        lines.append(f"**{i}. {t.get('topic', '')}**")
        lines.append(f"   {t.get('rationale', '')}")
        lines.append(f"   Tags: {', '.join(t.get('hashtags', []))}")
        lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")
    logger.info(f"Report saved: {path}")


def run():
    logger.info("=== Upcoming Trends Research started (3–6 month forecast) ===")

    upcoming_months = get_upcoming_months(start=3, end=6)
    seasonal_events = get_seasonal_events(upcoming_months)
    logger.info(f"Target window: {upcoming_months[0]} → {upcoming_months[-1]}")
    logger.info(f"Seasonal events detected: {seasonal_events[:8]}")

    all_keywords = [kw for kws in CONTENT_CATEGORIES.values() for kw in kws]
    logger.info(f"Fetching pytrends data for {len(all_keywords)} keywords...")
    trend_data = fetch_pytrends_seasonal(all_keywords, upcoming_months)
    logger.info(f"Trend data collected for {len(trend_data)} keywords")

    if not trend_data:
        logger.warning("No trend data retrieved — check pytrends connectivity")
        return

    logger.info("Generating Claude AI forecast...")
    forecast = build_claude_forecast(trend_data, seasonal_events, upcoming_months)
    topics = forecast.get("topics", [])
    logger.info(f"Claude forecast: {len(topics)} topics identified")

    save_report(forecast)

    session = SessionLocal()
    try:
        saved = save_to_db(session, topics)
        session.commit()
        logger.info(f"Saved {saved} new upcoming-trend topics to DB")
    except Exception as e:
        session.rollback()
        logger.error(f"DB save failed: {e}")
    finally:
        session.close()

    logger.info("=== Upcoming Trends Research complete ===")
    return forecast


if __name__ == "__main__":
    run()
