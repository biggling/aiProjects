"""Kling AI API client for video generation."""

import os
import time
from pathlib import Path

import httpx
from loguru import logger

CLIPS_DIR = Path("data/assets/clips")
CLIPS_DIR.mkdir(parents=True, exist_ok=True)


def generate(prompt: str, duration: int = 5, style: str = "realistic") -> Path:
    """Submit a video generation job to Kling AI, poll until complete, download result."""
    api_key = os.getenv("KLING_API_KEY", "")
    base_url = "https://api.klingai.com/v1"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    # Submit generation job
    payload = {
        "prompt": prompt,
        "duration": duration,
        "aspect_ratio": "9:16",
        "style": style,
    }

    with httpx.Client(timeout=60) as client:
        response = client.post(f"{base_url}/videos/generate", json=payload, headers=headers)
        response.raise_for_status()
        job_id = response.json()["data"]["task_id"]
        logger.info(f"Kling job submitted: {job_id}")

    # Poll for completion
    output_path = CLIPS_DIR / f"kling_{job_id}.mp4"
    max_polls = 120  # 10 minutes at 5s intervals
    for i in range(max_polls):
        time.sleep(5)
        with httpx.Client(timeout=30) as client:
            status_resp = client.get(f"{base_url}/videos/{job_id}", headers=headers)
            status_resp.raise_for_status()
            status_data = status_resp.json()["data"]

            if status_data["status"] == "completed":
                video_url = status_data["video_url"]
                _download_video(video_url, output_path)
                logger.info(f"Kling video downloaded: {output_path}")
                return output_path
            elif status_data["status"] == "failed":
                raise RuntimeError(f"Kling generation failed: {status_data.get('error', 'Unknown')}")

        if i % 12 == 0:
            logger.info(f"Kling job {job_id}: still processing ({i * 5}s elapsed)")

    raise TimeoutError(f"Kling job {job_id} timed out after {max_polls * 5}s")


def _download_video(url: str, output_path: Path) -> None:
    """Download video from URL."""
    with httpx.Client(timeout=120) as client:
        response = client.get(url)
        response.raise_for_status()
        output_path.write_bytes(response.content)
