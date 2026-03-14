import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from tools.shared.db import engine, get_session
from tools.shared.models import Base, Niche
from tools.trend.etsy_scraper import scrape_etsy_keyword, run


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.mark.asyncio
async def test_scrape_etsy_keyword():
    page = AsyncMock()

    # Mock listings with sales data
    listing1 = AsyncMock()
    listing1.inner_text.return_value = "Funny Cat Shirt - 2,500 sales - $19.99"
    listing2 = AsyncMock()
    listing2.inner_text.return_value = "Cat Mom Tee - 500 sales - $22.00"

    page.query_selector_all.return_value = [listing1, listing2]

    competition = await scrape_etsy_keyword(page, "funny cat shirt")

    assert 0.0 <= competition <= 1.0
    page.goto.assert_called_once()


@pytest.mark.asyncio
async def test_scrape_etsy_keyword_no_sales():
    page = AsyncMock()
    listing = AsyncMock()
    listing.inner_text.return_value = "Some product with no sales info"
    page.query_selector_all.return_value = [listing]

    competition = await scrape_etsy_keyword(page, "test keyword")
    assert competition == 0.5  # default when listings exist but no sales data


@patch("tools.trend.etsy_scraper._scrape_all")
def test_run(mock_scrape_all):
    # Insert test niches
    with get_session() as session:
        n1 = Niche(keyword="cat mom", trend_score=80, status="active")
        n2 = Niche(keyword="dog dad", trend_score=60, status="active")
        session.add_all([n1, n2])
        session.flush()
        id1, id2 = n1.id, n2.id

    mock_scrape_all.return_value = {id1: 0.75, id2: 0.3}

    result = run()
    assert "2 niches scraped" in result

    with get_session() as session:
        n1 = session.get(Niche, id1)
        n2 = session.get(Niche, id2)
        assert n1.competition == 0.75
        assert n2.competition == 0.3


@patch("tools.trend.etsy_scraper._scrape_all")
def test_run_no_niches(mock_scrape_all):
    result = run()
    assert "0 niches scraped" in result
    mock_scrape_all.assert_not_called()
