import os
import pytest
from unittest.mock import patch, MagicMock

from tools.shared.db import engine, get_session
from tools.shared.models import Base, Niche, Listing
from tools.analytics.weekly_report import gather_data, run


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


def test_gather_data():
    with get_session() as session:
        niche = Niche(keyword="cats", trend_score=90, status="active")
        session.add(niche)
        session.flush()
        session.add(Listing(
            niche_id=niche.id, title="Cat Shirt",
            status="live", revenue=150.0, views=500,
        ))

    data = gather_data()
    assert data["total_revenue"] == 150.0
    assert data["total_views"] == 500
    assert data["total_listings"] == 1


@patch("tools.analytics.weekly_report.notify")
@patch("tools.analytics.weekly_report.get_anthropic")
def test_run(mock_get_anthropic, mock_notify):
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.content = [MagicMock(text="## Summary\nGreat week!")]
    mock_client.messages.create.return_value = mock_response
    mock_get_anthropic.return_value = mock_client

    with get_session() as session:
        niche = Niche(keyword="cats", trend_score=90, status="active")
        session.add(niche)
        session.flush()
        session.add(Listing(
            niche_id=niche.id, title="Cat Shirt",
            status="live", revenue=100.0, views=300,
        ))

    result = run()
    assert "Report saved" in result
    mock_client.messages.create.assert_called_once()

    # Clean up report file
    import glob
    for f in glob.glob("data/logs/report_*.md"):
        os.remove(f)
