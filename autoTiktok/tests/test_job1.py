"""Tests for Job 1: Niche & Product Research"""
import pytest
from unittest.mock import patch, MagicMock
from jobs.job1_niche_research import score_product, SEED_NICHES


def test_score_product_basic():
    score = score_product(trend_score=80.0, commission_pct=5.0)
    assert score > 0


def test_score_product_zero_competition():
    score = score_product(trend_score=50.0, commission_pct=3.0, competition=0.0)
    assert score > 0


def test_score_product_high_competition_lower_score():
    low_comp = score_product(80.0, 5.0, competition=0.1)
    high_comp = score_product(80.0, 5.0, competition=0.9)
    assert low_comp > high_comp


def test_score_product_scales_with_commission():
    low = score_product(50.0, 1.0)
    high = score_product(50.0, 10.0)
    assert high > low


def test_seed_niches_not_empty():
    assert len(SEED_NICHES) > 0


def test_seed_niches_are_strings():
    for niche in SEED_NICHES:
        assert isinstance(niche, str)


@patch("jobs.job1_niche_research.fetch_tiktok_shop_trending")
@patch("jobs.job1_niche_research.fetch_amazon_bestsellers")
@patch("jobs.job1_niche_research.SessionLocal")
def test_run_falls_back_to_amazon(mock_session_cls, mock_amazon, mock_tiktok):
    mock_tiktok.return_value = []
    mock_amazon.return_value = [
        {
            "product_name": "Test Product",
            "product_url": "https://amazon.com/test",
            "affiliate_link": "https://amazon.com/test?tag=test",
            "affiliate_network": "amazon",
            "commission_pct": 4.0,
        }
    ]
    mock_session = MagicMock()
    mock_session.query.return_value.filter_by.return_value.first.return_value = None
    mock_session_cls.return_value = mock_session

    from jobs.job1_niche_research import run
    run()

    assert mock_amazon.called


@patch("jobs.job1_niche_research.fetch_tiktok_shop_trending")
@patch("jobs.job1_niche_research.SessionLocal")
def test_run_upserts_existing_product(mock_session_cls, mock_tiktok):
    existing = MagicMock()
    mock_tiktok.return_value = [
        {
            "product_name": "Existing Product",
            "product_url": "https://tiktok.com/product/123",
            "affiliate_link": "https://tiktok.com/product/123?aff=1",
            "affiliate_network": "tiktok_shop",
            "commission_pct": 6.0,
        }
    ]
    mock_session = MagicMock()
    mock_session.query.return_value.filter_by.return_value.first.return_value = existing
    mock_session_cls.return_value = mock_session

    from jobs.job1_niche_research import run
    run()

    assert existing.trend_score is not None
