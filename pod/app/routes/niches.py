from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy import select, func

from app.deps import templates, verify_credentials
from tools.shared.db import get_session
from tools.shared.models import Niche, Design, Listing

router = APIRouter()


@router.get("/niches", response_class=HTMLResponse)
def niche_list(request: Request, user: str = Depends(verify_credentials)):
    with get_session() as session:
        niches = session.execute(
            select(Niche).order_by(Niche.final_score.desc().nulls_last())
        ).scalars().all()

        items = []
        for n in niches:
            design_count = session.execute(
                select(func.count(Design.id)).where(Design.niche_id == n.id)
            ).scalar() or 0
            listing_count = session.execute(
                select(func.count(Listing.id)).where(Listing.niche_id == n.id)
            ).scalar() or 0

            items.append({
                "id": n.id,
                "keyword": n.keyword,
                "final_score": f"{n.final_score:.1f}" if n.final_score else "—",
                "trend_score": f"{n.trend_score:.1f}" if n.trend_score else "—",
                "velocity": f"{n.velocity:.2f}" if n.velocity else "—",
                "competition": f"{n.competition:.2f}" if n.competition else "—",
                "designs": design_count,
                "listings": listing_count,
                "status": n.status,
            })

    return templates.TemplateResponse("niches.html", {
        "request": request,
        "niches": items,
    })


@router.post("/niches/{niche_id}/kill")
def kill_niche(niche_id: int, user: str = Depends(verify_credentials)):
    with get_session() as session:
        niche = session.get(Niche, niche_id)
        if niche:
            niche.status = "killed"
    return RedirectResponse(url="/niches", status_code=303)


@router.post("/niches/{niche_id}/pause")
def pause_niche(niche_id: int, user: str = Depends(verify_credentials)):
    with get_session() as session:
        niche = session.get(Niche, niche_id)
        if niche:
            niche.status = "paused"
    return RedirectResponse(url="/niches", status_code=303)
