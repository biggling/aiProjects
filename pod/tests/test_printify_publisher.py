import pytest
from unittest.mock import patch, MagicMock

from PIL import Image

from tools.shared.db import engine, get_session
from tools.shared.models import Base, Niche, Prompt, Design, Listing
from tools.upload.printify_publisher import run


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@patch("tools.upload.printify_publisher.publish_product")
@patch("tools.upload.printify_publisher.create_product")
@patch("tools.upload.printify_publisher.upload_image")
def test_run(mock_upload, mock_create, mock_publish, tmp_path):
    mock_upload.return_value = "img_123"
    mock_create.return_value = "prod_456"
    mock_publish.return_value = True

    # Create test image
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
            processed_path=img_path, status="mockup_ready",
        )
        session.add(design)
        session.flush()
        listing = Listing(
            design_id=design.id, niche_id=niche.id,
            title="Test Shirt", description="A test", tags=["test"],
            status="copy_ready",
        )
        session.add(listing)

    result = run()
    assert "1 products published" in result

    mock_upload.assert_called_once()
    mock_create.assert_called_once()
    mock_publish.assert_called_once()

    with get_session() as session:
        l = session.query(Listing).first()
        assert l.printify_product_id == "prod_456"


def test_run_no_listings():
    result = run()
    assert "0 products published" in result
