"""Tests for database models using in-memory SQLite."""
import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import Base, Niche, Design, Listing, Order


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    s = Session()
    yield s
    s.close()


def test_create_niche(session):
    niche = Niche(niche="funny dog mom", search_volume=1000, trend_score=0.8)
    session.add(niche)
    session.commit()
    result = session.query(Niche).filter_by(niche="funny dog mom").first()
    assert result is not None
    assert result.trend_score == 0.8


def test_niche_design_relationship(session):
    niche = Niche(niche="hiking gear")
    session.add(niche)
    session.flush()

    design = Design(niche_id=niche.id, style="typography", product_type="tshirt", status="ready")
    session.add(design)
    session.commit()

    assert len(niche.designs) == 1
    assert niche.designs[0].style == "typography"


def test_listing_order_relationship(session):
    niche = Niche(niche="test niche")
    session.add(niche)
    session.flush()

    design = Design(niche_id=niche.id, style="illustrated", product_type="mug")
    session.add(design)
    session.flush()

    listing = Listing(design_id=design.id, platform="etsy", price=29.99, status="active")
    session.add(listing)
    session.flush()

    order = Order(listing_id=listing.id, platform="etsy", revenue=29.99, profit=5.00)
    session.add(order)
    session.commit()

    assert listing.orders[0].revenue == 29.99


def test_default_status_values(session):
    niche = Niche(niche="cat lover")
    session.add(niche)
    session.commit()
    assert niche.status == "active"
