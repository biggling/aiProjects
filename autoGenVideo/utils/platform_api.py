"""Platform API clients: TikTok, YouTube, Instagram, Pinterest."""
import os
import requests
from pathlib import Path
from tenacity import retry, stop_after_attempt, wait_exponential
from config import (
    TIKTOK_ACCESS_TOKEN, YOUTUBE_API_KEY, YOUTUBE_REFRESH_TOKEN,
    YOUTUBE_CLIENT_ID, YOUTUBE_CLIENT_SECRET,
    INSTAGRAM_ACCESS_TOKEN, INSTAGRAM_BUSINESS_ACCOUNT_ID,
    PINTEREST_ACCESS_TOKEN, get_logger
)

logger = get_logger("platform_api")


class TikTokClient:
    BASE = "https://open.tiktokapis.com/v2"

    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {TIKTOK_ACCESS_TOKEN}",
            "Content-Type": "application/json",
        }

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=2, max=15))
    def upload_video(self, video_path: Path, caption: str, hashtags: list[str]) -> dict:
        """Upload video via TikTok Content Posting API."""
        # Step 1: Init upload
        caption_full = caption + " " + " ".join(hashtags)
        r = requests.post(
            f"{self.BASE}/post/publish/video/init/",
            headers=self.headers,
            json={
                "post_info": {
                    "title": caption_full[:150],
                    "privacy_level": "PUBLIC_TO_EVERYONE",
                    "disable_duet": False,
                    "disable_comment": False,
                    "disable_stitch": False,
                    "video_cover_timestamp_ms": 500,
                },
                "source_info": {
                    "source": "FILE_UPLOAD",
                    "video_size": video_path.stat().st_size,
                    "chunk_size": video_path.stat().st_size,
                    "total_chunk_count": 1,
                },
            },
            timeout=30,
        )
        r.raise_for_status()
        data = r.json().get("data", {})
        upload_url = data.get("upload_url")
        publish_id = data.get("publish_id")

        # Step 2: Upload file
        with open(video_path, "rb") as f:
            requests.put(upload_url, data=f, headers={"Content-Type": "video/mp4"}, timeout=120)

        return {"publish_id": publish_id, "platform": "tiktok"}

    def get_video_stats(self, video_id: str) -> dict:
        r = requests.post(
            f"{self.BASE}/video/query/",
            headers=self.headers,
            json={"filters": {"video_ids": [video_id]}, "fields": ["view_count", "like_count", "comment_count", "share_count"]},
            timeout=15,
        )
        if r.status_code == 200:
            videos = r.json().get("data", {}).get("videos", [])
            return videos[0] if videos else {}
        return {}


class YouTubeClient:
    def __init__(self):
        from google.oauth2.credentials import Credentials
        from googleapiclient.discovery import build
        creds = Credentials(
            token=None,
            refresh_token=YOUTUBE_REFRESH_TOKEN,
            client_id=YOUTUBE_CLIENT_ID,
            client_secret=YOUTUBE_CLIENT_SECRET,
            token_uri="https://oauth2.googleapis.com/token",
        )
        self.service = build("youtube", "v3", credentials=creds)

    def upload_short(self, video_path: Path, title: str, description: str, tags: list[str]) -> dict:
        from googleapiclient.http import MediaFileUpload
        body = {
            "snippet": {
                "title": title[:100],
                "description": description[:5000],
                "tags": tags[:15],
                "categoryId": "22",  # People & Blogs
            },
            "status": {"privacyStatus": "public"},
        }
        media = MediaFileUpload(str(video_path), mimetype="video/mp4", resumable=True)
        request = self.service.videos().insert(part="snippet,status", body=body, media_body=media)
        response = request.execute()
        video_id = response.get("id")
        return {"video_id": video_id, "url": f"https://youtube.com/shorts/{video_id}", "platform": "youtube"}

    def get_video_stats(self, video_id: str) -> dict:
        r = self.service.videos().list(part="statistics", id=video_id).execute()
        items = r.get("items", [])
        return items[0].get("statistics", {}) if items else {}


class InstagramClient:
    BASE = "https://graph.facebook.com/v19.0"

    def __init__(self):
        self.token = INSTAGRAM_ACCESS_TOKEN
        self.account_id = INSTAGRAM_BUSINESS_ACCOUNT_ID

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=2, max=15))
    def upload_reel(self, video_url: str, caption: str) -> dict:
        """Upload reel via Instagram Graph API (requires public video URL)."""
        # Step 1: Create container
        r = requests.post(
            f"{self.BASE}/{self.account_id}/media",
            params={"access_token": self.token},
            json={"media_type": "REELS", "video_url": video_url, "caption": caption},
            timeout=30,
        )
        r.raise_for_status()
        container_id = r.json().get("id")

        # Step 2: Publish
        r2 = requests.post(
            f"{self.BASE}/{self.account_id}/media_publish",
            params={"access_token": self.token},
            json={"creation_id": container_id},
            timeout=30,
        )
        r2.raise_for_status()
        return {"media_id": r2.json().get("id"), "platform": "instagram"}


class PinterestClient:
    BASE = "https://api.pinterest.com/v5"

    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {PINTEREST_ACCESS_TOKEN}",
            "Content-Type": "application/json",
        }

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=2, max=10))
    def create_video_pin(self, board_id: str, video_url: str, title: str, description: str, link: str = "") -> dict:
        payload = {
            "board_id": board_id,
            "media_source": {"source_type": "video_url", "url": video_url},
            "title": title[:100],
            "description": description[:500],
        }
        if link:
            payload["link"] = link
        r = requests.post(f"{self.BASE}/pins", headers=self.headers, json=payload, timeout=15)
        r.raise_for_status()
        return r.json()

    def get_boards(self) -> list:
        r = requests.get(f"{self.BASE}/boards", headers=self.headers, timeout=10)
        return r.json().get("items", []) if r.ok else []
