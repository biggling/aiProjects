import os
import pytest
from unittest.mock import patch, MagicMock

from PIL import Image

from tools.shared.db import engine, get_session
from tools.shared.models import Base, Niche, Prompt, Design
from tools.design.clip_filter import run


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@patch("tools.design.clip_filter.compute_clip_score")
def test_run_approve(mock_clip, tmp_path):
    mock_clip.return_value = 0.35  # above threshold

    # Create test image
    img_path = str(tmp_path / "test.png")
    Image.new("RGB", (100, 100), (255, 0, 0)).save(img_path)

    with get_session() as session:
        niche = Niche(keyword="cat shirt", trend_score=80, status="active")
        session.add(niche)
        session.flush()

        prompt = Prompt(niche_id=niche.id, prompt_text="test", status="generated")
        session.add(prompt)
        session.flush()

        design = Design(
            prompt_id=prompt.id, niche_id=niche.id,
            processed_path=img_path, status="processed",
        )
        session.add(design)

    result = run()
    assert "1 approved" in result

    with get_session() as session:
        d = session.query(Design).first()
        assert d.status == "approved"
        assert d.clip_score == 0.35


@patch("tools.design.clip_filter.compute_clip_score")
def test_run_reject(mock_clip, tmp_path):
    mock_clip.return_value = 0.10  # below threshold

    img_path = str(tmp_path / "test.png")
    Image.new("RGB", (100, 100), (0, 0, 0)).save(img_path)

    with get_session() as session:
        niche = Niche(keyword="random noise", trend_score=80, status="active")
        session.add(niche)
        session.flush()

        prompt = Prompt(niche_id=niche.id, prompt_text="test", status="generated")
        session.add(prompt)
        session.flush()

        design = Design(
            prompt_id=prompt.id, niche_id=niche.id,
            processed_path=img_path, status="processed",
        )
        session.add(design)

    result = run()
    assert "1 rejected" in result

    with get_session() as session:
        d = session.query(Design).first()
        assert d.status == "rejected"


def test_run_no_designs():
    result = run()
    assert "0 designs filtered" in result
