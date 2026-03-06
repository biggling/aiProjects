"""Job: Upcoming Affiliate Trends Research (Weekly)

Forecasts hot TikTok affiliate niches and products for the next 3-6 months using:
  - Google Trends 12-month seasonal pattern analysis (pytrends)
  - Rising breakout keyword detection
  - Seasonal shopping event calendar
  - Claude AI synthesis into actionable affiliate niche forecast

Schedule: Weekly on Monday at 06:30 UTC
"""
import time
import random
from datetime import date, datetime

from pytrends.request import TrendReq
from database.models import SessionLocal, Trend
from utils.ai_utils import ask_claude_json
from config import REPORTS_DIR, get_logger

logger = get_logger("job_upcoming_trends")

# Affiliate product categories → seed keywords for seasonal analysis
AFFILIATE_CATEGORIES = {
    "beauty": ["sunscreen spf", "self tanner", "hair growth serum", "lip gloss", "body butter"],
    "fitness": ["resistance bands", "protein powder", "yoga mat", "walking pad", "gym bag"],
    "home": ["home organization", "kitchen gadgets", "smart home devices", "outdoor furniture", "cleaning products"],
    "fashion": ["summer dresses", "swimwear", "sandals women", "sunglasses", "linen outfits"],
    "outdoor": ["camping gear", "beach essentials", "hiking accessories", "portable blender", "water bottle"],
    "electronics": ["portable speaker", "wireless earbuds", "ring light", "phone stand", "mini projector"],
    "pets": ["dog cooling mat", "cat toys", "pet grooming", "dog water bottle", "pet carrier"],
    "supplements": ["collagen powder", "vitamin C serum", "magnesium supplement", "greens powder", "melatonin"],
    "kids": ["water toys", "outdoor play", "back to school supplies", "kids sunscreen", "lunch boxes"],
    "travel": ["travel accessories", "packing cubes", "neck pillow travel", "luggage tags", "travel adapter"],
}

