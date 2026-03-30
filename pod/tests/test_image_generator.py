import os
import pytest
from unittest.mock import patch, MagicMock

from tools.shared.db import engine, get_session
from tools.shared.models import Base, Niche, Prompt, Design
from tools.design.image_generator import generate_image, run


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@patch("tools.design.image_generator._generate_stability")
def test_generate_image(mock_stability, tmp_path):
    """generate_image routes to stability backend and returns (True, 'stability', params)."""
    output = str(tmp_path / "test.png")
    mock_stability.return_value = {"model": "sdxl", "backend": "stability"}

    # Force stability backend so the test doesn't depend on Gemini/DALL-E credentials
    success, backend, params = generate_image("a cute cat", output, preferred_backend="stability")

    assert success is True
    assert backend == "stability"
    assert params["backend"] == "stability"
    mock_stability.assert_called_once()


@patch("tools.design.image_generator._generate_stability")
@patch("tools.design.image_generator._generate_gemini")
@patch("tools.design.image_generator._generate_dalle")
def test_generate_image_failure(mock_dalle, mock_gemini, mock_stability, tmp_path):
    """generate_image returns (False, 'none', {}) when all backends fail."""
    mock_gemini.return_value = None
    mock_stability.return_value = None
    mock_dalle.return_value = None

    output = str(tmp_path / "fail.png")
    success, backend, params = generate_image("a cute cat", output)

    assert success is False
    assert backend == "none"
    assert params == {}


@patch("tools.design.image_generator.generate_image")
def test_run(mock_gen):
    """run() processes pending prompts and creates Design rows."""
    mock_gen.return_value = (True, "gemini", {"backend": "gemini"})

    with get_session() as session:
        niche = Niche(keyword="test", trend_score=80, status="active")
        session.add(niche)
        session.flush()
        niche_id = niche.id

        for i in range(3):
            session.add(Prompt(
                niche_id=niche_id,
                prompt_text=f"test prompt {i}",
                status="pending",
            ))

    result = run()
    assert "3 images generated" in result

    with get_session() as session:
        designs = session.query(Design).all()
        assert len(designs) == 3
        assert all(d.status == "generated" for d in designs)
        assert all(d.image_backend == "gemini" for d in designs)


@patch("tools.design.image_generator.generate_image")
def test_run_no_prompts(mock_gen):
    result = run()
    assert "0 images generated" in result
    mock_gen.assert_not_called()
