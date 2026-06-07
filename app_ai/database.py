import os
import logging
from datetime import datetime, timezone
from sqlalchemy import create_engine, Column, Integer, String, Text, Boolean, DateTime, ForeignKey, JSON, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session

logger = logging.getLogger("NewsAI.DB")

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "ai_news.db")
DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(120), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    display_name = Column(String(100), default="")
    avatar = Column(String(500), default="")
    bio = Column(Text, default="")
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    preferences = relationship("UserPreference", uselist=False, back_populates="user")
    bookmarks = relationship("Bookmark", back_populates="user", cascade="all, delete-orphan")
    reading_history = relationship("ReadingHistory", back_populates="user", cascade="all, delete-orphan")

class UserPreference(Base):
    __tablename__ = "user_preferences"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    dark_mode = Column(Boolean, default=False)
    subscribed_categories = Column(JSON, default=list)
    email_notifications = Column(Boolean, default=False)
    article_layout = Column(String(20), default="card")
    font_size = Column(String(10), default="medium")
    user = relationship("User", back_populates="preferences")

class Bookmark(Base):
    __tablename__ = "bookmarks"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    article_title = Column(String(500))
    article_url = Column(String(1000))
    article_source = Column(String(200))
    article_summary = Column(Text, default="")
    article_category = Column(String(100), default="")
    article_image = Column(String(1000), default="")
    saved_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    user = relationship("User", back_populates="bookmarks")

class ReadingHistory(Base):
    __tablename__ = "reading_history"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    article_title = Column(String(500))
    article_url = Column(String(1000))
    article_category = Column(String(100), default="")
    read_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    read_count = Column(Integer, default=1)
    user = relationship("User", back_populates="reading_history")

class NewsArticle(Base):
    __tablename__ = "news_articles"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), index=True)
    url = Column(String(1000), unique=True)
    source = Column(String(200))
    category = Column(String(100), index=True)
    summary = Column(Text, default="")
    content = Column(Text, default="")
    published = Column(String(50))
    author = Column(String(200), default="")
    image_url = Column(String(1000), default="")
    score = Column(Float, default=0.0)
    fetched_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class ArticleEmbedding(Base):
    __tablename__ = "article_embeddings"
    id = Column(Integer, primary_key=True, index=True)
    article_id = Column(Integer, ForeignKey("news_articles.id"))
    embedding_id = Column(String(100), unique=True)


class NotificationHistory(Base):
    __tablename__ = "notification_history"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    channel = Column(String(20), default="email")  # email, whatsapp, in-app
    title = Column(String(500), default="")
    message = Column(Text, default="")
    status = Column(String(20), default="sent")  # sent, failed, read
    read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "id": self.id,
            "channel": self.channel,
            "title": self.title,
            "message": self.message[:200] if self.message else "",
            "status": self.status,
            "read": self.read,
            "created_at": self.created_at.isoformat() if self.created_at else "",
            "time_ago": (datetime.now(timezone.utc) - self.created_at).total_seconds() // 60 if self.created_at else 0
        }


class NewsletterSubscription(Base):
    __tablename__ = "newsletter_subscriptions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    email = Column(String(120), nullable=False)
    frequency = Column(String(20), default="weekly")  # daily, weekly, monthly
    categories = Column(JSON, default=list)
    enabled = Column(Boolean, default=True)
    last_sent_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


def init_db():
    Base.metadata.create_all(bind=engine)
    logger.info("Database initialized")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
