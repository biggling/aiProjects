"""SQLAlchemy models for analytics."""

from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from modules.01_research.db import Base


class VideoMetric(Base):
    __tablename__ = "video_metrics"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    published_video_id: Mapped[int] = mapped_column(Integer, nullable=False)
    pulled_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    views: Mapped[int] = mapped_column(Integer, default=0)
    watch_time_avg: Mapped[float] = mapped_column(Float, default=0.0)
    likes: Mapped[int] = mapped_column(Integer, default=0)
    shares: Mapped[int] = mapped_column(Integer, default=0)
    comments: Mapped[int] = mapped_column(Integer, default=0)
    ctr: Mapped[float] = mapped_column(Float, default=0.0)
    gmv: Mapped[float] = mapped_column(Float, default=0.0)
    winner: Mapped[bool] = mapped_column(Boolean, default=False)
