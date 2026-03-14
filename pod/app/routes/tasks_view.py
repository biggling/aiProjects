from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy import select, func

from app.deps import templates, verify_credentials
from tools.shared.db import get_session
from tools.shared.models import TaskLog

router = APIRouter()

TASK_NAMES = [
    "trend_scraper", "reddit_scraper", "etsy_scraper", "niche_scorer",
    "prompt_gen", "image_gen", "image_processor", "clip_filter", "mockup_gen",
    "copy_gen", "caption_gen",
    "printify_publish", "etsy_upload", "social_post", "price_check",
    "analytics_pull", "performance_flag", "weekly_report", "backup",
]


@router.get("/tasks", response_class=HTMLResponse)
def task_list(request: Request, user: str = Depends(verify_credentials)):
    tasks = []
    with get_session() as session:
        for name in TASK_NAMES:
            latest = session.execute(
                select(TaskLog)
                .where(TaskLog.task_name == name)
                .order_by(TaskLog.started_at.desc())
                .limit(1)
            ).scalar_one_or_none()

            tasks.append({
                "name": name,
                "last_run": latest.started_at.strftime("%Y-%m-%d %H:%M") if latest and latest.started_at else "never",
                "status": latest.status if latest else "—",
                "duration": _duration(latest) if latest else "—",
                "summary": (latest.result_summary or latest.error or "")[:100] if latest else "",
            })

    return templates.TemplateResponse("tasks.html", {
        "request": request,
        "tasks": tasks,
    })


@router.post("/tasks/{task_name}/run")
def run_task(task_name: str, user: str = Depends(verify_credentials)):
    from celery_app import app as celery_app
    celery_app.send_task(f"tasks.run_{task_name}")
    return RedirectResponse(url="/tasks", status_code=303)


def _duration(log: TaskLog) -> str:
    if log.started_at and log.finished_at:
        delta = log.finished_at - log.started_at
        return f"{delta.total_seconds():.1f}s"
    return "running"
