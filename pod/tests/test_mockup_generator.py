import os
import pytest
from unittest.mock import patch, MagicMock

from PIL import Image

from tools.shared.db import engine, get_session
from tools.shared.models import Base, Niche, Prompt, Design
from tools.design.mockup_generator import run


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@patch("tools.design.mockup_generator.create_printify_mockup")
def test_run(mock_create, tmp_path):
    mockup_path = str(tmp_path / "mockup.png")
    Image.new("RGB", (100, 100)).save(mockup_path)
    mock_create.return_value = mockup_path

    # Create test data
    img_path = str(tmp_path / "processed.png")
    Image.new("RGB", (100, 100)).save(img_path)

    with get_session() as session:
        niche = Niche(keyword="test", trend_score=80, status="active")
        session.add(niche)
        session.flush()
        prompt = Prompt(niche_id=niche.id, prompt_text="test", status="generated")
        session.add(prompt)
        session.flush()
        design = Design(
            prompt_id=prompt.id, niche_id=niche.id,
            processed_path=img_path, status="approved",
        )
        session.add(design)

    result = run()
    assert "1 mockups generated" in result

    with get_session() as session:
        d = session.query(Design).first()
        assert d.status == "mockup_ready"
        assert d.mockup_path is not None


@patch("tools.design.mockup_generator.create_printify_mockup")
def test_run_no_designs(mock_create):
    result = run()
    assert "0 mockups generated" in result
    mock_create.assert_not_called()


@patch("tools.design.mockup_generator.requests")
def test_create_printify_mockup(mock_requests, tmp_path):
    from tools.design.mockup_generator import create_printify_mockup

    # Create test image
    img_path = str(tmp_path / "design.png")
    Image.new("RGB", (100, 100)).save(img_path)

    # Mock upload response
    upload_resp = MagicMock()
    upload_resp.status_code = 200
    upload_resp.json.return_value = {"id": "img_123"}

    # Mock product create response
    product_resp = MagicMock()
    product_resp.status_code = 200
    product_resp.json.return_value = {
        "images": [{"src": "https://example.com/mockup.png"}]
    }

    # Mock image download
    img_resp = MagicMock()
    img_resp.status_code = 200
    img_resp.content = b"\x89PNG" + b"\x00" * 100

    mock_requests.post.side_effect = [upload_resp, product_resp]
    mock_requests.get.return_value = img_resp

    result = create_printify_mockup(1, img_path)
    assert result is not None
    assert "mockup" in result
