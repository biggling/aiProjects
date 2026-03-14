"""Content brief read and product approval endpoints."""

import asyncio
import json
from datetime import date, datetime

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from api.deps import get_db, verify_api_key
from modules.01_research.models import ContentBrief

router = APIRouter(prefix="/api/brief", tags=["brief"], dependencies=[Depends(verify_api_key)])


class BriefResponse(BaseModel):
    id: int
    date: str
    ideas: list[dict]
    human_approved: bool
    approved_at: datetime | None

    model_config = {"from_attributes": True}


class ApproveRequest(BaseModel):
    idea_ids: list[int]


@router.get("/today", response_model=BriefResponse)
async def get_today_brief(db: Session = Depends(get_db)):
    """Get today's content brief."""
    today = date.today().isoformat()
    brief = await asyncio.to_thread(
        lambda: db.query(ContentBrief)
        .filter(ContentBrief.date == today)
        .order_by(ContentBrief.id.desc())
        .first()
    )
    if not brief:
        raise HTTPException(status_code=404, detail="No brief found for today")

    return BriefResponse(
        id=brief.id,
        date=brief.date,
        ideas=json.loads(brief.ideas_json),
        human_approved=brief.human_approved,
        approved_at=brief.approved_at,
    )


@router.post("/approve", response_model=BriefResponse)
async def approve_brief(body: ApproveRequest, db: Session = Depends(get_db)):
    """Approve selected ideas from today's brief."""
    today = date.today().isoformat()
    brief = await asyncio.to_thread(
        lambda: db.query(ContentBrief)
        .filter(ContentBrief.date == today)
        .order_by(ContentBrief.id.desc())
        .first()
    )
    if not brief:
        raise HTTPException(status_code=404, detail="No brief found for today")

    # Filter ideas to only approved ones
    ideas = json.loads(brief.ideas_json)
    approved_ideas = [idea for i, idea in enumerate(ideas) if i in body.idea_ids]

    brief.ideas_json = json.dumps(approved_ideas, ensure_ascii=False)
    brief.human_approved = True
    brief.approved_at = datetime.utcnow()
    await asyncio.to_thread(db.commit)

    return BriefResponse(
        id=brief.id,
        date=brief.date,
        ideas=approved_ideas,
        human_approved=True,
        approved_at=brief.approved_at,
    )
