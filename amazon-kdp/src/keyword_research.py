"""KDP keyword research helper.

Uses Amazon autocomplete to find long-tail keywords for book niches.
"""

from pathlib import Path
from datetime import datetime
import json
import requests
from loguru import logger
import argparse

DATA_DIR = Path(__file__).parent.parent / "research"
DATA_DIR.mkdir(parents=True, exist_ok=True)


def get_amazon_suggestions(query: str, marketplace: str = "com") -> list[str]:
    """Get Amazon search autocomplete suggestions.

    Uses Amazon's public completion API — no auth required.
    """
    url = f"https://completion.amazon.{marketplace}/api/2017/suggestions"
    params = {
        "prefix": query,
        "mid": "ATVPDKIKX0DER",  # US marketplace
        "alias": "stripbooks",    # Books department
        "fresh": 0,
        "limit": 11,
    }

    try:
        resp = requests.get(url, params=params, timeout=10, headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
        })
        resp.raise_for_status()
        data = resp.json()
        suggestions = [s.get("value", "") for s in data.get("suggestions", [])]
        logger.info(f"Got {len(suggestions)} suggestions for '{query}'")
        return suggestions
    except Exception as e:
        logger.warning(f"Amazon autocomplete failed for '{query}': {e}")
        return []


def expand_keywords(seed: str, depth: int = 2) -> list[str]:
    """Expand a seed keyword using alphabet soup technique.

    Appends a-z to the seed and collects all suggestions.
    """
    all_keywords = set()

    # Base suggestions
    base = get_amazon_suggestions(seed)
    all_keywords.update(base)

    if depth >= 1:
        # Alphabet expansion
        for letter in "abcdefghijklmnopqrstuvwxyz":
            expanded = get_amazon_suggestions(f"{seed} {letter}")
            all_keywords.update(expanded)

    if depth >= 2:
        # Prefix variations
        for prefix in ["best", "top", "cute", "funny", "personalized", "custom"]:
            expanded = get_amazon_suggestions(f"{prefix} {seed}")
            all_keywords.update(expanded)

    keywords = sorted(all_keywords)
    logger.info(f"Expanded '{seed}' to {len(keywords)} keywords")
    return keywords


def save_keywords(seed: str, keywords: list[str]):
    """Save keyword research results."""
    date_str = datetime.now().strftime("%Y-%m-%d")
    slug = seed.replace(" ", "_").lower()
    out_path = DATA_DIR / f"keywords_{slug}_{date_str}.json"

    data = {
        "seed": seed,
        "date": date_str,
        "count": len(keywords),
        "keywords": keywords,
    }

    with open(out_path, "w") as f:
        json.dump(data, f, indent=2)

    logger.info(f"Saved {len(keywords)} keywords to {out_path}")
    return out_path


def main():
    parser = argparse.ArgumentParser(description="KDP Keyword Research")
    parser.add_argument("--niche", type=str, required=True, help="Seed keyword/niche")
    parser.add_argument("--depth", type=int, default=1, choices=[0, 1, 2])
    args = parser.parse_args()

    keywords = expand_keywords(args.niche, depth=args.depth)
    save_keywords(args.niche, keywords)

    print(f"\nFound {len(keywords)} keywords for '{args.niche}':")
    for kw in keywords[:20]:
        print(f"  - {kw}")
    if len(keywords) > 20:
        print(f"  ... and {len(keywords) - 20} more (saved to file)")


if __name__ == "__main__":
    main()
