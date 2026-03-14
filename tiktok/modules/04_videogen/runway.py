"""Runway Gen-4 API client for video generation (fallback)."""

import os
import time
from pathlib import Path

import httpx
from loguru import logger

CLIPS_DIR = Path("data/assets/clips")
CLIPS_DIR.mkdir(parents=True, exist_ok=True)


def generate(prompt: str, duration: int = 5, style: str = "realistic") -> Path:
    """Submit a video generation job to Runway Gen-4, poll until complete, download result."""
    api_key = os.getenv("RUNWAY_API_KEY", "")
    base_url = "https://api.dev.runwayml.com/v1"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "promptText": prompt,
        "model": "gen4",
        "duration": duration,
        "ratio": "portrait",
    }

    with httpx.Client(timeout=60) as client:
        response = client.post(f"{base_url}/image_to_video", json=payload, headers=headers)
        response.raise_for_status()
        task_id = response.json()["id"]
        logger.info(f"Runway job submitted: {task_id}")

    # Poll for completion
    output_path = CLIPS_DIR / f"runway_{task_id}.mp4"
    max_polls = 120
    for i in range(max_polls):
        time.sleep(5)
        with httpx.Client(timeout=30) as client:
            status_resp = client.get(f"{base_url}/tasks/{task_id}", headers=headers)
            status_resp.raise_for_status()
            status_data = status_resp.json()

            if status_data["status"] == "SUCCEEDED":
                video_url = status_data["output"][0]
                _download_video(video_url, output_path)
                logger.info(f"Runway video downloaded: {output_path}")
                return output_path
            elif status_data["status"] == "FAILED":
                raise RuntimeError(f"Runway generation failed: {status_data.get('failure', 'Unknown')}")

        if i % 12 == 0:
            logger.info(f"Runway job {task_id}: still processing ({i * 5}s elapsed)")

    raise TimeoutError(f"Runway job {task_id} timed out after {max_polls * 5}s")


def _download_video(url: str, output_path: Path) -> None:
    """Download video from URL."""
    with httpx.Client(timeout=120) as client:
        response = client.get(url)
        response.raise_for_status()
        output_path.write_bytes(response.content)
