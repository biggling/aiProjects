import os
import pytest
from unittest.mock import patch

from PIL import Image

from tools.shared.db import engine, get_session
from tools.shared.models import Base, Niche, Prompt, Design
from tools.design.image_processor import process_image, run, TARGET_WIDTH, TARGET_HEIGHT


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture
def test_image(tmp_path):
    """Create a 200x200 test image."""
    img = Image.new("RGBA", (200, 200), (255, 0, 0, 255))
    path = str(tmp_path / "test_raw.png")
    img.save(path, "PNG")
    return path


@patch("tools.design.image_processor.remove")
def test_process_image(mock_remove, test_image, tmp_path):
    # Mock rembg to return the same image data (just skip bg removal)
    with open(test_image, "rb") as f:
        mock_remove.return_value = f.read()

    output = str(tmp_path / "processed.png")
    result = process_image(test_image, output)

    assert result is True
    assert os.path.exists(output)

    # Verify output dimensions
    img = Image.open(output)
    assert img.size == (TARGET_WIDTH, TARGET_HEIGHT)


def test_process_image_missing_file(tmp_path):
    result = process_image("/nonexistent/path.png", str(tmp_path / "out.png"))
    assert result is False


@patch("tools.design.image_processor.process_image")
def test_run(mock_process, tmp_path):
    mock_process.return_value = True

    # Insert test data
    with get_session() as session:
        niche = Niche(keyword="test", trend_score=80, status="active")
        session.add(niche)
        session.flush()

        prompt = Prompt(niche_id=niche.id, prompt_text="test", status="generated")
        session.add(prompt)
        session.flush()

        raw_path = str(tmp_path / "raw.png")
        Image.new("RGBA", (100, 100)).save(raw_path)
        design = Design(
            prompt_id=prompt.id, niche_id=niche.id,
            raw_path=raw_path, status="generated",
        )
        session.add(design)

    result = run()
    assert "1 designs processed" in result

    with get_session() as session:
        d = session.query(Design).first()
        assert d.status == "processed"
        assert d.processed_path is not None
