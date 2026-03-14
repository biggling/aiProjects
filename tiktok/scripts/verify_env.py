"""Verify all API keys and environment variables are configured and working."""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dotenv import load_dotenv
import os

load_dotenv()

REQUIRED_VARS = [
    "OPENAI_API_KEY",
    "ELEVENLABS_API_KEY",
    "ELEVENLABS_VOICE_ID",
    "TIKTOK_ACCESS_TOKEN",
    "TIKTOK_OPEN_ID",
    "DATABASE_URL",
    "API_KEY",
]

OPTIONAL_VARS = [
    "KLING_API_KEY",
    "RUNWAY_API_KEY",
    "INSTAGRAM_ACCESS_TOKEN",
    "YOUTUBE_CLIENT_SECRET",
    "REDIS_URL",
]


def check_env_vars():
    """Check that all required environment variables are set."""
    missing = []
    for var in REQUIRED_VARS:
        if not os.getenv(var):
            missing.append(var)

    optional_missing = []
    for var in OPTIONAL_VARS:
        if not os.getenv(var):
            optional_missing.append(var)

    return missing, optional_missing


def check_openai():
    """Verify OpenAI API key works."""
    from openai import OpenAI

    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": "Say OK"}],
        max_tokens=5,
    )
    assert response.choices[0].message.content is not None
    return True


def check_elevenlabs():
    """Verify ElevenLabs API key works."""
    import httpx

    api_key = os.getenv("ELEVENLABS_API_KEY")
    response = httpx.get(
        "https://api.elevenlabs.io/v1/voices",
        headers={"xi-api-key": api_key},
        timeout=30,
    )
    response.raise_for_status()
    return True


def check_database():
    """Verify database connection."""
    from sqlalchemy import create_engine, text

    db_url = os.getenv("DATABASE_URL", "sqlite:///data/db/app.db")
    engine = create_engine(db_url)
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    return True


def main():
    from loguru import logger

    logger.remove()
    logger.add(sys.stderr, level="INFO")

    results = {}
    all_ok = True

    # Check env vars
    missing, optional_missing = check_env_vars()
    if missing:
        logger.error(f"Missing required env vars: {missing}")
        all_ok = False
    else:
        logger.info("All required env vars set")
        results["env_vars"] = "OK"

    if optional_missing:
        logger.warning(f"Missing optional env vars: {optional_missing}")

    # Check APIs
    checks = {
        "openai": check_openai,
        "elevenlabs": check_elevenlabs,
        "database": check_database,
    }

    for name, check_fn in checks.items():
        try:
            check_fn()
            logger.info(f"{name}: OK")
            results[name] = "OK"
        except Exception as e:
            logger.error(f"{name}: FAILED - {e}")
            results[name] = f"FAILED: {e}"
            all_ok = False

    if all_ok:
        logger.info("All APIs OK")
        return 0
    else:
        logger.error("Some checks failed. Fix errors above before proceeding.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
