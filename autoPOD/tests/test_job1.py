"""Tests for Job 1: Trend Research"""
import pytest
from unittest.mock import patch, MagicMock
from jobs.job1_trend_research import score_niche, fetch_google_trends, SEED_KEYWORDS


def test_score_niche_basic():
    score = score_niche(trend_score=80.0, competition=0.2)
    assert score > 0


def test_score_niche_zero_competition():
    score = score_niche(trend_score=50.0, competition=0.0)
    assert score > 0


def test_score_niche_high_competition_lower_score():
    low_comp = score_niche(80.0, 0.1)
    high_comp = score_niche(80.0, 0.9)
    assert low_comp > high_comp


@patch("jobs.job1_trend_research.TrendReq")
def test_fetch_google_trends_handles_error(mock_trends_cls):
    mock_instance = MagicMock()
    mock_instance.interest_over_time.side_effect = Exception("API error")
    mock_trends_cls.return_value = mock_instance
    result = fetch_google_trends(["test keyword"])
    assert isinstance(result, dict)


def test_seed_keywords_not_empty():
    assert len(SEED_KEYWORDS) > 0
