"""Upcoming Trends Forecast — Weekly, 3-6 Month Horizon

Claude-powered forecast of TikTok trends 3-6 months ahead.
Pulls Reddit RSS signals, maps seasonal calendar, produces
Markdown + JSON reports and saves top trends to the DB.

Run:
  python jobs/job_trend_forecast.py
  python main.py --job trend
Schedule: Weekly (Mondays 07:00 UTC recommended)
"""
import json
import time
import random
import feedparser
from datetime import datetime
from database.models import SessionLocal, Niche, Trend
from utils.ai_utils import ask_claude_json
from config import get_logger, REPORTS_DIR

logger = get_logger("job_trend_forecast")

# ── Seasonal calendar: April – September 2026 ──────────────────────────────
SEASONAL_CALENDAR = [
    {
        "month": "April 2026",
        "events": [
            "April Fools (Apr 1)", "Spring Cleaning season", "Easter weekend",
            "Earth Day (Apr 22)", "Tax season end — disposable income spike",
        ],
    },
    {
        "month": "May 2026",
        "events": [
            "Mother's Day (May 10)", "Memorial Day weekend", "Graduation season",
            "Mental Health Awareness Month", "Spring fitness push",
        ],
    },
    {
        "month": "June 2026",
        "events": [
            "Pride Month", "Father's Day (Jun 21)", "Summer solstice",
            "Wedding / bridal season peak", "Back-to-summer travel boom",
        ],
    },
    {
        "month": "July 2026",
        "events": [
            "Independence Day (Jul 4)", "Amazon Prime Day (mid-July)",
            "Summer beauty + SPF peak", "Beach & outdoor gear surge",
            "Mid-year clearance sales",
        ],
    },
    {
        "month": "August 2026",
        "events": [
            "Back-to-school shopping", "Dorm essentials surge",
            "Pre-fall fashion launches", "Late-summer travel last push",
            "End-of-summer fitness motivation",
        ],
    },
    {
        "month": "September 2026",
        "events": [
            "Labor Day (Sep 7)", "Fall fashion & beauty launch",
            "Back-to-routine wellness", "Pumpkin spice season starts",
            "Hispanic Heritage Month",
        ],
    },
]

SEED_NICHES = ["beauty", "fitness", "gadgets", "food", "pets", "tech"]

# Reddit RSS feeds (no API key, no rate limits for RSS)
REDDIT_FEEDS = {
    "beauty":  "https://www.reddit.com/r/SkincareAddiction+MakeupAddiction/.rss",
    "fitness": "https://www.reddit.com/r/fitness+bodyweightfitness/.rss",
    "gadgets": "https://www.reddit.com/r/gadgets+BuyItForLife/.rss",
    "food":    "https://www.reddit.com/r/food+Cooking/.rss",
    "pets":    "https://www.reddit.com/r/dogs+cats/.rss",
    "tech":    "https://www.reddit.com/r/technology+hardware/.rss",
}


# ── Signal scraping ─────────────────────────────────────────────────────────

def fetch_reddit_signals(niche: str, limit: int = 8) -> list[str]:
    """Pull hot post titles from Reddit RSS for a niche (no API key needed)."""
    url = REDDIT_FEEDS.get(niche, f"https://www.reddit.com/r/{niche}/.rss")
    try:
        feed = feedparser.parse(url)
        titles = [e.title for e in feed.entries[:limit] if hasattr(e, "title")]
        logger.info(f"  Reddit signals for '{niche}': {len(titles)} titles")
        return titles
    except Exception as e:
        logger.warning(f"  Reddit RSS failed for '{niche}': {e}")
        return []


# ── Claude AI forecast ──────────────────────────────────────────────────────

def forecast_niche(niche: str, signals: list[str], calendar: list[dict]) -> dict:
    """Ask Claude to forecast top 5 upcoming TikTok trends for a niche (3-6 months)."""
    signals_text = "\n".join(f"  - {s}" for s in signals) if signals else "  - (no live signals available)"
    calendar_text = "\n".join(
        f"  {c['month']}: {', '.join(c['events'])}" for c in calendar
    )

    prompt = f"""You are a senior TikTok affiliate trend analyst. Today is {datetime.utcnow().strftime('%Y-%m-%d')}.

NICHE: {niche}

UPCOMING SEASONAL CALENDAR (April – September 2026):
{calendar_text}

CURRENT REDDIT COMMUNITY SIGNALS (what people are actively discussing NOW):
{signals_text}

TASK: Forecast the TOP 5 TikTok content/product trends for the "{niche}" niche that will peak between April and September 2026.

For each trend, explain:
- What specifically will go viral and WHY (tie to a seasonal driver, cultural moment, or product cycle)
- Best TikTok hook style: question | bold_claim | tutorial | reaction | curiosity_gap
- Top 3 hashtags
- Estimated peak month
- Confidence score (0.0–1.0 based on signal strength)

Return ONLY valid JSON (no markdown, no extra text):
{{
  "niche": "{niche}",
  "forecast_window": "April–September 2026",
  "generated_at": "{datetime.utcnow().isoformat()}",
  "trends": [
    {{
      "rank": 1,
      "trend_name": "short catchy trend label",
      "description": "2-3 sentence explanation of why this will trend",
      "driver": "seasonal|cultural|product_launch|algorithm|celebrity",
      "peak_month": "Month YYYY",
      "hook_style": "one of the 5 patterns above",
      "hashtags": ["#tag1", "#tag2", "#tag3"],
      "content_angle": "One-sentence idea for the video",
      "affiliate_opportunity": "Specific product type or brand to affiliate with",
      "confidence": 0.85
    }}
  ],
  "top_products_to_watch": ["product or product category 1", "product 2", "product 3"],
  "emerging_hashtags": ["#emerging1", "#emerging2", "#emerging3"],
  "summary": "2-sentence executive summary for content planning this niche over the next 3-6 months"
}}"""

    return ask_claude_json(prompt, max_tokens=2000)


