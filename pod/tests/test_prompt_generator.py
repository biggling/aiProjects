import pytest
from unittest.mock import patch, MagicMock
import json

from tools.shared.db import engine, get_session
from tools.shared.models import Base, Niche, Prompt
from tools.design.prompt_generator import generate_prompts_for_niche, run


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@patch("tools.design.prompt_generator.get_anthropic")
def test_generate_prompts_for_niche(mock_get_anthropic):
    prompts = [f"prompt {i}" for i in range(50)]
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.content = [MagicMock(text=json.dumps(prompts))]
    mock_client.messages.create.return_value = mock_response
    mock_get_anthropic.return_value = mock_client

    result = generate_prompts_for_niche("funny cat")
    assert len(result) == 50
    mock_client.messages.create.assert_called_once()


@patch("tools.design.prompt_generator.get_anthropic")
def test_run(mock_get_anthropic):
    # Insert test niche
    with get_session() as session:
        session.add(Niche(
            keyword="cat mom", trend_score=90, velocity=1.0,
            competition=0.3, final_score=85, status="active",
        ))

    prompts = [f"design prompt {i}" for i in range(50)]
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.content = [MagicMock(text=json.dumps(prompts))]
    mock_client.messages.create.return_value = mock_response
    mock_get_anthropic.return_value = mock_client

    result = run()
    assert "50 prompts generated" in result

    with get_session() as session:
        count = session.query(Prompt).count()
        assert count == 50
        first = session.query(Prompt).first()
        assert first.status == "pending"
        assert first.niche_id is not None


@patch("tools.design.prompt_generator.get_anthropic")
def test_run_no_niches(mock_get_anthropic):
    result = run()
    assert "0 prompts generated" in result
    mock_get_anthropic.assert_not_called()
