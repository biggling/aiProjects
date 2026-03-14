"""Metrics and weekly report endpoints."""

import asyncio

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from api.deps import get_db, verify_api_key
from modules.07_analytics.models import VideoMetric
from modules.07_analytics.report import generate_weekly_report

router = APIRouter(prefix="/api/analytics", tags=["analytics"], dependencies=[Depends(verify_api_key)])


class MetricResponse(BaseModel):
    id: int
    published_video_id: int
    views: int
    watch_time_avg: float
    likes: int
    shares: int
    comments: int
    ctr: float
    gmv: float
    winner: bool

    model_config = {"from_attributes": True}


class WeeklyReportResponse(BaseModel):
    week: str
    period: str
    total_views: int
    total_gmv: float
    total_likes: int
    total_shares: int
    avg_ctr: float
    videos_published: int
    top_3_videos: list[dict]


@router.get("/weekly", response_model=WeeklyReportResponse)
async def get_weekly_report(week: str = "current"):
    """Get weekly performance summary."""
    report = await asyncio.to_thread(generate_weekly_report, week)
    return report


@router.get("/video/{video_id}", response_model=list[MetricResponse])
async def get_video_metrics(video_id: int, db: Session = Depends(get_db)):
    """Get metrics history for a specific video."""
    metrics = await asyncio.to_thread(
        lambda: db.query(VideoMetric)
        .filter(VideoMetric.published_video_id == video_id)
        .order_by(VideoMetric.pulled_at.desc())
        .all()
    )
    if not metrics:
        raise HTTPException(status_code=404, detail="No metrics found for this video")
    return metrics
