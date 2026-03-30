from sqlalchemy import (
    Column, Integer, String, Float, Text, DateTime, JSON, ForeignKey, Boolean,
)
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    pass


class Niche(Base):
    __tablename__ = "niches"
    id = Column(Integer, primary_key=True)
    keyword = Column(String, unique=True, index=True)
    trend_score = Column(Float)           # latest composite trend score (0-100)
    velocity = Column(Float)              # momentum: positive=rising, negative=fading
    competition = Column(Float)           # estimated competition (0-1)
    final_score = Column(Float)           # niche_scorer normalised score (0-100)
    # Gemini-sourced enrichment
    gemini_reason = Column(Text)          # latest Gemini explanation for why this is trending
    upcoming_score = Column(Float)        # Gemini's predicted score 2-4 weeks ahead
    # Per-source breakdown for transparency
    # e.g. {"gemini": 75.0, "pytrends": 60.0, "reddit": 45.0, "etsy": 55.0}
    source_scores = Column(JSON)
    # Blue ocean fields
    competition_level = Column(Float)     # 0.0 (no competition) to 1.0 (saturated)
    blue_ocean_score = Column(Float)      # demand × (1 - competition): higher = better opportunity
    parent_niche = Column(String)         # broader trending niche this was derived from
    target_customer = Column(Text)        # who buys this (age, identity, occasion, budget)
    recommended_products = Column(JSON)   # e.g. ["mug", "tote", "sweatshirt"]
    design_pattern = Column(Text)         # visual style/theme recommendation
    status = Column(String, default="active")
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    prompts = relationship("Prompt", back_populates="niche")
    designs = relationship("Design", back_populates="niche")
    listings = relationship("Listing", back_populates="niche")
    snapshots = relationship("TrendSnapshot", back_populates="niche")


class TrendSnapshot(Base):
    """Point-in-time recording of a niche's trend metrics from any source.

    Multiple rows per niche enable ranking trends over time and comparing
    how popularity evolves across sources (Gemini, pytrends, Reddit, Etsy).
    Query the last N snapshots per niche to detect acceleration/deceleration.
    """
    __tablename__ = "trend_snapshots"
    id = Column(Integer, primary_key=True)
    niche_id = Column(Integer, ForeignKey("niches.id"), index=True)
    source = Column(String, index=True)   # "gemini" | "pytrends" | "reddit" | "etsy"
    trend_score = Column(Float)           # 0-100
    velocity = Column(Float)              # -1.0 to 1.0
    rank_position = Column(Integer)       # rank among all niches in this run (1 = top)
    reason = Column(Text)                 # explanation string (Gemini only)
    is_upcoming = Column(Boolean, default=False)  # True = predicted future trend
    horizon_days = Column(Integer)        # days ahead the prediction covers
    snapshot_date = Column(DateTime, default=func.now(), index=True)
    # Blue ocean fields (populated by blue_ocean_scraper)
    competition_level = Column(Float)     # 0.0–1.0
    blue_ocean_score = Column(Float)      # demand × (1 − competition)

    niche = relationship("Niche", back_populates="snapshots")


class Prompt(Base):
    __tablename__ = "prompts"
    id = Column(Integer, primary_key=True)
    niche_id = Column(Integer, ForeignKey("niches.id"))
    # The actual prompt text sent to the image generator
    prompt_text = Column(Text)
    # Metadata stored per-prompt for SEO reuse and reproducibility
    keywords = Column(JSON)               # ["personalized mom gift", "mama sweatshirt", ...]
    design_style = Column(String)         # "vintage" | "minimalist" | "maximalist" | "romantic goth"
    product_types = Column(JSON)          # ["t-shirt", "mug", "tote"] — applicable product types
    target_persona = Column(String)       # "gen_x_women" | "millennials" | "gen_z"
    color_palette = Column(String)        # e.g. "Patina Blue, Washed Linen, Persimmon"
    image_backend = Column(String)        # preferred backend: "gemini" | "stability" | "dalle" | "auto"
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
    image_backend = Column(String)        # "gemini" | "stability" | "dalle" — which actually ran
    generation_params = Column(JSON)      # model, resolution, steps, cfg_scale etc. for audit
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
