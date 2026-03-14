"""Tests for the research module."""

import pytest
from unittest.mock import patch, MagicMock
from modules.01_research.tiktok_trends import scrape_trends, _fallback_trending
from modules.01_research.shop_products import scrape_products, _fallback_products
from modules.01_research.competitor import _fallback_videos


def test_fallback_trending():
    """Test fallback trending data returns valid data."""
    trends = _fallback_trending()
    assert len(trends) > 0
    assert all("hashtag_name" in t for t in trends)
    assert all("use_count" in t for t in trends)


def test_fallback_products():
    """Test fallback products filter by commission rate."""
    products = _fallback_products(min_commission=15.0)
    assert all(p["commission_rate"] >= 15.0 for p in products)

    products_all = _fallback_products(min_commission=0)
    assert len(products_all) >= len(products)


def test_fallback_videos():
    """Test fallback video data."""
    videos = _fallback_videos("test")
    assert len(videos) > 0
    assert all("id" in v for v in videos)
    assert all("title" in v for v in videos)


@patch("modules.01_research.tiktok_trends.httpx.Client")
def test_scrape_trends_fallback_on_error(mock_client):
    """Test that scraper falls back gracefully on API error."""
    mock_client.side_effect = Exception("API unavailable")
    # Should use fallback and not crash
    with patch("modules.01_research.tiktok_trends.SessionLocal") as mock_session:
        mock_db = MagicMock()
        mock_session.return_value = mock_db
        count = scrape_trends("fake_token")
        assert count > 0
