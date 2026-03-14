import pytest
from unittest.mock import patch

from tools.shared.db import engine, get_session
from tools.shared.models import Base, Niche
from tools.upload.price_adjuster import generate_report, run


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


def test_generate_report_warning():
    report = generate_report("test", 40.00, [20.0, 22.0, 25.0, 18.0])
    assert "WARNING" in report


def test_generate_report_recommendation():
    report = generate_report("test", 22.00, [20.0, 22.0, 25.0, 30.0])
    assert "RECOMMENDATION" in report or "competitive" in report


def test_generate_report_no_prices():
    report = generate_report("test", 25.00, [])
    assert "No competitor prices" in report


@patch("tools.upload.price_adjuster.asyncio.run")
def test_run(mock_run):
    mock_run.return_value = [19.99, 24.99, 29.99]

    with get_session() as session:
        session.add(Niche(keyword="test", trend_score=80, status="active"))

    result = run()
    assert "1 niches checked" in result


def test_run_no_niches():
    result = run()
    assert "0 niches checked" in result
