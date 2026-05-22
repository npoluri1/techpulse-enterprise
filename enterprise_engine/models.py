import os
import json
from datetime import datetime
from sqlalchemy import create_engine, Column, String, Float, DateTime, JSON, Boolean, Text, Integer, inspect
from sqlalchemy.orm import declarative_base, sessionmaker

from enterprise_engine.config import config

os.makedirs(os.path.dirname(config.DB_PATH), exist_ok=True)
engine = create_engine(config.DATABASE_URL, connect_args={"check_same_thread": False})
Base = declarative_base()


class Article(Base):
    __tablename__ = "articles"

    id = Column(String, primary_key=True)
    title = Column(String(500))
    url = Column(Text, unique=True)
    source = Column(String(200))
    source_type = Column(String(50))
    published = Column(DateTime, nullable=True)
    summary = Column(Text, default="")
    industry_tags = Column(JSON, default=list)
    region_tags = Column(JSON, default=list)
    category = Column(String(100), default="General")
    sentiment = Column(String(20), default="neutral")
    relevance_score = Column(Float, default=0.0)
    final_score = Column(Float, default=0.0)
    funding_amount_usd = Column(Float, nullable=True)
    funding_round = Column(String(50), nullable=True)
    has_regulatory_impact = Column(Boolean, default=False)
    key_entities = Column(JSON, default=list)
    source_credibility = Column(Float, default=5.0)
    created_at = Column(DateTime, default=datetime.utcnow)


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(String, primary_key=True)
    type = Column(String(100))
    severity = Column(Integer, default=0)
    headline = Column(String(500))
    body = Column(Text, default="")
    industry_tags = Column(JSON, default=list)
    region = Column(String(100), default="Global")
    action_url = Column(Text, default="")
    suggested_push_text = Column(String(300), default="")
    sent = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class PipelineRun(Base):
    __tablename__ = "pipeline_runs"

    id = Column(String, primary_key=True)
    started_at = Column(DateTime)
    completed_at = Column(DateTime, nullable=True)
    articles_fetched = Column(Integer, default=0)
    articles_curated = Column(Integer, default=0)
    alerts_generated = Column(Integer, default=0)
    status = Column(String(50), default="running")
    error = Column(Text, nullable=True)


class UserPreference(Base):
    __tablename__ = "user_preferences"

    id = Column(String, primary_key=True)
    industries = Column(JSON, default=list)
    regions = Column(JSON, default=list)
    alert_threshold = Column(Integer, default=75)
    created_at = Column(DateTime, default=datetime.utcnow)


def init_db():
    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()
    tables = [Article.__tablename__, Alert.__tablename__,
              PipelineRun.__tablename__, UserPreference.__tablename__]
    missing = [t for t in tables if t not in existing_tables]
    if missing:
        Base.metadata.create_all(engine)
        print(f"[DB] Created tables: {missing}")
    return engine


def get_session():
    Session = sessionmaker(bind=engine)
    return Session()


def save_article(session, article: dict):
    existing = session.query(Article).filter_by(url=article.get("url")).first()
    if not existing:
        a = Article(
            id=article.get("url", ""),
            title=article.get("title", ""),
            url=article.get("url", ""),
            source=article.get("source", ""),
            source_type=article.get("source_type", "rss"),
            published=article.get("published") if isinstance(article.get("published"), datetime) else None,
            summary=article.get("summary", ""),
            industry_tags=article.get("industry_tags", []),
            region_tags=article.get("region_tags", []),
            category=article.get("category", "General"),
            sentiment=article.get("sentiment", "neutral"),
            relevance_score=float(article.get("relevance_score", 0)),
            final_score=float(article.get("final_score", 0)),
            funding_amount_usd=article.get("funding_amount_usd"),
            funding_round=article.get("funding_round"),
            has_regulatory_impact=article.get("has_regulatory_impact", False),
            key_entities=article.get("key_entities", []),
            source_credibility=float(article.get("source_credibility", 5)),
        )
        session.add(a)
        return True
    return False


def save_alert(session, alert: dict):
    a = Alert(
        id=f"alert_{alert.get('type', '')}_{datetime.utcnow().timestamp()}",
        type=alert.get("type", ""),
        severity=alert.get("severity", 0),
        headline=alert.get("headline", ""),
        body=alert.get("body", ""),
        industry_tags=alert.get("industry_tags", []),
        region=alert.get("region", "Global"),
        action_url=alert.get("action_url", ""),
        suggested_push_text=alert.get("suggested_push_text", ""),
    )
    session.add(a)
    return True


def get_latest_articles(session, limit=50):
    return session.query(Article).order_by(
        Article.published.desc().nullslast()
    ).limit(limit).all()


def get_articles_by_industry(session, industry: str, limit=30):
    all_articles = session.query(Article).order_by(
        Article.published.desc().nullslast()
    ).limit(200).all()
    return [
        a for a in all_articles
        if a.industry_tags and industry.lower() in [t.lower() for t in a.industry_tags]
    ][:limit]


def get_articles_by_region(session, region: str, limit=30):
    all_articles = session.query(Article).order_by(
        Article.published.desc().nullslast()
    ).limit(200).all()
    return [
        a for a in all_articles
        if a.region_tags and any(region.lower() in r.lower() for r in a.region_tags)
    ][:limit]


def get_articles_by_industry_and_region(session, industry: str, region: str, limit=30):
    all_articles = session.query(Article).order_by(
        Article.published.desc().nullslast()
    ).limit(300).all()
    return [
        a for a in all_articles
        if (not industry or (a.industry_tags and industry.lower() in [t.lower() for t in a.industry_tags]))
        and (not region or region == "Global" or (a.region_tags and any(region.lower() in r.lower() for r in a.region_tags)))
    ][:limit]


def get_source_breakdown(session):
    rows = session.query(Article.source).all()
    counts = {}
    for (source,) in rows:
        key = source.split(":")[0] if ":" in source else source
        counts[key] = counts.get(key, 0) + 1
    return sorted(counts.items(), key=lambda x: x[1], reverse=True)


def get_entity_mentions(session, limit=15):
    rows = session.query(Article.key_entities).filter(
        Article.key_entities != None
    ).limit(200).all()
    counts = {}
    for (entities,) in rows:
        if entities:
            for e in entities:
                counts[e] = counts.get(e, 0) + 1
    return sorted(counts.items(), key=lambda x: x[1], reverse=True)[:limit]


def get_alerts(session, limit=20, unsent_only=False):
    q = session.query(Alert).order_by(Alert.severity.desc(), Alert.created_at.desc())
    if unsent_only:
        q = q.filter(Alert.sent == False)
    return q.limit(limit).all()


def get_pipeline_stats(session):
    total_articles = session.query(Article).count()
    total_alerts = session.query(Alert).count()
    avg_score = session.query(Article.final_score).filter(
        Article.final_score > 0
    ).all()
    avg = sum(s[0] for s in avg_score) / len(avg_score) if avg_score else 0
    return {
        "total_articles": total_articles,
        "total_alerts": total_alerts,
        "avg_score": round(avg, 1),
        "latest_run": session.query(PipelineRun).order_by(
            PipelineRun.started_at.desc()
        ).first(),
    }
