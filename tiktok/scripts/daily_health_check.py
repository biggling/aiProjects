"""Daily health check — verifies all API connections and system status."""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dotenv import load_dotenv
from loguru import logger

load_dotenv()

logger.remove()
logger.add(sys.stderr, level="INFO")


def check_disk_space():
    """Check data directory size."""
    data_dir = Path("data")
    if not data_dir.exists():
        return True
    total_size = sum(f.stat().st_size for f in data_dir.rglob("*") if f.is_file())
    size_gb = total_size / (1024 ** 3)
    logger.info(f"Data directory: {size_gb:.2f} GB")
    if size_gb > 10:
        logger.warning(f"Data directory exceeds 10 GB!")
        return False
    return True


def check_database():
    """Verify database is accessible."""
    try:
        from sqlalchemy import create_engine, text
        db_url = os.getenv("DATABASE_URL", "sqlite:///data/db/app.db")
        engine = create_engine(db_url)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("Database: OK")
        return True
    except Exception as e:
        logger.error(f"Database: FAILED - {e}")
        return False


def check_ffmpeg():
    """Verify FFmpeg is installed."""
    import subprocess
    try:
        result = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            logger.info("FFmpeg: OK")
            return True
    except Exception:
        pass
    logger.error("FFmpeg: NOT FOUND")
    return False


def main():
    checks = {
        "disk_space": check_disk_space,
        "database": check_database,
        "ffmpeg": check_ffmpeg,
    }

    all_ok = True
    for name, check_fn in checks.items():
        if not check_fn():
            all_ok = False

    if all_ok:
        logger.info("Health check: ALL OK")
        return 0
    else:
        logger.error("Health check: SOME CHECKS FAILED")
        return 1


if __name__ == "__main__":
    sys.exit(main())
