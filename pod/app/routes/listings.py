from fastapi import APIRouter, Depends, Request, Query
from fastapi.responses import HTMLResponse
from sqlalchemy import select

from app.deps import templates, verify_credentials
from tools.shared.db import get_session
from tools.shared.models import Listing, Niche

router = APIRouter()

PAGE_SIZE = 25


@router.get("/listings", response_class=HTMLResponse)
def listing_list(
    request: Request,
    status_filter: str = Query(default="all"),
    page: int = Query(default=1, ge=1),
    user: str = Depends(verify_credentials),
):
    with get_session() as session:
        query = select(Listing)
        if status_filter != "all":
            query = query.where(Listing.status == status_filter)
        query = query.order_by(Listing.created_at.desc())

        total = session.execute(
            select(Listing.id).where(
                Listing.status == status_filter if status_filter != "all" else True
            )
        ).all()
        total_count = len(total)

        offset = (page - 1) * PAGE_SIZE
        listings_raw = session.execute(
            query.offset(offset).limit(PAGE_SIZE)
        ).scalars().all()

        items = []
        for l in listings_raw:
            niche = session.get(Niche, l.niche_id) if l.niche_id else None
            items.append({
                "id": l.id,
                "title": l.title or "—",
                "keyword": niche.keyword if niche else "—",
                "status": l.status,
                "etsy_id": l.etsy_listing_id or "—",
                "views": l.views or 0,
                "favorites": l.favorites or 0,
                "revenue": f"${l.revenue:.2f}" if l.revenue else "$0.00",
                "description": l.description or "",
                "tags": l.tags or [],
                "mockup_path": "",
            })

    return templates.TemplateResponse("listings.html", {
        "request": request,
        "listings": items,
        "status_filter": status_filter,
        "page": page,
        "total_pages": max(1, (total_count + PAGE_SIZE - 1) // PAGE_SIZE),
    })
