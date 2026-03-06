"""SQLAlchemy ORM models for autoGenVideo."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from config import DATABASE_URL

Base = declarative_base()


class Topic(Base):
    __tablename__ = "topics"
    id = Column(Integer, primary_key=True)
    topic = Column(Text, nullable=False)
    platform = Column(String(50))
    trend_score = Column(Float, default=0.0)
    hashtags = Column(Text)            # comma-separated
    source = Column(String(100))
    language = Column(String(10), default="en")
    status = Column(String(20), default="pending")  # pending | scripted | archived
    discovered_at = Column(DateTime, default=datetime.utcnow)

    scripts = relationship("Script", back_populates="topic")


class Script(Base):
    __tablename__ = "scripts"
    id = Column(Integer, primary_key=True)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    hook = Column(Text)
    body = Column(Text)                # JSON array of scene texts
    cta = Column(Text)
    caption = Column(Text)
    voiceover_text = Column(Text)
    hashtags = Column(Text)
    language = Column(String(10), default="en")
    duration_target = Column(Integer, default=30)   # seconds
    status = Column(String(20), default="pending")  # pending | assets_ready | rendered | published
    created_at = Column(DateTime, default=datetime.utcnow)

    topic = relationship("Topic", back_populates="scripts")
    video = relationship("Video", back_populates="script", uselist=False)


class Video(Base):
    __tablename__ = "videos"
    id = Column(Integer, primary_key=True)
    script_id = Column(Integer, ForeignKey("scripts.id"), nullable=False)
    file_path = Column(Text)
    thumbnail_path = Column(Text)
    duration = Column(Float)
    resolution = Column(String(20))
    status = Column(String(20), default="rendering")  # rendering | ready | published | archived
    created_at = Column(DateTime, default=datetime.utcnow)

    script = relationship("Script", back_populates="video")
    publications = relationship("Publication", back_populates="video")


class Publication(Base):
    __tablename__ = "publications"
    id = Column(Integer, primary_key=True)
    video_id = Column(Integer, ForeignKey("videos.id"), nullable=False)
    platform = Column(String(50))    # tiktok | youtube | instagram | pinterest
    post_id = Column(String(200))
    url = Column(Text)
    posted_at = Column(DateTime)
    status = Column(String(20), default="pending")  # pending | posted | failed

    video = relationship("Video", back_populates="publications")
    analytics = relationship("Analytics", back_populates="publication")


class Analytics(Base):
    __tablename__ = "analytics"
    id = Column(Integer, primary_key=True)
    pub_id = Column(Integer, ForeignKey("publications.id"), nullable=False)
    platform = Column(String(50))
    views = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    shares = Column(Integer, default=0)
    watch_time_avg = Column(Float, default=0.0)
    engagement_rate = Column(Float, default=0.0)
    collected_at = Column(DateTime, default=datetime.utcnow)

    publication = relationship("Publication", back_populates="analytics")


engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_session():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
