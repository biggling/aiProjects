import pytest
from unittest.mock import patch, MagicMock

from tools.shared.db import engine, get_session
from tools.shared.models import Base, Niche, Listing
from tools.upload.etsy_uploader import run


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@patch("tools.upload.etsy_uploader.create_etsy_listing")
def test_run(mock_create):
    mock_create.return_value = "etsy_789"

    with get_session() as session:
        niche = Niche(keyword="test", trend_score=80, status="active")
        session.add(niche)
        session.flush()
        listing = Listing(
            niche_id=niche.id, title="Test Shirt",
            description="A test", tags=["test"],
            printify_product_id="prod_456", status="copy_ready",
        )
        session.add(listing)

    result = run()
    assert "1 listings uploaded" in result

    with get_session() as session:
        l = session.query(Listing).first()
        assert l.etsy_listing_id == "etsy_789"
        assert l.status == "live"
        assert l.uploaded_at is not None


def test_run_no_listings():
    result = run()
    assert "0 listings uploaded" in result
