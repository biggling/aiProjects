"""Instagram Graph API client for posting Reels."""

import os
import time

import httpx
from loguru import logger
from pathlib import Path


def post_reel(file_path: Path, caption: str) -> str:
    """Post video as Instagram Reel. Returns media_id."""
    access_token = os.getenv("INSTAGRAM_ACCESS_TOKEN", "")
    base_url = "https://graph.facebook.com/v19.0"

    # Get Instagram Business Account ID
    with httpx.Client(timeout=30) as client:
        me_resp = client.get(
            f"{base_url}/me/accounts",
            params={"access_token": access_token},
        )
        me_resp.raise_for_status()
        pages = me_resp.json()["data"]
        if not pages:
            raise ValueError("No Instagram business accounts found")

        page_id = pages[0]["id"]
        page_token = pages[0]["access_token"]

        # Get Instagram account ID
        ig_resp = client.get(
            f"{base_url}/{page_id}",
            params={"fields": "instagram_business_account", "access_token": page_token},
        )
        ig_resp.raise_for_status()
        ig_account_id = ig_resp.json()["instagram_business_account"]["id"]

    # Step 1: Create media container
    # Note: Instagram requires a publicly accessible URL for the video
    # In production, upload to a temporary public storage first
    with httpx.Client(timeout=60) as client:
        container_resp = client.post(
            f"{base_url}/{ig_account_id}/media",
            params={
                "media_type": "REELS",
                "caption": caption,
                "access_token": page_token,
                # video_url would be set here in production
            },
        )
        container_resp.raise_for_status()
        container_id = container_resp.json()["id"]

    # Step 2: Poll until ready
    for _ in range(30):
        time.sleep(5)
        with httpx.Client(timeout=30) as client:
            status_resp = client.get(
                f"{base_url}/{container_id}",
                params={"fields": "status_code", "access_token": page_token},
            )
            status_resp.raise_for_status()
            status = status_resp.json().get("status_code")
            if status == "FINISHED":
                break

    # Step 3: Publish
    with httpx.Client(timeout=30) as client:
        publish_resp = client.post(
            f"{base_url}/{ig_account_id}/media_publish",
            params={"creation_id": container_id, "access_token": page_token},
        )
        publish_resp.raise_for_status()
        media_id = publish_resp.json()["id"]

    logger.info(f"Instagram Reel published: media_id={media_id}")
    return media_id
