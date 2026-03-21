"""Tests for FastAPI dashboard endpoints."""

import pytest
from fastapi.testclient import TestClient

from app.main import app
from tools.shared.db import get_session, init_db
from tools.shared.models import Niche, Design, Listing, Prompt


@pytest.fixture
def client(setup_db):
    """Create test client with fresh DB."""
    init_db()
    return TestClient(app)


@pytest.fixture
def seeded_db(setup_db):
    """Seed DB with test data."""
    init_db()
    with get_session() as session:
        niche = Niche(keyword="test-niche", trend_score=80, final_score=75, status="active")
        session.add(niche)
        session.flush()

        prompt = Prompt(niche_id=niche.id, prompt_text="test prompt", status="pending")
        session.add(prompt)
        session.flush()

        design = Design(
            prompt_id=prompt.id, niche_id=niche.id,
            raw_path="/tmp/raw.png", status="approved",
        )
        session.add(design)
        session.flush()

        listing = Listing(
            design_id=design.id, niche_id=niche.id,
            title="Test Product", status="live",
            views=100, favorites=10, sales=2, revenue=25.99,
        )
        session.add(listing)

    return TestClient(app)


class TestDashboard:
    def test_dashboard_loads(self, client):
        resp = client.get("/")
        assert resp.status_code == 200

    def test_niches_page(self, seeded_db):
        resp = seeded_db.get("/niches/")
        assert resp.status_code == 200

    def test_designs_page(self, seeded_db):
        resp = seeded_db.get("/designs/")
        assert resp.status_code == 200

    def test_listings_page(self, seeded_db):
        resp = seeded_db.get("/listings/")
        assert resp.status_code == 200
