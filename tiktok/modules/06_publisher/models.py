"""SQLAlchemy models for the publisher module."""

from datetime import datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from modules.01_research.db import Base


class PublishedVideo(Base):
    __tablename__ = "published_videos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    edited_video_id: Mapped[int] = mapped_column(Integer, nullable=False)
    platform: Mapped[str] = mapped_column(String(50), nullable=False)
    post_id: Mapped[str | None] = mapped_column(String(200), nullable=True)
    published_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="pending")
