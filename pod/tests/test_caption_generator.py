import pytest
from unittest.mock import patch, MagicMock

from tools.shared.db import engine, get_session
from tools.shared.models import Base, Niche, Design, Listing
from tools.copy.caption_generator import generate_caption, run


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@patch("tools.copy.caption_generator.get_anthropic")
def test_generate_caption(mock_get_anthropic):
    mock_client = MagicMock()
    caption_text = "Love cats? This tee is purr-fect! #catmom #catshirt #catlover"
    mock_response = MagicMock()
    mock_response.content = [MagicMock(text=caption_text)]
    mock_client.messages.create.return_value = mock_response
    mock_get_anthropic.return_value = mock_client

    result = generate_caption("Funny Cat Mom Shirt", "cat mom")

    assert len(result) <= 200
    assert "#" in result


@patch("tools.copy.caption_generator.get_anthropic")
def test_run(mock_get_anthropic):
    caption_text = "Cat lovers unite! #catmom #catlover #tshirt"
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.content = [MagicMock(text=caption_text)]
    mock_client.messages.create.return_value = mock_response
    mock_get_anthropic.return_value = mock_client

    with get_session() as session:
        niche = Niche(keyword="cat mom", trend_score=90, status="active")
        session.add(niche)
        session.flush()
        listing = Listing(
            niche_id=niche.id, title="Cat Mom Shirt",
            description="A great shirt", tags=["cat"], status="copy_ready",
        )
        session.add(listing)

    result = run()
    assert "1 captions generated" in result

    with get_session() as session:
        l = session.query(Listing).first()
        assert l.caption is not None
        assert len(l.caption) <= 200


def test_run_no_listings():
    result = run()
    assert "0 captions generated" in result
