from sqlalchemy import (
    Column, Integer, String, Float, Text, DateTime, JSON, ForeignKey,
    create_engine,
)
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    pass


class Niche(Base):
    __tablename__ = "niches"
    id = Column(Integer, primary_key=True)
    keyword = Column(String, unique=True, index=True)
    trend_score = Column(Float)
    velocity = Column(Float)
    competition = Column(Float)
    final_score = Column(Float)
    status = Column(String, default="active")
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    prompts = relationship("Prompt", back_populates="niche")
    designs = relationship("Design", back_populates="niche")
    listings = relationship("Listing", back_populates="niche")


class Prompt(Base):
    __tablename__ = "prompts"
    id = Column(Integer, primary_key=True)
    niche_id = Column(Integer, ForeignKey("niches.id"))
    prompt_text = Column(Text)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=func.now())

    niche = relationship("Niche", back_populates="prompts")
    designs = relationship("Design", back_populates="prompt")


class Design(Base):
    __tablename__ = "designs"
    id = Column(Integer, primary_key=True)
    prompt_id = Column(Integer, ForeignKey("prompts.id"))
    niche_id = Column(Integer, ForeignKey("niches.id"))
    raw_path = Column(String)
    processed_path = Column(String)
    mockup_path = Column(String)
    clip_score = Column(Float)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=func.now())

    prompt = relationship("Prompt", back_populates="designs")
    niche = relationship("Niche", back_populates="designs")
    listings = relationship("Listing", back_populates="design")


class Listing(Base):
    __tablename__ = "listings"
    id = Column(Integer, primary_key=True)
    design_id = Column(Integer, ForeignKey("designs.id"))
    niche_id = Column(Integer, ForeignKey("niches.id"))
    title = Column(String)
    description = Column(Text)
    tags = Column(JSON)
    caption = Column(Text)
    etsy_listing_id = Column(String)
    printify_product_id = Column(String)
    status = Column(String, default="pending")
    views = Column(Integer, default=0)
    favorites = Column(Integer, default=0)
    sales = Column(Integer, default=0)
    revenue = Column(Float, default=0.0)
    created_at = Column(DateTime, default=func.now())
    uploaded_at = Column(DateTime)

    design = relationship("Design", back_populates="listings")
    niche = relationship("Niche", back_populates="listings")


class TaskLog(Base):
    __tablename__ = "task_logs"
    id = Column(Integer, primary_key=True)
    task_name = Column(String, index=True)
    status = Column(String)
    started_at = Column(DateTime)
    finished_at = Column(DateTime)
    error = Column(Text)
    result_summary = Column(Text)