# Seasonal affiliate shopping calendar
SEASONAL_MAP = {
    1:  ["New Year fitness products", "January detox supplements", "winter skincare"],
    2:  ["Valentine's gifts beauty", "self care sets", "romantic gifts"],
    3:  ["spring cleaning supplies", "spring fashion haul", "gardening tools"],
    4:  ["spring break essentials", "Easter gifts", "outdoor prep gear"],
    5:  ["Mother's Day gift guide", "summer body prep", "Memorial Day outdoor"],
    6:  ["Father's Day gadgets", "summer skincare must-haves", "beach essentials", "Pride Month beauty"],
    7:  ["4th of July BBQ products", "summer travel gear", "outdoor games", "pool accessories"],
    8:  ["Back to School supplies", "college dorm essentials", "end of summer sale"],
    9:  ["fall fashion transition", "back to routine supplements", "cozy home items", "Labor Day sale"],
    10: ["Halloween costumes accessories", "fall skincare switch", "cozy season products"],
    11: ["Black Friday deals", "holiday gift guide", "Thanksgiving hosting"],
    12: ["Christmas gift ideas", "holiday beauty sets", "New Year wellness prep"],
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
    """Return seasonal affiliate opportunities for the upcoming window."""
    events = []
    for m in upcoming_months:
        events.extend(SEASONAL_MAP.get(m.month, []))
    return list(dict.fromkeys(events))


def fetch_pytrends_seasonal(keywords: list[str], upcoming_months: list[date]) -> dict:
    """
    Fetch 12-month Google Trends and score keywords by seasonal affiliate fit:
      - seasonal_score: peak interest in target months vs annual avg
      - momentum: recent 3-month growth vs annual avg
      - rising_related: breakout related product searches
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

                # Seasonal score: how strongly this keyword peaks in target months
                monthly_avg = series.groupby(series.index.month).mean()
                target_vals = [float(monthly_avg.get(m, 0)) for m in target_month_nums]
                peak_seasonal = max(target_vals) if target_vals else 0.0
                seasonal_score = min(peak_seasonal / (overall_avg + 0.01), 5.0)

                # Momentum: last ~13 weeks vs full-year avg
                recent_avg = float(series.tail(13).mean())
                momentum = min(recent_avg / (overall_avg + 0.01), 3.0)

                # Rising related queries (breakout product searches)
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
    """Synthesize trend data into a Claude-powered 3–6 month affiliate niche forecast."""
    month_labels = [m.strftime("%B %Y") for m in upcoming_months]

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

    prompt = f"""You are a TikTok affiliate marketing strategist specializing in short-form video product promotion.

Target forecast window: {', '.join(month_labels)}
Upcoming seasonal shopping moments: {', '.join(seasonal_events[:15])}

Google Trends 12-month analysis (seasonal_score = peak demand in target months vs annual avg; momentum = recent growth; rising_related = breakout product searches):
{trend_summary}

Task: Forecast the TOP 15 affiliate product niches for TikTok content during {month_labels[0]}–{month_labels[-1]}.

Focus on products with strong video potential, good affiliate commissions (Amazon Associates 3-8%, TikTok Shop 5-20%), and clear seasonal demand.

Return ONLY valid JSON:
{{
  "forecast_period": "{month_labels[0]} — {month_labels[-1]}",
  "generated_at": "{datetime.utcnow().strftime('%Y-%m-%d')}",
  "niches": [
    {{
      "niche": "product niche name",
      "product_type": "specific product type to promote (e.g. 'SPF 50 mineral sunscreen sticks')",
      "hook_pattern": "question|bold_claim|tutorial|curiosity_gap|reaction",
      "hook_text": "viral TikTok hook line (max 12 words)",
      "trend_score": 82,
      "affiliate_platform": "amazon|tiktok_shop|both",
      "est_commission_pct": 5.0,
      "rationale": "1-2 sentences: why this product category peaks in the target window",
      "hashtags": ["#tag1", "#tag2", "#tag3", "#fyp", "#tiktokmademebuyit"]
    }}
  ]
}}"""

    return ask_claude_json(prompt, max_tokens=3000)


def save_to_db(session, niches: list[dict]) -> int:
    """Upsert upcoming trend niches into the Trend table."""
    saved = 0
    for item in niches:
        niche_name = item.get("niche", "").strip()
        hook_text = item.get("hook_text", "").strip()
        if not niche_name:
            continue
        existing = session.query(Trend).filter_by(
            niche=niche_name, hook_text=hook_text
        ).first()
        if not existing:
            session.add(Trend(
                niche=niche_name,
                hook_pattern=item.get("hook_pattern", "curiosity_gap"),
                hook_text=hook_text,
                hashtags=",".join(item.get("hashtags", [])),
                views=int(item.get("trend_score", 50) * 1000),
            ))
            saved += 1
    return saved


def save_report(forecast: dict) -> None:
    """Write a markdown affiliate forecast report to reports/."""
    today = date.today()
    path = REPORTS_DIR / f"upcoming_trends_{today}.md"

    lines = [
        "# Upcoming TikTok Affiliate Trends Forecast",
        f"**Period:** {forecast.get('forecast_period', 'N/A')}",
        f"**Generated:** {forecast.get('generated_at', today)}",
        "",
        "| # | Niche | Product Type | Hook Pattern | Score | Platform | Est. Commission |",
        "|---|-------|-------------|--------------|-------|----------|-----------------|",
    ]
    for i, n in enumerate(forecast.get("niches", []), 1):
        lines.append(
            f"| {i} | {n.get('niche', '')} | {n.get('product_type', '')} "
            f"| {n.get('hook_pattern', '')} | {n.get('trend_score', '')} "
            f"| {n.get('affiliate_platform', '')} | {n.get('est_commission_pct', '')}% |"
        )

    lines += ["", "## Analysis & Hooks", ""]
    for i, n in enumerate(forecast.get("niches", []), 1):
        lines.append(f"**{i}. {n.get('niche', '')}** — {n.get('rationale', '')}")
        lines.append(f"   Hook: *\"{n.get('hook_text', '')}\"*")
        lines.append(f"   Tags: {', '.join(n.get('hashtags', []))}")
        lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")
    logger.info(f"Report saved: {path}")


def run():
    logger.info("=== Upcoming TikTok Affiliate Trends Research started (3–6 month forecast) ===")

    upcoming_months = get_upcoming_months(start=3, end=6)
    seasonal_events = get_seasonal_events(upcoming_months)
    logger.info(f"Target window: {upcoming_months[0]} → {upcoming_months[-1]}")
    logger.info(f"Seasonal opportunities detected: {seasonal_events[:8]}")

    all_keywords = [kw for kws in AFFILIATE_CATEGORIES.values() for kw in kws]
    logger.info(f"Fetching pytrends data for {len(all_keywords)} keywords...")
    trend_data = fetch_pytrends_seasonal(all_keywords, upcoming_months)
    logger.info(f"Trend data collected for {len(trend_data)} keywords")

    if not trend_data:
        logger.warning("No trend data retrieved — check pytrends connectivity")
        return

    logger.info("Generating Claude AI affiliate niche forecast...")
    forecast = build_claude_forecast(trend_data, seasonal_events, upcoming_months)
    niches = forecast.get("niches", [])
    logger.info(f"Claude forecast: {len(niches)} affiliate niches identified")

    save_report(forecast)

    session = SessionLocal()
    try:
        saved = save_to_db(session, niches)
        session.commit()
        logger.info(f"Saved {saved} new upcoming affiliate trend niches to DB")
    except Exception as e:
        session.rollback()
        logger.error(f"DB save failed: {e}")
    finally:
        session.close()

    logger.info("=== Upcoming TikTok Affiliate Trends Research complete ===")
    return forecast


if __name__ == "__main__":
    run()
