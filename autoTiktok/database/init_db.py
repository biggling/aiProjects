"""Initialize autoTiktok database schema."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from database.models import Base, engine
from config import get_logger

logger = get_logger("init_db")


def init_db():
    logger.info("Creating database tables...")
    Base.metadata.create_all(engine)
    logger.info("Database initialized.")


if __name__ == "__main__":
    init_db()
