"""Video queue and approval endpoints."""

import asyncio
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from api.deps import get_db, verify_api_key
from api.ws import manager
from modules.05_editor.models import EditedVideo

router = APIRouter(prefix="/api/videos", tags=["videos"], dependencies=[Depends(verify_api_key)])


class VideoResponse(BaseModel):
    id: int
    script_id: int
    file_path: str
    thumbnail_path: str | None
    duration_sec: float
    status: str

    model_config = {"from_attributes": True}


class RejectRequest(BaseModel):
    reason: str


@router.get("/pending", response_model=list[VideoResponse])
async def list_pending(db: Session = Depends(get_db)):
    """List videos awaiting QC review."""
    videos = await asyncio.to_thread(
        lambda: db.query(EditedVideo)
        .filter(EditedVideo.status == "pending_review")
        .order_by(EditedVideo.created_at.desc())
        .all()
    )
    return videos


@router.get("/{video_id}/stream")
async def stream_video(video_id: int, db: Session = Depends(get_db)):
    """Stream MP4 for in-browser playback."""
    video = await asyncio.to_thread(
        lambda: db.query(EditedVideo).filter(EditedVideo.id == video_id).first()
    )
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")

    file_path = Path(video.file_path)
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Video file not found")

    def iterfile():
        with open(file_path, "rb") as f:
            while chunk := f.read(1024 * 1024):
                yield chunk

    return StreamingResponse(
        iterfile(),
        media_type="video/mp4",
        headers={"Accept-Ranges": "bytes", "Content-Length": str(file_path.stat().st_size)},
    )


@router.get("/{video_id}/thumbnail")
async def get_thumbnail(video_id: int, db: Session = Depends(get_db)):
    """Serve thumbnail JPEG."""
    video = await asyncio.to_thread(
        lambda: db.query(EditedVideo).filter(EditedVideo.id == video_id).first()
    )
    if not video or not video.thumbnail_path:
        raise HTTPException(status_code=404, detail="Thumbnail not found")

    thumb_path = Path(video.thumbnail_path)
    if not thumb_path.exists():
        raise HTTPException(status_code=404, detail="Thumbnail file not found")

    return FileResponse(str(thumb_path), media_type="image/jpeg")


@router.post("/{video_id}/approve", response_model=VideoResponse)
async def approve_video(video_id: int, db: Session = Depends(get_db)):
    """Approve video for publishing."""
    video = await asyncio.to_thread(
        lambda: db.query(EditedVideo).filter(EditedVideo.id == video_id).first()
    )
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")

    video.status = "approved"
    await asyncio.to_thread(db.commit)
    await manager.broadcast("video_approved", {"video_id": video_id})
    return video


@router.post("/{video_id}/reject", response_model=VideoResponse)
async def reject_video(video_id: int, body: RejectRequest, db: Session = Depends(get_db)):
    """Reject video with reason."""
    video = await asyncio.to_thread(
        lambda: db.query(EditedVideo).filter(EditedVideo.id == video_id).first()
    )
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")

    video.status = "rejected"
    await asyncio.to_thread(db.commit)
    await manager.broadcast("video_rejected", {"video_id": video_id, "reason": body.reason})
    return video
