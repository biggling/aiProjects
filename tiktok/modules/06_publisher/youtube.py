"""YouTube Data API v3 client for uploading Shorts."""

import json
import os
from pathlib import Path

import httpx
from loguru import logger


def upload_short(
    file_path: Path,
    title: str,
    description: str,
    tags: list[str] | None = None,
) -> str:
    """Upload video as YouTube Short. Returns video_id."""
    # Note: In production, use google-auth + google-api-python-client
    # This is a simplified implementation using direct HTTP
    client_secret = os.getenv("YOUTUBE_CLIENT_SECRET", "")

    # YouTube resumable upload endpoint
    upload_url = "https://www.googleapis.com/upload/youtube/v3/videos"

    metadata = {
        "snippet": {
            "title": title[:100],
            "description": description[:5000],
            "tags": tags or [],
            "categoryId": "22",  # People & Blogs
        },
        "status": {
            "privacyStatus": "public",
            "selfDeclaredMadeForKids": False,
        },
    }

    # Step 1: Initialize resumable upload
    with httpx.Client(timeout=60) as client:
        init_resp = client.post(
            upload_url,
            params={
                "uploadType": "resumable",
                "part": "snippet,status",
            },
            headers={
                "Authorization": f"Bearer {client_secret}",
                "Content-Type": "application/json",
            },
            content=json.dumps(metadata),
        )
        init_resp.raise_for_status()
        upload_location = init_resp.headers["location"]

    # Step 2: Upload video content
    video_data = file_path.read_bytes()
    with httpx.Client(timeout=300) as client:
        upload_resp = client.put(
            upload_location,
            content=video_data,
            headers={
                "Content-Type": "video/mp4",
                "Content-Length": str(len(video_data)),
            },
        )
        upload_resp.raise_for_status()
        video_id = upload_resp.json()["id"]

    logger.info(f"YouTube Short uploaded: video_id={video_id}")
    return video_id
