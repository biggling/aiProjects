import json
import pytest
from unittest.mock import patch, MagicMock

from tools.shared.db import engine, get_session
from tools.shared.models import Base, Niche, Prompt, Design, Listing
from tools.copy.copy_generator import generate_copy, run


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


def _mock_copy_response():
    return {
        "title": "Funny Cat Mom Shirt - Cat Lover Gift - Cute Kitten Tee",
        "description": "Show your love for cats!\n- Premium soft cotton\n- Unisex fit\n- Machine washable\n- Perfect gift\n- Vibrant print",
        "tags": ["cat mom", "cat shirt", "cat lover", "kitten tee", "cat gift",
                 "funny cat", "cat lady", "pet lover", "animal shirt", "cat owner",
                 "cute cat", "cat apparel", "meow shirt"],
    }


@patch("tools.copy.copy_generator.get_anthropic")
def test_generate_copy(mock_get_anthropic):
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.content = [MagicMock(text=json.dumps(_mock_copy_response()))]
    mock_client.messages.create.return_value = mock_response
    mock_get_anthropic.return_value = mock_client

    result = generate_copy("cat mom")

    assert "title" in result
    assert "description" in result
    assert "tags" in result
    assert len(result["tags"]) == 13


@patch("tools.copy.copy_generator.get_anthropic")
def test_run(mock_get_anthropic):
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.content = [MagicMock(text=json.dumps(_mock_copy_response()))]
    mock_client.messages.create.return_value = mock_response
    mock_get_anthropic.return_value = mock_client

    with get_session() as session:
        niche = Niche(keyword="cat mom", trend_score=90, status="active")
        session.add(niche)
        session.flush()
        prompt = Prompt(niche_id=niche.id, prompt_text="test", status="generated")
        session.add(prompt)
        session.flush()
        design = Design(
            prompt_id=prompt.id, niche_id=niche.id,
            status="mockup_ready", mockup_path="/tmp/mock.png",
        )
        session.add(design)

    result = run()
    assert "1 listings created" in result

    with get_session() as session:
        listing = session.query(Listing).first()
        assert listing is not None
        assert listing.title is not None
        assert listing.description is not None
        assert len(listing.tags) == 13
        assert listing.status == "copy_ready"


def test_run_no_designs():
    result = run()
    assert "0 listings created" in result
