"""FastAPI REST API for autoGenVideo."""
from fastapi import FastAPI, HTTPException, Depends, Header
from pydantic import BaseModel
from datetime import datetime
from database.models import SessionLocal, Topic, Script, Video, Publication, Analytics
from config import API_SECRET_KEY, get_logger

logger = get_logger("api")
app = FastAPI(title="autoGenVideo API", version="1.0.0")


def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_SECRET_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key


class GenerateRequest(BaseModel):
    topic: str
    platform: str = "tiktok"
    duration: int = 30
    language: str = "en"


@app.get("/api/v1/health")
def health():
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}


@app.post("/api/v1/video/generate")
def generate_video(req: GenerateRequest, _key=Depends(verify_api_key)):
    """Submit a topic to trigger the full pipeline."""
    session = SessionLocal()
    try:
        topic = Topic(
            topic=req.topic,
            platform=req.platform,
            trend_score=80.0,
            source="api",
            language=req.language,
            status="pending",
        )
        session.add(topic)
        session.commit()
        session.refresh(topic)
        return {"topic_id": topic.id, "status": "queued", "message": "Pipeline triggered."}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()


@app.get("/api/v1/video/{video_id}/status")
def video_status(video_id: int, _key=Depends(verify_api_key)):
    session = SessionLocal()
    try:
        video = session.query(Video).get(video_id)
        if not video:
            raise HTTPException(status_code=404, detail="Video not found")
        return {"video_id": video.id, "status": video.status, "created_at": video.created_at}
    finally:
        session.close()


@app.get("/api/v1/analytics/summary")
def analytics_summary(_key=Depends(verify_api_key)):
    session = SessionLocal()
    try:
        pubs = session.query(Publication).filter_by(status="posted").count()
        all_analytics = session.query(Analytics).all()
        total_views = sum(a.views for a in all_analytics)
        total_likes = sum(a.likes for a in all_analytics)
        total_videos = session.query(Video).count()
        return {
            "total_videos": total_videos,
            "publications": pubs,
            "total_views": total_views,
            "total_likes": total_likes,
        }
    finally:
        session.close()


@app.get("/api/v1/topics/trending")
def trending_topics(_key=Depends(verify_api_key)):
    session = SessionLocal()
    try:
        topics = session.query(Topic).filter_by(status="pending").order_by(
            Topic.trend_score.desc()
        ).limit(10).all()
        return [{"id": t.id, "topic": t.topic, "trend_score": t.trend_score, "source": t.source} for t in topics]
    finally:
        session.close()


@app.get("/api/v1/jobs/status")
def jobs_status(_key=Depends(verify_api_key)):
    """Simple scheduler health check."""
    session = SessionLocal()
    try:
        return {
            "pending_topics": session.query(Topic).filter_by(status="pending").count(),
            "pending_scripts": session.query(Script).filter_by(status="pending").count(),
            "ready_videos": session.query(Video).filter_by(status="ready").count(),
            "published_videos": session.query(Video).filter_by(status="published").count(),
        }
    finally:
        session.close()
