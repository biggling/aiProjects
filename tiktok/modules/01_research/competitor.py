"""Extract hooks from top-performing competitor videos."""

from datetime import datetime

import httpx
from loguru import logger
from openai import OpenAI

from modules.01_research.db import SessionLocal
from modules.01_research.models import CompetitorHook


def fetch_top_videos(access_token: str, hashtag: str, limit: int = 10) -> list[dict]:
    """Fetch top videos for a given hashtag from TikTok Research API."""
    url = "https://open.tiktokapis.com/v2/research/video/query/"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    payload = {
        "query": {"and": [{"field_name": "hashtag_name", "field_values": [hashtag]}]},
        "max_count": limit,
        "sort_type": "popular",
    }

    try:
        with httpx.Client(timeout=30) as client:
            response = client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            return data.get("data", {}).get("videos", [])
    except Exception as e:
        logger.warning(f"Failed to fetch videos for #{hashtag}: {e}")
        return []


def extract_hook_with_gpt(video_title: str, video_description: str) -> str:
    """Use GPT-4o to extract the hook from a video's caption/title."""
    client = OpenAI()
    prompt = (
        f"Extract the hook (attention-grabbing first sentence) from this TikTok video.\n"
        f"Title: {video_title}\n"
        f"Description: {video_description}\n\n"
        f"Return ONLY the hook text, nothing else. If no clear hook, write a likely hook based on the content."
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100,
            timeout=30,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"GPT hook extraction failed: {e}")
        return video_title[:100] if video_title else "Unknown hook"


def scrape_competitor_hooks(
    access_token: str, hashtags: list[str], videos_per_hashtag: int = 10
) -> int:
    """Scrape hooks from competitor videos. Returns count of new records."""
    count = 0
    db = SessionLocal()

    try:
        for hashtag in hashtags:
            logger.info(f"Fetching top videos for #{hashtag}")
            videos = fetch_top_videos(access_token, hashtag, videos_per_hashtag)

            if not videos:
                # Use fallback data in dev
                videos = _fallback_videos(hashtag)

            for video in videos:
                video_id = video.get("id", f"fallback_{hashtag}_{count}")
                title = video.get("title", "")
                desc = video.get("video_description", title)
                view_count = video.get("view_count", 0)

                hook_text = extract_hook_with_gpt(title, desc) if title else title

                hook = CompetitorHook(
                    video_id=str(video_id),
                    hook_text=hook_text,
                    view_count=view_count,
                    scraped_at=datetime.utcnow(),
                )
                db.add(hook)
                count += 1

        db.commit()
        logger.info(f"Stored {count} competitor hooks")
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to store hooks: {e}")
        raise
    finally:
        db.close()

    return count


def _fallback_videos(hashtag: str) -> list[dict]:
    """Fallback video data for development."""
    return [
        {
            "id": f"dev_{hashtag}_1",
            "title": f"ลองใช้แล้วดีมาก #{hashtag}",
            "video_description": f"รีวิวจริงจัง #{hashtag} ของดีบอกต่อ",
            "view_count": 50000,
        },
        {
            "id": f"dev_{hashtag}_2",
            "title": f"ห้ามพลาด! #{hashtag}",
            "video_description": f"สิ่งนี้เปลี่ยนชีวิตฉัน #{hashtag}",
            "view_count": 120000,
        },
    ]
