"""Tests for database models using in-memory SQLite."""
import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import Base, Niche, Trend, Script, Video, Post, Analytics, Affiliate


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    s = Session()
    yield s
    s.close()


def test_create_niche(session):
    niche = Niche(
        niche="beauty",
        product_name="Face Serum",
        product_url="https://example.com/p1",
        affiliate_link="https://example.com/p1?aff=1",
        affiliate_network="amazon",
        commission_pct=4.0,
        trend_score=75.0,
    )
    session.add(niche)
    session.commit()
    result = session.query(Niche).filter_by(product_url="https://example.com/p1").first()
    assert result is not None
    assert result.trend_score == 75.0


def test_niche_default_status(session):
    niche = Niche(niche="fitness", product_name="Resistance Bands")
    session.add(niche)
    session.commit()
    assert niche.status == "active"


def test_niche_script_relationship(session):
    niche = Niche(niche="gadgets", product_name="Smart Plug")
    session.add(niche)
    session.flush()

    script = Script(
        product_id=niche.id,
        hook="You're wasting electricity every day",
        voiceover_text="This $10 smart plug saves you money automatically.",
        status="pending",
        confidence_score=0.9,
    )
    session.add(script)
    session.commit()

    assert len(niche.scripts) == 1
    assert niche.scripts[0].hook == "You're wasting electricity every day"


def test_script_video_relationship(session):
    niche = Niche(niche="pets", product_name="Dog Toy")
    session.add(niche)
    session.flush()

    script = Script(product_id=niche.id, hook="Your dog is bored", status="approved")
    session.add(script)
    session.flush()

    video = Video(script_id=script.id, file_path="videos/v1.mp4", duration=28.5, status="ready")
    session.add(video)
    session.commit()

    assert script.video.file_path == "videos/v1.mp4"


def test_video_post_relationship(session):
    niche = Niche(niche="food", product_name="Air Fryer")
    session.add(niche)
    session.flush()

    script = Script(product_id=niche.id, hook="Stop deep frying!", status="approved")
    session.add(script)
    session.flush()

    video = Video(script_id=script.id, file_path="videos/v2.mp4", status="ready")
    session.add(video)
    session.flush()

    post = Post(
        video_id=video.id,
        platform="tiktok",
        tiktok_video_id="tt_123456",
        status="posted",
    )
    session.add(post)
    session.commit()

    assert len(video.posts) == 1
    assert video.posts[0].platform == "tiktok"


def test_post_analytics_relationship(session):
    niche = Niche(niche="tech", product_name="USB Hub")
    session.add(niche)
    session.flush()

    script = Script(product_id=niche.id, hook="Your laptop is missing this", status="approved")
    session.add(script)
    session.flush()

    video = Video(script_id=script.id, file_path="videos/v3.mp4", status="ready")
    session.add(video)
    session.flush()

    post = Post(video_id=video.id, platform="tiktok", status="posted")
    session.add(post)
    session.flush()

    analytics = Analytics(
        post_id=post.id,
        views_24h=5000,
        likes=320,
        comments=45,
        follows_gained=80,
        engagement_rate=7.3,
    )
    session.add(analytics)
    session.commit()

    assert post.analytics[0].views_24h == 5000
    assert post.analytics[0].engagement_rate == 7.3


def test_affiliate_default_values(session):
    affiliate = Affiliate(
        product_name="Test Product",
        affiliate_network="amazon",
        period="2026-03-06",
    )
    session.add(affiliate)
    session.commit()
    assert affiliate.clicks == 0
    assert affiliate.conversions == 0
    assert affiliate.commission == 0.0


def test_trend_creation(session):
    trend = Trend(
        niche="beauty",
        hook_pattern="bold_claim",
        hook_text="This product cleared my skin in 3 days",
        hashtags="#skincare,#beauty,#fyp",
        views=120000,
    )
    session.add(trend)
    session.commit()
    result = session.query(Trend).filter_by(hook_pattern="bold_claim").first()
    assert result is not None
    assert result.views == 120000
