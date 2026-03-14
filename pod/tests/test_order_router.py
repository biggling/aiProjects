import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from fastapi import FastAPI

from tools.shared.db import engine, get_session
from tools.shared.models import Base, Niche, Listing
from tools.upload.order_router import router


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture
def client():
    app = FastAPI()
    app.include_router(router)
    return TestClient(app)


@patch("tools.upload.order_router.requests.post")
def test_handle_etsy_order(mock_post, client):
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {"id": "order_123"}
    mock_post.return_value = mock_resp

    with get_session() as session:
        niche = Niche(keyword="test", trend_score=80, status="active")
        session.add(niche)
        session.flush()
        listing = Listing(
            niche_id=niche.id, title="Test",
            etsy_listing_id="12345",
            printify_product_id="prod_456",
            status="live",
        )
        session.add(listing)

    payload = {
        "receipt_id": "receipt_001",
        "transactions": [{"listing_id": "12345", "quantity": 1}],
        "first_name": "John",
        "last_name": "Doe",
        "address": {
            "first_line": "123 Main St",
            "city": "Portland",
            "state": "OR",
            "zip": "97201",
            "country_iso": "US",
        },
    }

    response = client.post("/webhook/etsy-order", json=payload)
    assert response.status_code == 200
    assert response.json()["orders_created"] == 1
    mock_post.assert_called_once()
