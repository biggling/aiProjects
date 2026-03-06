"""SQLAlchemy ORM models for autoPOD"""
from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Float, Text, DateTime, ForeignKey, create_engine
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from config import DATABASE_URL

Base = declarative_base()


class Niche(Base):
    __tablename__ = "niches"

    id = Column(Integer, primary_key=True)
    niche = Column(String(200), unique=True, nullable=False)
    search_volume = Column(Integer, default=0)
    competition_score = Column(Float, default=0.0)
    trend_score = Column(Float, default=0.0)
    source = Column(String(100))
    status = Column(String(20), default="active")  # active | paused
    discovered_at = Column(DateTime, default=datetime.utcnow)

    designs = relationship("Design", back_populates="niche")


class Design(Base):
    __tablename__ = "designs"

    id = Column(Integer, primary_key=True)
    niche_id = Column(Integer, ForeignKey("niches.id"), nullable=False)
    style = Column(String(100))         # typography | illustrated | hybrid
    product_type = Column(String(100))  # tshirt | mug | sticker | poster
    file_path = Column(Text)
    dalle_prompt = Column(Text)
    status = Column(String(20), default="ready")  # ready | published | rejected
    created_at = Column(DateTime, default=datetime.utcnow)

    niche = relationship("Niche", back_populates="designs")
    listings = relationship("Listing", back_populates="design")


class Listing(Base):
    __tablename__ = "listings"

    id = Column(Integer, primary_key=True)
    design_id = Column(Integer, ForeignKey("designs.id"), nullable=False)
    platform = Column(String(50))       # etsy | redbubble | amazon
    external_id = Column(String(200))
    url = Column(Text)
    title = Column(Text)
    description = Column(Text)
    tags = Column(Text)                 # comma-separated
    price = Column(Float)
    status = Column(String(20), default="active")  # active | paused | optimized
    published_at = Column(DateTime)
    last_optimized_at = Column(DateTime)

    design = relationship("Design", back_populates="listings")
    orders = relationship("Order", back_populates="listing")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    listing_id = Column(Integer, ForeignKey("listings.id"), nullable=False)
    platform = Column(String(50))
    qty = Column(Integer, default=1)
    revenue = Column(Float, default=0.0)
    platform_fee = Column(Float, default=0.0)
    print_cost = Column(Float, default=0.0)
    profit = Column(Float, default=0.0)
    fulfillment_status = Column(String(50))  # pending | processing | shipped | delivered
    order_date = Column(DateTime)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    listing = relationship("Listing", back_populates="orders")


class Competitor(Base):
    __tablename__ = "competitor"

    id = Column(Integer, primary_key=True)
    niche = Column(String(200))
    platform = Column(String(50))
    title = Column(Text)
    price = Column(Float)
    reviews = Column(Integer)
    tags = Column(Text)
    url = Column(Text)
    scraped_at = Column(DateTime, default=datetime.utcnow)


class MarketingLog(Base):
    __tablename__ = "marketing_log"

    id = Column(Integer, primary_key=True)
    listing_id = Column(Integer, ForeignKey("listings.id"), nullable=True)
    platform = Column(String(50))       # pinterest | reddit | instagram
    content = Column(Text)
    post_url = Column(Text)
    posted_at = Column(DateTime, default=datetime.utcnow)
    clicks = Column(Integer, default=0)


class OptimizationLog(Base):
    __tablename__ = "optimization_log"

    id = Column(Integer, primary_key=True)
    listing_id = Column(Integer, ForeignKey("listings.id"), nullable=False)
    change_type = Column(String(100))   # title | tags | price | paused
    old_value = Column(Text)
    new_value = Column(Text)
    optimized_at = Column(DateTime, default=datetime.utcnow)


# ── Engine & Session Factory ──────────────────────────────────────────────────
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_session():
    """Context manager for DB sessions."""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
