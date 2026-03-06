"""SQLAlchemy ORM models for autoTiktok."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from config import DATABASE_URL

Base = declarative_base()


class Niche(Base):
    __tablename__ = "niches"
    id = Column(Integer, primary_key=True)
    niche = Column(String(100), nullable=False)
    product_name = Column(Text)
    product_url = Column(Text)
    affiliate_link = Column(Text)
    affiliate_network = Column(String(50))  # amazon | tiktok_shop | shareasale
    commission_pct = Column(Float, default=0.0)
    trend_score = Column(Float, default=0.0)
    performance_score = Column(Float, default=0.0)
    status = Column(String(20), default="active")  # active | paused | retired
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    scripts = relationship("Script", back_populates="product")


class Trend(Base):
    __tablename__ = "trends"
    id = Column(Integer, primary_key=True)
    niche = Column(String(100))
    hook_pattern = Column(String(50))    # question | bold_claim | tutorial | reaction | curiosity_gap
    hook_text = Column(Text)
    trending_sound_id = Column(String(200))
    sound_name = Column(String(200))
    hashtags = Column(Text)              # comma-separated
    top_video_url = Column(Text)
    views = Column(Integer, default=0)
    scraped_at = Column(DateTime, default=datetime.utcnow)


class Script(Base):
    __tablename__ = "scripts"
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("niches.id"), nullable=False)
    hook = Column(Text)
    body = Column(Text)                  # JSON scenes array
    cta = Column(Text)
    voiceover_text = Column(Text)
    caption = Column(Text)
    hashtags = Column(Text)
    sound_id = Column(String(200))
    confidence_score = Column(Float, default=0.0)
    status = Column(String(20), default="pending")  # pending | approved | rejected | rendered | posted
    created_at = Column(DateTime, default=datetime.utcnow)

    product = relationship("Niche", back_populates="scripts")
    video = relationship("Video", back_populates="script", uselist=False)


class Video(Base):
    __tablename__ = "videos"
    id = Column(Integer, primary_key=True)
    script_id = Column(Integer, ForeignKey("scripts.id"), nullable=False)
    file_path = Column(Text)
    thumbnail_path = Column(Text)
    duration = Column(Float)
    status = Column(String(20), default="ready")  # ready | posted | archived
    created_at = Column(DateTime, default=datetime.utcnow)

    script = relationship("Script", back_populates="video")
    posts = relationship("Post", back_populates="video")


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    video_id = Column(Integer, ForeignKey("videos.id"), nullable=False)
    platform = Column(String(50))        # tiktok | instagram | youtube
    tiktok_video_id = Column(String(200))
    url = Column(Text)
    caption = Column(Text)
    hashtags = Column(Text)
    posted_at = Column(DateTime)
    status = Column(String(20), default="posted")

    video = relationship("Video", back_populates="posts")
    analytics = relationship("Analytics", back_populates="post")
    affiliate_data = relationship("Affiliate", back_populates="post")


class Analytics(Base):
    __tablename__ = "analytics"
    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    views_24h = Column(Integer, default=0)
    views_7d = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    shares = Column(Integer, default=0)
    follows_gained = Column(Integer, default=0)
    link_clicks = Column(Integer, default=0)
    engagement_rate = Column(Float, default=0.0)
    collected_at = Column(DateTime, default=datetime.utcnow)

    post = relationship("Post", back_populates="analytics")


class Affiliate(Base):
    __tablename__ = "affiliate"
    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=True)
    product_name = Column(Text)
    affiliate_network = Column(String(50))
    clicks = Column(Integer, default=0)
    conversions = Column(Integer, default=0)
    commission = Column(Float, default=0.0)
    period = Column(String(10))         # YYYY-MM-DD
    recorded_at = Column(DateTime, default=datetime.utcnow)

    post = relationship("Post", back_populates="affiliate_data")


engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
