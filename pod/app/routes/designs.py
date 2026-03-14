from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy import select

from app.deps import templates, verify_credentials
from tools.shared.db import get_session
from tools.shared.models import Design, Niche

router = APIRouter()


@router.get("/designs", response_class=HTMLResponse)
def design_list(request: Request, user: str = Depends(verify_credentials)):
    with get_session() as session:
        designs = session.execute(
            select(Design).where(Design.status.in_(["approved", "processed"]))
            .order_by(Design.created_at.desc())
        ).scalars().all()

        items = []
        for d in designs:
            niche = session.get(Niche, d.niche_id)
            items.append({
                "id": d.id,
                "keyword": niche.keyword if niche else "—",
                "clip_score": f"{d.clip_score:.3f}" if d.clip_score else "—",
                "raw_path": d.raw_path or "",
                "processed_path": d.processed_path or "",
                "status": d.status,
            })

    return templates.TemplateResponse("designs.html", {
        "request": request,
        "designs": items,
    })


@router.post("/designs/{design_id}/approve")
def approve_design(design_id: int, user: str = Depends(verify_credentials)):
    with get_session() as session:
        design = session.get(Design, design_id)
        if design:
            design.status = "approved"
    return RedirectResponse(url="/designs", status_code=303)


@router.post("/designs/{design_id}/reject")
def reject_design(design_id: int, user: str = Depends(verify_credentials)):
    with get_session() as session:
        design = session.get(Design, design_id)
        if design:
            design.status = "rejected"
    return RedirectResponse(url="/designs", status_code=303)
