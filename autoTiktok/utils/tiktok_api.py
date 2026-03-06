"""TikTok API client (Content Posting API v2 + Analytics API)."""
from pathlib import Path
import requests
from tenacity import retry, stop_after_attempt, wait_exponential
from config import TIKTOK_ACCESS_TOKEN, TIKTOK_CLIENT_KEY, get_logger

logger = get_logger("tiktok_api")
BASE = "https://open.tiktokapis.com/v2"


class TikTokClient:
    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {TIKTOK_ACCESS_TOKEN}",
            "Content-Type": "application/json",
        }

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=5, max=30))
    def upload_video(self, video_path: Path, caption: str, hashtags: list[str],
                     cover_timestamp_ms: int = 500) -> dict:
        """Upload video via TikTok Content Posting API v2."""
        if not TIKTOK_ACCESS_TOKEN:
            logger.warning("TikTok token not configured, skipping upload.")
            return {}

        caption_full = f"{caption} {' '.join(hashtags)}"[:2200]
        file_size = video_path.stat().st_size

        # Init upload
        r = requests.post(
            f"{BASE}/post/publish/video/init/",
            headers=self.headers,
            json={
                "post_info": {
                    "title": caption_full[:150],
                    "privacy_level": "PUBLIC_TO_EVERYONE",
                    "disable_duet": False,
                    "disable_comment": False,
                    "disable_stitch": False,
                    "video_cover_timestamp_ms": cover_timestamp_ms,
                },
                "source_info": {
                    "source": "FILE_UPLOAD",
                    "video_size": file_size,
                    "chunk_size": file_size,
                    "total_chunk_count": 1,
                },
            },
            timeout=30,
        )
        r.raise_for_status()
        data = r.json().get("data", {})
        upload_url = data.get("upload_url")
        publish_id = data.get("publish_id")

        # Upload file
        with open(video_path, "rb") as f:
            up = requests.put(
                upload_url, data=f,
                headers={"Content-Type": "video/mp4", "Content-Range": f"bytes 0-{file_size-1}/{file_size}"},
                timeout=120,
            )
            up.raise_for_status()

        logger.info(f"TikTok video uploaded: publish_id={publish_id}")
        return {"publish_id": publish_id, "platform": "tiktok"}

    def get_video_stats(self, video_id: str) -> dict:
        """Get video analytics."""
        if not video_id:
            return {}
        try:
            r = requests.post(
                f"{BASE}/video/query/",
                headers=self.headers,
                json={
                    "filters": {"video_ids": [video_id]},
                    "fields": ["view_count", "like_count", "comment_count", "share_count"],
                },
                timeout=15,
            )
            if r.ok:
                videos = r.json().get("data", {}).get("videos", [])
                return videos[0] if videos else {}
        except Exception as e:
            logger.warning(f"TikTok stats failed: {e}")
        return {}

    def get_comments(self, video_id: str, cursor: int = 0) -> list[dict]:
        """Fetch recent comments on a video."""
        try:
            r = requests.post(
                f"{BASE}/video/comment/list/",
                headers=self.headers,
                json={
                    "video_id": video_id,
                    "cursor": cursor,
                    "count": 20,
                    "sort_field": "time",
                    "sort_order": "desc",
                },
                timeout=15,
            )
            if r.ok:
                return r.json().get("data", {}).get("comments", [])
        except Exception as e:
            logger.warning(f"TikTok comments fetch failed: {e}")
        return []

    def reply_to_comment(self, video_id: str, comment_id: str, reply_text: str) -> bool:
        """Post reply to a comment."""
        try:
            r = requests.post(
                f"{BASE}/video/comment/reply/",
                headers=self.headers,
                json={"video_id": video_id, "comment_id": comment_id, "text": reply_text[:150]},
                timeout=10,
            )
            return r.ok
        except Exception as e:
            logger.error(f"Reply failed: {e}")
            return False
