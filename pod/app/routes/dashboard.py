from datetime import datetime, timezone, timedelta

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlalchemy import select, func

from app.deps import templates, verify_credentials
from tools.shared.db import get_session
from tools.shared.models import TaskLog, Listing, Design

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
def overview(request: Request, user: str = Depends(verify_credentials)):
    cutoff = datetime.now(timezone.utc) - timedelta(hours=24)

    with get_session() as session:
        tasks_today = session.execute(
            select(func.count(TaskLog.id)).where(TaskLog.started_at >= cutoff)
        ).scalar() or 0

        errors_today = session.execute(
            select(func.count(TaskLog.id)).where(
                TaskLog.started_at >= cutoff,
                TaskLog.status == "failed",
            )
        ).scalar() or 0

        designs_pending = session.execute(
            select(func.count(Design.id)).where(Design.status == "approved")
        ).scalar() or 0

        listings_today = session.execute(
            select(func.count(Listing.id)).where(Listing.uploaded_at >= cutoff)
        ).scalar() or 0

        total_revenue = session.execute(
            select(func.sum(Listing.revenue))
        ).scalar() or 0

        total_live = session.execute(
            select(func.count(Listing.id)).where(Listing.status == "live")
        ).scalar() or 0

    return templates.TemplateResponse("overview.html", {
        "request": request,
        "tasks_today": tasks_today,
        "errors_today": errors_today,
        "designs_pending": designs_pending,
        "listings_today": listings_today,
        "total_revenue": f"{total_revenue:.2f}",
        "total_live": total_live,
    })
