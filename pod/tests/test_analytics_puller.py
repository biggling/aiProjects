import pytest
from unittest.mock import patch, MagicMock

from tools.shared.db import engine, get_session
from tools.shared.models import Base, Niche, Listing
from tools.analytics.analytics_puller import fetch_listing_stats, run


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@patch("tools.analytics.analytics_puller.requests.get")
def test_fetch_listing_stats(mock_get):
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {"views": 150, "num_favorers": 12}
    mock_get.return_value = mock_resp

    stats = fetch_listing_stats("12345")
    assert stats["views"] == 150
    assert stats["num_favorers"] == 12


@patch("tools.analytics.analytics_puller.fetch_listing_stats")
def test_run(mock_fetch):
    mock_fetch.return_value = {"views": 100, "num_favorers": 5}

    with get_session() as session:
        niche = Niche(keyword="test", trend_score=80, status="active")
        session.add(niche)
        session.flush()
        listing = Listing(
            niche_id=niche.id, title="Test", etsy_listing_id="12345",
            status="live", revenue=50.0,
        )
        session.add(listing)

    result = run()
    assert "1 listings updated" in result

    with get_session() as session:
        l = session.query(Listing).first()
        assert l.views == 100
        assert l.favorites == 5


def test_run_no_listings():
    result = run()
    assert "0 listings updated" in result
