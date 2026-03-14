import pytest
from datetime import datetime, timezone, timedelta

from tools.shared.db import engine, get_session
from tools.shared.models import Base, Niche, Listing
from tools.analytics.performance_flagger import run


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


def test_flags_underperforming():
    old_date = datetime.now(timezone.utc) - timedelta(days=10)

    with get_session() as session:
        niche = Niche(keyword="test", trend_score=80, status="active")
        session.add(niche)
        session.flush()
        listing = Listing(
            niche_id=niche.id, title="Bad Seller",
            status="live", uploaded_at=old_date,
            views=20, favorites=1,
        )
        session.add(listing)

    result = run()
    assert "1 listings flagged" in result

    with get_session() as session:
        l = session.query(Listing).first()
        assert l.status == "underperforming"


def test_does_not_flag_good_performer():
    old_date = datetime.now(timezone.utc) - timedelta(days=10)

    with get_session() as session:
        niche = Niche(keyword="test", trend_score=80, status="active")
        session.add(niche)
        session.flush()
        listing = Listing(
            niche_id=niche.id, title="Good Seller",
            status="live", uploaded_at=old_date,
            views=200, favorites=15,
        )
        session.add(listing)

    result = run()
    assert "0 listings flagged" in result


def test_does_not_flag_recent():
    recent = datetime.now(timezone.utc) - timedelta(days=2)

    with get_session() as session:
        niche = Niche(keyword="test", trend_score=80, status="active")
        session.add(niche)
        session.flush()
        listing = Listing(
            niche_id=niche.id, title="New Listing",
            status="live", uploaded_at=recent,
            views=5, favorites=0,
        )
        session.add(listing)

    result = run()
    assert "0 listings flagged" in result
