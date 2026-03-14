"""TikTok Content Posting API v2 client."""

import os
from datetime import datetime
from pathlib import Path

import httpx
from loguru import logger


def upload_video(file_path: Path, caption: str, cover_path: Path | None = None) -> str:
    """Upload video to TikTok using Content Posting API v2. Returns post_id."""
    access_token = os.getenv("TIKTOK_ACCESS_TOKEN", "")
    open_id = os.getenv("TIKTOK_OPEN_ID", "")
    base_url = "https://open.tiktokapis.com/v2"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    file_size = file_path.stat().st_size

    # Step 1: Initialize upload
    init_payload = {
        "post_info": {
            "title": caption[:150],
            "privacy_level": "PUBLIC_TO_EVERYONE",
            "disable_duet": False,
            "disable_comment": False,
            "disable_stitch": False,
        },
        "source_info": {
            "source": "FILE_UPLOAD",
            "video_size": file_size,
        },
    }

    with httpx.Client(timeout=60) as client:
        init_resp = client.post(
            f"{base_url}/post/publish/inbox/video/init/",
            json=init_payload,
            headers=headers,
        )
        init_resp.raise_for_status()
        init_data = init_resp.json()["data"]
        upload_url = init_data["upload_url"]
        publish_id = init_data["publish_id"]

    # Step 2: Upload video file
    chunk_size = 10 * 1024 * 1024  # 10MB chunks
    video_data = file_path.read_bytes()

    if file_size <= chunk_size:
        # Single upload
        with httpx.Client(timeout=120) as client:
            upload_resp = client.put(
                upload_url,
                content=video_data,
                headers={
                    "Content-Type": "video/mp4",
                    "Content-Range": f"bytes 0-{file_size - 1}/{file_size}",
                },
            )
            upload_resp.raise_for_status()
    else:
        # Chunked upload
        offset = 0
        with httpx.Client(timeout=120) as client:
            while offset < file_size:
                end = min(offset + chunk_size, file_size)
                chunk = video_data[offset:end]
                upload_resp = client.put(
                    upload_url,
                    content=chunk,
                    headers={
                        "Content-Type": "video/mp4",
                        "Content-Range": f"bytes {offset}-{end - 1}/{file_size}",
                    },
                )
                upload_resp.raise_for_status()
                offset = end

    logger.info(f"Video uploaded to TikTok: publish_id={publish_id}")
    return publish_id
