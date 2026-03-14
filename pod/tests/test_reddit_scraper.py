import pytest
from unittest.mock import patch, MagicMock

from tools.shared.db import engine, get_session
from tools.shared.models import Base, Niche
from tools.trend.reddit_scraper import (
    fetch_rising_posts, extract_keywords, upsert_reddit_niches, run,
)


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


def _mock_reddit():
    reddit = MagicMock()
    post1 = MagicMock()
    post1.title = "Best selling cat mom shirts this month"
    post2 = MagicMock()
    post2.title = "Retro gaming designs are trending hard"
    post3 = MagicMock()
    post3.title = "How to price your POD products?"

    subreddit = MagicMock()
    subreddit.hot.return_value = [post1, post2, post3]
    reddit.subreddit.return_value = subreddit
    return reddit


def test_fetch_rising_posts():
    reddit = _mock_reddit()
    titles = fetch_rising_posts(reddit)
    # 3 posts × 3 subreddits
    assert len(titles) == 9
    assert "Best selling cat mom shirts this month" in titles


@patch("tools.trend.reddit_scraper.get_anthropic")
def test_extract_keywords(mock_get_anthropic):
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.content = [MagicMock(text='["cat mom", "retro gaming", "nurse life"]')]
    mock_client.messages.create.return_value = mock_response
    mock_get_anthropic.return_value = mock_client

    keywords = extract_keywords(["some post title"])

    assert len(keywords) == 3
    assert "cat mom" in keywords
    mock_client.messages.create.assert_called_once()


def test_upsert_reddit_niches_new():
    count = upsert_reddit_niches(["cat mom", "retro gaming"])
    assert count == 2

    with get_session() as session:
        niches = session.query(Niche).all()
        assert len(niches) == 2


def test_upsert_reddit_niches_boosts_velocity():
    # Insert initial
    with get_session() as session:
        session.add(Niche(keyword="cat mom", trend_score=60, velocity=0.5, status="active"))

    upsert_reddit_niches(["cat mom"])

    with get_session() as session:
        niche = session.query(Niche).filter_by(keyword="cat mom").one()
        assert niche.velocity == pytest.approx(0.8, abs=0.01)


@patch("tools.trend.reddit_scraper.get_reddit")
@patch("tools.trend.reddit_scraper.get_anthropic")
def test_run(mock_get_anthropic, mock_get_reddit):
    mock_get_reddit.return_value = _mock_reddit()

    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.content = [MagicMock(text='["cat mom", "retro gaming"]')]
    mock_client.messages.create.return_value = mock_response
    mock_get_anthropic.return_value = mock_client

    result = run()
    assert "niches from Reddit" in result

    with get_session() as session:
        assert session.query(Niche).count() == 2
