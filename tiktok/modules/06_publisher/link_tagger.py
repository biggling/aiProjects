"""UTM and affiliate link formatter."""

from urllib.parse import urlencode, urlparse, urlunparse, parse_qs

import yaml
from pathlib import Path
from loguru import logger


def format_affiliate_link(
    product_id: str,
    video_id: int,
    products_path: Path = Path("config/products.yaml"),
) -> str:
    """Build affiliate link with UTM params for a product."""
    products_data = yaml.safe_load(products_path.read_text())
    products = products_data.get("products", [])

    product = next((p for p in products if p["id"] == product_id), None)
    if not product or not product.get("affiliate_link"):
        logger.warning(f"No affiliate link for product {product_id}")
        return ""

    base_url = product["affiliate_link"]
    utm_params = {
        "utm_source": product.get("utm_source", "tiktok"),
        "utm_medium": "video",
        "utm_campaign": product.get("utm_campaign", ""),
        "utm_content": f"video_{video_id}",
    }

    # Parse existing URL and append UTM params
    parsed = urlparse(base_url)
    existing_params = parse_qs(parsed.query)
    existing_params.update(utm_params)
    new_query = urlencode(existing_params, doseq=True)
    tagged_url = urlunparse(parsed._replace(query=new_query))

    logger.info(f"Tagged link for {product_id}: {tagged_url}")
    return tagged_url
