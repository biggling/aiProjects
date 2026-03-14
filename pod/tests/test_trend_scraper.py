import pytest
from unittest.mock import patch, MagicMock
import pandas as pd

from tools.shared.db import engine, get_session
from tools.shared.models import Base, Niche
from tools.trend.trend_scraper import fetch_trends, upsert_niches, run


@pytest.fixture(autouse=True)
def setup_db():
    """Create tables before each test, drop after."""
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


def _mock_pytrends():
    """Return a mock TrendReq that returns predictable data."""
    mock = MagicMock()

    # interest_over_time returns a DataFrame
    dates = pd.date_range("2025-12-01", periods=12, freq="W")
    iot_data = {
        "funny cat shirt": [10, 20, 30, 40, 50, 60, 70, 80, 90, 95, 98, 100],
        "isPartial": [False] * 12,
    }
    iot_df = pd.DataFrame(iot_data, index=dates)
    mock.interest_over_time.return_value = iot_df

    # related_queries
    rising_df = pd.DataFrame({
        "query": ["funny cat meme shirt", "cat lover tee"],
        "value": [200, 150],
    })
    mock.related_queries.return_value = {
        "funny cat shirt": {"top": None, "rising": rising_df},
    }

    return mock


@patch("tools.trend.trend_scraper.TrendReq")
def test_fetch_trends(mock_trend_req_cls):
    mock_trend_req_cls.return_value = _mock_pytrends()

    results = fetch_trends(["funny cat shirt"])

    assert "funny cat shirt" in results
    assert results["funny cat shirt"]["trend_score"] > 0
    assert "funny cat meme shirt" in results  # from rising queries


@patch("tools.trend.trend_scraper.TrendReq")
def test_upsert_niches(mock_trend_req_cls):
    trends = {
        "test keyword": {"trend_score": 75.0, "velocity": 0.5},
        "another keyword": {"trend_score": 30.0, "velocity": -0.1},
    }

    count = upsert_niches(trends)
    assert count == 2

    with get_session() as session:
        niches = session.query(Niche).all()
        assert len(niches) == 2
        kw_map = {n.keyword: n for n in niches}
        assert kw_map["test keyword"].trend_score == 75.0
        assert kw_map["another keyword"].velocity == -0.1


@patch("tools.trend.trend_scraper.TrendReq")
def test_upsert_updates_existing(mock_trend_req_cls):
    # Insert first
    upsert_niches({"test kw": {"trend_score": 50.0, "velocity": 0.2}})

    # Update
    upsert_niches({"test kw": {"trend_score": 80.0, "velocity": 0.9}})

    with get_session() as session:
        niche = session.query(Niche).filter_by(keyword="test kw").one()
        assert niche.trend_score == 80.0
        assert niche.velocity == 0.9


@patch("tools.trend.trend_scraper.TrendReq")
@patch("tools.trend.trend_scraper.SEED_KEYWORDS", ["funny cat shirt"])
def test_run(mock_trend_req_cls):
    mock_trend_req_cls.return_value = _mock_pytrends()

    result = run()

    assert "niches updated" in result
    with get_session() as session:
        niches = session.query(Niche).all()
        assert len(niches) > 0