# ── Report generation ───────────────────────────────────────────────────────

def build_markdown_report(forecasts: list[dict]) -> str:
    """Render all forecasts as a human-readable Markdown report."""
    now = datetime.utcnow()
    lines = [
        "# TikTok Upcoming Trends — 3-6 Month Forecast",
        f"**Generated:** {now.strftime('%Y-%m-%d %H:%M UTC')}",
        f"**Forecast Window:** April – September 2026",
        "",
        "---",
        "",
        "## Seasonal Calendar",
        "",
    ]

    for c in SEASONAL_CALENDAR:
        events = " · ".join(c["events"])
        lines.append(f"**{c['month']}** — {events}")
    lines += ["", "---", ""]

    for f in forecasts:
        niche = f.get("niche", "unknown").upper()
        summary = f.get("summary", "")
        emerging = " ".join(f.get("emerging_hashtags", []))
        lines += [
            f"## {niche}",
            f"> {summary}",
            "",
        ]
        if emerging:
            lines += [f"**Emerging hashtags:** {emerging}", ""]

        for t in f.get("trends", []):
            rank = t.get("rank", "?")
            conf = int(t.get("confidence", 0) * 100)
            tags = " ".join(t.get("hashtags", []))
            lines += [
                f"### {rank}. {t.get('trend_name', '?')}  _{conf}% confidence_",
                f"- **Peak month:** {t.get('peak_month', '?')}",
                f"- **Driver:** {t.get('driver', '?')}",
                f"- **Hook style:** `{t.get('hook_style', '?')}`",
                f"- **Content angle:** {t.get('content_angle', '?')}",
                f"- **Affiliate opportunity:** {t.get('affiliate_opportunity', '?')}",
                f"- **Hashtags:** {tags}",
                f"",
                f"  {t.get('description', '')}",
                "",
            ]

        products = ", ".join(f.get("top_products_to_watch", []))
        if products:
            lines += [f"**Products to watch:** {products}", ""]

        lines += ["---", ""]

    return "\n".join(lines)


# ── DB persistence ──────────────────────────────────────────────────────────

def save_to_db(session, forecasts: list[dict]) -> int:
    """Write forecasted trends (confidence >= 0.6) into the Trend table."""
    saved = 0
    for f in forecasts:
        niche = f.get("niche", "unknown")
        for t in f.get("trends", []):
            if t.get("confidence", 0) < 0.6:
                continue
            trend = Trend(
                niche=niche,
                hook_pattern=t.get("hook_style", "bold_claim"),
                hook_text=t.get("content_angle", "")[:200],
                hashtags=",".join(t.get("hashtags", [])),
                views=0,
                scraped_at=datetime.utcnow(),
            )
            session.add(trend)
            saved += 1
    session.commit()
    logger.info(f"Saved {saved} forecast trend records to DB.")
    return saved


# ── Main entry ──────────────────────────────────────────────────────────────

def run():
    logger.info("=== Trend Forecast (3-6 Month Outlook) started ===")

    session = SessionLocal()
    forecasts = []

    try:
        # Pull active niches from DB; fall back to seed list
        db_niches = [
            n.niche for n in
            session.query(Niche).filter_by(status="active").distinct(Niche.niche).limit(10).all()
        ]
        niches = list(dict.fromkeys(db_niches)) if db_niches else SEED_NICHES
        logger.info(f"Forecasting niches: {niches}")

        for niche in niches:
            logger.info(f"-- Niche: {niche}")

            signals = fetch_reddit_signals(niche)
            time.sleep(random.uniform(1.5, 3.0))  # polite scraping

            try:
                forecast = forecast_niche(niche, signals, SEASONAL_CALENDAR)
                forecasts.append(forecast)
                n_trends = len(forecast.get("trends", []))
                logger.info(f"   Claude returned {n_trends} trend forecasts for '{niche}'")
            except Exception as e:
                logger.error(f"   Claude forecast failed for '{niche}': {e}")

            time.sleep(random.uniform(2.0, 4.0))

        if not forecasts:
            logger.warning("No forecasts generated — check API key and DB.")
            return []

        # Persist to DB
        save_to_db(session, forecasts)

        # Write reports
        ts = datetime.utcnow().strftime("%Y%m%d_%H%M")
        md_path = REPORTS_DIR / f"trend_forecast_{ts}.md"
        json_path = REPORTS_DIR / f"trend_forecast_{ts}.json"

        md_report = build_markdown_report(forecasts)
        md_path.write_text(md_report, encoding="utf-8")
        json_path.write_text(json.dumps(forecasts, indent=2, ensure_ascii=False), encoding="utf-8")

        logger.info(f"Report (Markdown): {md_path}")
        logger.info(f"Report (JSON):     {json_path}")
        logger.info(f"=== Trend Forecast complete — {len(forecasts)} niches covered ===")

        # Print to stdout for immediate review
        print("\n" + md_report)

        return forecasts

    except Exception as e:
        session.rollback()
        logger.error(f"Trend Forecast job failed: {e}")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    run()
