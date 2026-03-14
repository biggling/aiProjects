"""Database session and migration helpers."""

from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///data/db/app.db")

# Ensure db directory exists for SQLite
if DATABASE_URL.startswith("sqlite"):
    db_path = DATABASE_URL.replace("sqlite:///", "")
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


class Base(DeclarativeBase):
    pass


def get_db():
    """Yield a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Create all tables."""
    from modules.01_research.models import Trend, Product, CompetitorHook  # noqa: F401
    from modules.02_scriptgen.models import Script  # noqa: F401
    from modules.03_voiceover.models import Voiceover  # noqa: F401
    from modules.04_videogen.models import VideoClip  # noqa: F401
    from modules.05_editor.models import EditedVideo  # noqa: F401
    from modules.06_publisher.models import PublishedVideo  # noqa: F401
    from modules.07_analytics.models import VideoMetric  # noqa: F401
    from modules.01_research.models import ContentBrief  # noqa: F401

    Base.metadata.create_all(bind=engine)
