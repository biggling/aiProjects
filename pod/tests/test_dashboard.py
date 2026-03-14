import base64

import pytest
from fastapi.testclient import TestClient

from app.main import app
from tools.shared.db import engine
from tools.shared.models import Base


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture
def client():
    return TestClient(app)


def _auth_headers():
    creds = base64.b64encode(b"admin:changeme").decode()
    return {"Authorization": f"Basic {creds}"}


def test_overview_requires_auth(client):
    resp = client.get("/")
    assert resp.status_code == 401


def test_overview(client):
    resp = client.get("/", headers=_auth_headers())
    assert resp.status_code == 200
    assert "Dashboard Overview" in resp.text


def test_tasks_page(client):
    resp = client.get("/tasks", headers=_auth_headers())
    assert resp.status_code == 200
    assert "Task Control Panel" in resp.text


def test_designs_page(client):
    resp = client.get("/designs", headers=_auth_headers())
    assert resp.status_code == 200
    assert "Design Review" in resp.text


def test_listings_page(client):
    resp = client.get("/listings", headers=_auth_headers())
    assert resp.status_code == 200
    assert "Listings" in resp.text


def test_niches_page(client):
    resp = client.get("/niches", headers=_auth_headers())
    assert resp.status_code == 200
    assert "Niche Rankings" in resp.text


def test_logs_page(client):
    resp = client.get("/logs", headers=_auth_headers())
    assert resp.status_code == 200
    assert "Log Viewer" in resp.text


def test_report_page(client):
    resp = client.get("/report", headers=_auth_headers())
    assert resp.status_code == 200
    assert "Weekly Reports" in resp.text
