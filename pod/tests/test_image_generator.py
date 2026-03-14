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


@patch("tools.design.image_generator.requests.post")
def test_generate_image(mock_post, tmp_path):
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.content = b"\x89PNG\r\n\x1a\n" + b"\x00" * 100  # fake PNG
    mock_post.return_value = mock_resp

    output = str(tmp_path / "test.png")
    result = generate_image("a cute cat", output)

    assert result is True
    assert os.path.exists(output)
    mock_post.assert_called_once()


@patch("tools.design.image_generator.requests.post")
def test_generate_image_failure(mock_post, tmp_path):
    mock_resp = MagicMock()
    mock_resp.status_code = 500
    mock_resp.text = "Internal Server Error"
    mock_post.return_value = mock_resp

    output = str(tmp_path / "fail.png")
    result = generate_image("a cute cat", output)

    assert result is False


@patch("tools.design.image_generator.generate_image")
def test_run(mock_gen):
    mock_gen.return_value = True

    # Insert test data
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


@patch("tools.design.image_generator.generate_image")
def test_run_no_prompts(mock_gen):
    result = run()
    assert "0 images generated" in result
    mock_gen.assert_not_called()
