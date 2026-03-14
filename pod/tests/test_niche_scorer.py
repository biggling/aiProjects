import pytest

from tools.shared.db import engine, get_session
from tools.shared.models import Base, Niche
from tools.trend.niche_scorer import compute_score, run


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


def test_compute_score_basic():
    # (80 * 0.5) / 0.4 = 100
    assert compute_score(80, 0.5, 0.4) == 100.0


def test_compute_score_zero_competition():
    # Should use 0.1 as minimum: (50 * 1.0) / 0.1 = 500
    assert compute_score(50, 1.0, 0.0) == 500.0


def test_compute_score_none_values():
    assert compute_score(None, None, None) == 0.0


def test_run_scoring():
    with get_session() as session:
        session.add_all([
            Niche(keyword="high scorer", trend_score=90, velocity=1.5, competition=0.2, status="active"),
            Niche(keyword="mid scorer", trend_score=50, velocity=0.5, competition=0.5, status="active"),
            Niche(keyword="low scorer", trend_score=10, velocity=0.1, competition=0.9, status="active"),
        ])

    result = run()
    assert "3 niches scored" in result

    with get_session() as session:
        niches = {n.keyword: n for n in session.query(Niche).all()}

        # High scorer should be 100 (it's the max)
        assert niches["high scorer"].final_score == 100.0

        # Low scorer should be killed (score < 10)
        assert niches["low scorer"].final_score < 10
        assert niches["low scorer"].status == "killed"

        # Mid scorer should be between
        assert 0 < niches["mid scorer"].final_score < 100


def test_run_no_niches():
    result = run()
    assert "0 niches scored" in result
