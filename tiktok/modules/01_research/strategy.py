"""AI content strategy engine — produces ranked daily content briefs."""

import json
import os
import sys
from datetime import date, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from dotenv import load_dotenv
from loguru import logger
from openai import OpenAI

from modules.01_research.db import SessionLocal, init_db
from modules.01_research.models import CompetitorHook, ContentBrief, Product, Trend

load_dotenv()

ANALYTICS_DIR = Path("data/analytics")
ANALYTICS_DIR.mkdir(parents=True, exist_ok=True)


def generate_brief(print_brief: bool = False) -> dict:
    """Generate a ranked content brief from today's research data."""
    init_db()
    db = SessionLocal()

    try:
        today = date.today().isoformat()

        # Load today's data
        trends = db.query(Trend).filter(Trend.date == today).all()
        products = db.query(Product).order_by(Product.rank.asc()).limit(10).all()
        hooks = (
            db.query(CompetitorHook)
            .order_by(CompetitorHook.view_count.desc())
            .limit(20)
            .all()
        )

        # Build prompt
        prompt = _build_strategy_prompt(trends, products, hooks)

        # Call GPT-4o
        client = OpenAI()
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a TikTok content strategist for a Thai affiliate marketing account. "
                        "Produce content ideas that combine trending topics with high-commission products. "
                        "Always respond with valid JSON only."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=2000,
            timeout=30,
            response_format={"type": "json_object"},
        )

        raw = response.choices[0].message.content
        ideas = json.loads(raw).get("ideas", json.loads(raw))
        if isinstance(ideas, dict):
            ideas = [ideas]

        # Validate and save
        brief_data = {"date": today, "ideas": ideas}
        brief_path = ANALYTICS_DIR / f"brief_{today}.json"
        brief_path.write_text(json.dumps(brief_data, ensure_ascii=False, indent=2))
        logger.info(f"Brief saved to {brief_path}")

        # Save to DB
        brief_record = ContentBrief(
            date=today,
            ideas_json=json.dumps(ideas, ensure_ascii=False),
            created_at=datetime.utcnow(),
        )
        db.add(brief_record)
        db.commit()

        if print_brief:
            _print_brief(ideas)

        return brief_data

    except Exception as e:
        db.rollback()
        logger.error(f"Brief generation failed: {e}")
        raise
    finally:
        db.close()


def _build_strategy_prompt(
    trends: list[Trend], products: list[Product], hooks: list[CompetitorHook]
) -> str:
    """Build the strategy prompt from research data."""
    trend_lines = "\n".join(
        [f"- #{t.hashtag} ({t.use_count:,} uses)" for t in trends if t.hashtag]
    ) or "- No trends available today"

    product_lines = "\n".join(
        [
            f"- {p.name} | {p.category} | ฿{p.price:.0f} | {p.commission_rate}% commission | Rank #{p.rank}"
            for p in products
        ]
    ) or "- No products available"

    hook_lines = "\n".join(
        [
            f"- \"{h.hook_text}\" ({h.view_count:,} views)"
            for h in hooks[:10]
        ]
    ) or "- No hooks available"

    return f"""Based on today's TikTok research data, produce 5 ranked content ideas.

## Trending Hashtags
{trend_lines}

## Top Affiliate Products
{product_lines}

## Top Competitor Hooks
{hook_lines}

## Requirements
- Each idea must pair a product with a trending angle
- Prioritize high-commission products with trending hashtags
- Hooks should be attention-grabbing in Thai
- Target 30-45 second video format

Return a JSON object with an "ideas" array. Each idea must have:
- rank (1-5)
- product_name (from the product list)
- angle (creative angle in Thai)
- hook_idea (first 3 seconds script hook in Thai)
- trending_sound (suggested trending sound or "original")
- hashtags (array of 5 relevant hashtags)
- estimated_difficulty ("low", "medium", or "high")
"""


def _print_brief(ideas: list[dict]) -> None:
    """Pretty-print the brief to terminal."""
    print("\n" + "=" * 60)
    print(f"  CONTENT BRIEF — {date.today().isoformat()}")
    print("=" * 60)

    for idea in ideas:
        rank = idea.get("rank", "?")
        print(f"\n  #{rank} | {idea.get('product_name', 'Unknown')}")
        print(f"  Angle: {idea.get('angle', 'N/A')}")
        print(f"  Hook: {idea.get('hook_idea', 'N/A')}")
        print(f"  Sound: {idea.get('trending_sound', 'N/A')}")
        print(f"  Tags: {', '.join(idea.get('hashtags', []))}")
        print(f"  Difficulty: {idea.get('estimated_difficulty', 'N/A')}")
        print("-" * 40)

    print()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate daily content brief")
    parser.add_argument("--print", dest="print_brief", action="store_true", help="Print brief to terminal")
    args = parser.parse_args()

    generate_brief(print_brief=args.print_brief)
