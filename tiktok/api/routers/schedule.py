"""Job status and manual trigger endpoints."""

import asyncio
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from api.deps import verify_api_key
from api.ws import manager
from scheduler import jobs

router = APIRouter(prefix="/api/schedule", tags=["schedule"], dependencies=[Depends(verify_api_key)])

JOB_REGISTRY = {
    "run_research": jobs.run_research,
    "run_strategy": jobs.run_strategy,
    "run_scriptgen": jobs.run_scriptgen,
    "run_voiceover": jobs.run_voiceover,
    "run_videogen": jobs.run_videogen,
    "run_editor": jobs.run_editor,
    "publish_slot_1": jobs.publish_slot,
    "publish_slot_2": jobs.publish_slot,
    "run_crosspost": jobs.run_crosspost,
    "run_analytics": jobs.run_analytics,
    "run_weekly_score": jobs.run_weekly_score,
}

SCHEDULE = [
    {"name": "run_research", "module": "01_research.scraper", "time": "06:00"},
    {"name": "run_strategy", "module": "01_research.strategy", "time": "07:00"},
    {"name": "run_scriptgen", "module": "02_scriptgen.generator", "time": "07:30"},
    {"name": "run_voiceover", "module": "03_voiceover.renderer", "time": "08:00"},
    {"name": "run_videogen", "module": "04_videogen.orchestrator", "time": "09:00"},
    {"name": "run_editor", "module": "05_editor.editor", "time": "10:30"},
    {"name": "publish_slot_1", "module": "06_publisher.tiktok", "time": "12:00"},
    {"name": "run_crosspost", "module": "06_publisher.crosspost", "time": "15:30"},
    {"name": "publish_slot_2", "module": "06_publisher.tiktok", "time": "18:00"},
    {"name": "run_analytics", "module": "07_analytics.puller", "time": "21:00"},
    {"name": "run_weekly_score", "module": "07_analytics.scorer", "time": "Fri 21:00"},
]

# In-memory job status tracking
job_statuses: dict[str, dict] = {}


class JobStatus(BaseModel):
    name: str
    module: str
    scheduled_time: str
    status: str = "pending"
    last_run: str | None = None
    duration: float | None = None


class RunResponse(BaseModel):
    job_name: str
    status: str
    message: str


@router.get("/today", response_model=list[JobStatus])
async def get_today_schedule():
    """Get today's job statuses."""
    result = []
    for job in SCHEDULE:
        status_info = job_statuses.get(job["name"], {})
        result.append(JobStatus(
            name=job["name"],
            module=job["module"],
            scheduled_time=job["time"],
            status=status_info.get("status", "pending"),
            last_run=status_info.get("last_run"),
            duration=status_info.get("duration"),
        ))
    return result


@router.post("/run/{job_name}", response_model=RunResponse)
async def run_job(job_name: str):
    """Manually trigger a job."""
    if job_name not in JOB_REGISTRY:
        raise HTTPException(status_code=404, detail=f"Job '{job_name}' not found")

    job_fn = JOB_REGISTRY[job_name]
    start = datetime.utcnow()

    job_statuses[job_name] = {"status": "running", "last_run": start.isoformat()}
    await manager.broadcast("job_started", {"job_name": job_name})

    try:
        result = await asyncio.to_thread(job_fn)
        elapsed = (datetime.utcnow() - start).total_seconds()
        job_statuses[job_name] = {
            "status": "done",
            "last_run": start.isoformat(),
            "duration": elapsed,
        }
        await manager.broadcast("job_done", {"job_name": job_name, "duration": elapsed})
        return RunResponse(job_name=job_name, status="done", message=f"Completed in {elapsed:.1f}s")

    except Exception as e:
        elapsed = (datetime.utcnow() - start).total_seconds()
        job_statuses[job_name] = {
            "status": "failed",
            "last_run": start.isoformat(),
            "duration": elapsed,
        }
        await manager.broadcast("job_failed", {"job_name": job_name, "error": str(e)})
        return RunResponse(job_name=job_name, status="failed", message=str(e))
