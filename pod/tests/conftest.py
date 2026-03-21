"""Shared test fixtures for POD project."""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from tools.shared.models import Base


@pytest.fixture(autouse=True)
def setup_db():
    """Create fresh in-memory DB for each test."""
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)
    _Session = sessionmaker(bind=engine)

    # Monkey-patch get_session for tests
    import tools.shared.db as db_module
    original_engine = db_module.engine
    original_session = db_module.SessionLocal

    db_module.engine = engine
    db_module.SessionLocal = _Session

    yield engine, _Session

    db_module.engine = original_engine
    db_module.SessionLocal = original_session
    Base.metadata.drop_all(engine)
