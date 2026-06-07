#!/usr/bin/env python3
"""
NovaPulse AI - Next Generation AI-Powered News Platform
====================================================
Features:
  - Apple Design System (iMac, iPad, iPhone responsive)
  - JWT Authentication with user profiles
  - RAG (Retrieval Augmented Generation) with ChromaDB
  - AI Agent orchestration with LangGraph patterns
  - Vector search for semantic article discovery
  - Bookmarking, reading history, personalized feed
  - Multi-source news aggregation from RSS, Web, APIs
  - Gemini AI for intelligent summarization & chat
  - Dark/Light mode with system preference support
"""

import os, sys, re, json, logging, asyncio, threading, hashlib
import yaml
from pathlib import Path
import pytz
from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo
from typing import Optional, List, Dict, Any, Union
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Depends, HTTPException, status, Form, Query, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordRequestForm
from jinja2 import Environment, FileSystemLoader
from sqlalchemy.orm import Session
from apscheduler.schedulers.background import BackgroundScheduler

sys.path.insert(0, str(Path(__file__).parent))
from app_ai.auth import (
    verify_password, get_password_hash, create_access_token, decode_token,
    get_current_user, TokenData, SECRET_KEY, ALGORITHM
)
from app_ai.database import (
    init_db, get_db, SessionLocal, User, UserPreference, Bookmark,
    ReadingHistory, NewsArticle
)
from app_ai.vector_store import vector_store
from app_ai.rag_engine import rag_engine
from app_ai.agent_orchestrator import agent_orchestrator, register_news_tools
from app_ai.ai_tools_catalog import AI_TOOLS_CATALOG
from app_ai.notifier import (
    load_notif_config, save_notif_config,
    load_schedule_config, save_schedule_config,
    send_notifications, test_notification
)
from app_ai.openalternative_data import OPENALTERNATIVE_DATA

# Enterprise pipeline imports for country-based news fetching
sys.path.insert(0, str(Path(__file__).parent))
from enterprise_engine.pipeline import EnterprisePipeline
from enterprise_engine.config import config as enterprise_config
from enterprise_engine.industry_categories import get_all_industries, tag_industries
from enterprise_engine.models import get_session, get_latest_articles, get_articles_by_industry, get_articles_by_region, get_articles_by_industry_and_region

logger = logging.getLogger("NewsAI")
CONFIG_PATH = Path(__file__).parent / "config.yaml"
OUTPUT_DIR = Path(__file__).parent / "output"
TEMPLATES_DIR = Path(__file__).parent / "templates_v2"
STATIC_DIR = Path(__file__).parent / "static"
STATIC_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

jinja_env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)))
scheduler = BackgroundScheduler()
enterprise_pipeline = EnterprisePipeline()

# Current country filter state (for dashboard)
CURRENT_COUNTRY = "Global"
LAST_FETCH_STATUS = {"status": "idle", "message": "No runs yet", "time": None}
WEBSOCKET_CLIENTS = set()

def load_config():
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH) as f:
            return yaml.safe_load(f)
    return {}

def format_date(s):
    try:
        dt = datetime.fromisoformat(s.replace("Z", "+00:00")) if isinstance(s, str) else s
        return dt.strftime("%d %b %Y, %H:%M")
    except:
        return str(s)[:10] if s else ""

def time_ago(s):
    try:
        dt = datetime.fromisoformat(s.replace("Z", "+00:00")) if isinstance(s, str) else s
        diff = datetime.now(dt.tzinfo) - dt
        days = diff.days
        if days == 0:
            hours = diff.seconds // 3600
            return f"{hours}h ago" if hours else f"{diff.seconds // 60}m ago"
        return f"{days}d ago"
    except:
        return ""

def get_articles_for_rag(db: Session, category: str = None, limit: int = 50):
    query = db.query(NewsArticle)
    if category:
        query = query.filter(NewsArticle.category == category)
    return query.order_by(NewsArticle.score.desc()).limit(limit).all()

def search_articles_fn(query: str, category: str = None, db: Session = None):
    articles = []
    if vector_store.embeddings_enabled:
        results = vector_store.search(query, n_results=15)
        articles = results
    if not articles and db:
        q = db.query(NewsArticle)
        if category:
            q = q.filter(NewsArticle.category == category)
        for kw in query.lower().split()[:3]:
            q = q.filter(NewsArticle.title.ilike(f"%{kw}%"))
        db_articles = q.limit(10).all()
        articles = [{"id": str(a.id), "title": a.title, "url": a.url, "source": a.source, "summary": a.summary, "category": a.category} for a in db_articles]
    return articles

def get_summary_fn(db: Session = None):
    articles = db.query(NewsArticle).order_by(NewsArticle.score.desc()).limit(5).all() if db else []
    summary = "\n".join([f"• {a.title}" for a in articles]) if articles else "No articles yet. Fetch news to get started."
    return {"summary": summary, "count": len(articles)}

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    logger.info("Database initialized")
    register_news_tools(
        lambda: get_summary_fn(),
        lambda query, category=None: search_articles_fn(query, category),
        lambda: get_summary_fn()
    )
    # Initialize enterprise engine database
    from enterprise_engine.models import init_db as ee_init_db
    ee_init_db()        # Auto-sync existing enterprise articles to main app DB on startup
    try:
        logger.info("Auto-syncing enterprise articles to main app DB...")
        sync_enterprise_to_main(country="Global")
        db_check = SessionLocal()
        try:
            count = db_check.query(NewsArticle).count()
            logger.info(f"Main app DB now has {count} articles")
        finally:
            db_check.close()
    except Exception as e:
        logger.warning(f"Auto-sync on startup failed (non-fatal): {e}")
    
    # Set up scheduling - every 2 hours for real-time updates
    sched_cfg = load_schedule_config()
    sched_enabled = sched_cfg.get("enabled", True)

    if sched_enabled:
        if not scheduler.get_job("news_fetch_every_2h"):
            from apscheduler.triggers.interval import IntervalTrigger
            scheduler.add_job(
                run_news_fetch_with_notify,
                trigger=IntervalTrigger(minutes=10, jitter=3000),
                id="news_fetch_every_2h",
                replace_existing=True,
                kwargs={"country": CURRENT_COUNTRY}
            )
            import random
            next_min = random.randint(10, 60)
            logger.info(f"[Scheduler] News fetch every {next_min} min (10-60 random) for country: {CURRENT_COUNTRY}")
        else:
            scheduler.reschedule_job(
                "news_fetch_every_2h",
                trigger=IntervalTrigger(minutes=10, jitter=3000)
            )
    else:
        job = scheduler.get_job("news_fetch_every_2h")
        if job:
            job.remove()
            logger.info("[Scheduler] Disabled")
    scheduler.start()
    logger.info("[Scheduler] Started")

    thread = threading.Thread(target=delayed_initial_fetch, daemon=True)
    thread.start()

    yield
    scheduler.shutdown(wait=False)

# Collect accent classes for categories
CATEGORY_ACCENTS = {
    "AI Coding Agents": "blue",
    "AI Agent Frameworks": "purple",
    "Vector Databases & RAG": "green",
    "AI Video & Image": "orange",
    "AI Voice & Audio": "red",
    "AI Platforms & Infrastructure": "teal",
    "LLMs & Foundation Models": "blue",
    "AI Business & Marketing": "orange",
    "MLOps & Production": "teal",
    "AI Security & Compliance": "red",
    "Analytics & Monitoring": "green",
    "Automation & Workflows": "purple"
}

CATEGORY_ICONS = {
    cat["name"]: cat["icon"] for cat in AI_TOOLS_CATALOG["categories"]
}

app = FastAPI(title="NovaPulse AI", lifespan=lifespan)

@app.get("/favicon.ico")
async def favicon():
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
    <defs><linearGradient id="g" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0071e3"/>
      <stop offset="100%" stop-color="#40a9ff"/>
    </linearGradient></defs>
    <rect width="100" height="100" rx="20" fill="url(#g)"/>
    <text x="50" y="68" font-family="Arial,sans-serif" font-size="52" font-weight="800" fill="white" text-anchor="middle">AI</text>
    </svg>'''
    from fastapi.responses import Response
    return Response(content=svg, media_type="image/svg+xml")

@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    token = request.cookies.get("access_token") or request.headers.get("Authorization", "").replace("Bearer ", "")
    user = None
    if token:
        token_data = decode_token(token)
        if token_data:
            user = token_data
    request.state.user = user
    response = await call_next(request)
    return response

def render(template_name: str, request: Request, **kwargs):
    tmpl = jinja_env.get_template(template_name)
    user = getattr(request.state, "user", None)
    db = next(get_db())
    prefs = {}
    if user:
        user_pref = db.query(UserPreference).filter(UserPreference.user_id == user.user_id).first()
        if user_pref:
            prefs = {"dark_mode": user_pref.dark_mode, "font_size": user_pref.font_size}
    db.close()
    html = tmpl.render(
        user=user,
        prefs=prefs,
        year=datetime.now().year,
        **kwargs
    )
    return HTMLResponse(html)

# ==== AUTH ROUTES ====

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return render("login.html", request=request)

@app.post("/api/auth/register")
async def register(request: Request, data: dict):
    db = next(get_db())
    try:
        username = data.get("username", "").strip()
        email = data.get("email", "").strip()
        password = data.get("password", "")
        if not username or not email or not password:
            raise HTTPException(400, "All fields required")
        if len(password) < 6:
            raise HTTPException(400, "Password must be at least 6 characters")
        if db.query(User).filter((User.username == username) | (User.email == email)).first():
            raise HTTPException(400, "Username or email already exists")
        user = User(username=username, email=email, hashed_password=get_password_hash(password), display_name=username)
        db.add(user)
        db.flush()
        prefs = UserPreference(user_id=user.id, subscribed_categories=[])
        db.add(prefs)
        db.commit()
        token = create_access_token({"sub": user.username, "id": user.id})
        return {"token": token, "username": user.username}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(500, str(e))
    finally:
        db.close()

@app.post("/api/auth/login")
async def login(request: Request, data: dict):
    db = next(get_db())
    try:
        username = data.get("username", "")
        password = data.get("password", "")
        user = db.query(User).filter(User.username == username).first()
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(401, "Invalid credentials")
        token = create_access_token({"sub": user.username, "id": user.id})
        return {"token": token, "username": user.username, "email": user.email}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))
    finally:
        db.close()

@app.post("/api/auth/token")
async def token_login(form_data: OAuth2PasswordRequestForm = Depends()):
    db = next(get_db())
    try:
        user = db.query(User).filter(User.username == form_data.username).first()
        if not user or not verify_password(form_data.password, user.hashed_password):
            raise HTTPException(401, "Invalid credentials")
        token = create_access_token({"sub": user.username, "id": user.id})
        return {"access_token": token, "token_type": "bearer"}
    finally:
        db.close()

@app.get("/api/auth/me")
async def get_me(request: Request):
    user = getattr(request.state, "user", None)
    if not user:
        return JSONResponse({"authenticated": False}, status_code=401)
    db = next(get_db())
    try:
        db_user = db.query(User).filter(User.id == user.user_id).first()
        if not db_user:
            return {"authenticated": False}
        prefs = db.query(UserPreference).filter(UserPreference.user_id == user.user_id).first()
        return {
            "authenticated": True,
            "id": db_user.id,
            "username": db_user.username,
            "email": db_user.email,
            "display_name": db_user.display_name,
            "bio": db_user.bio or "",
            "avatar": db_user.avatar or "",
            "preferences": {
                "dark_mode": prefs.dark_mode if prefs else False,
                "subscribed_categories": prefs.subscribed_categories if prefs else [],
                "font_size": prefs.font_size if prefs else "medium",
                "article_layout": prefs.article_layout if prefs else "card"
            } if prefs else {}
        }
    finally:
        db.close()

@app.post("/api/auth/preferences")
async def update_preferences(request: Request, data: dict):
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(401)
    db = next(get_db())
    try:
        prefs = db.query(UserPreference).filter(UserPreference.user_id == user.user_id).first()
        if not prefs:
            prefs = UserPreference(user_id=user.user_id)
            db.add(prefs)
        if "dark_mode" in data: prefs.dark_mode = data["dark_mode"]
        if "subscribed_categories" in data: prefs.subscribed_categories = data["subscribed_categories"]
        if "font_size" in data: prefs.font_size = data["font_size"]
        if "article_layout" in data: prefs.article_layout = data["article_layout"]
        db.commit()
        return {"status": "ok"}
    finally:
        db.close()

@app.post("/api/auth/logout")
async def logout():
    resp = JSONResponse({"status": "ok"})
    resp.delete_cookie("access_token")
    return resp

# ==== MAIN PAGES ====

@app.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    db = next(get_db())
    try:
        articles = db.query(NewsArticle).order_by(NewsArticle.score.desc()).limit(60).all()
        categories = db.query(NewsArticle.category).distinct().all()
        cat_list = sorted(set(c[0] for c in categories if c[0]))
        articles_data = [{
            "id": a.id, "title": a.title, "url": a.url, "source": a.source,
            "category": a.category or "General", "summary": a.summary[:200] if a.summary else "",
            "published": time_ago(a.published) if a.published else "",
            "score": round(a.score, 1)
        } for a in articles]
        return render("dashboard.html", request=request, articles=articles_data, categories=cat_list, total_articles=len(articles_data))
    finally:
        db.close()

@app.get("/learn", response_class=HTMLResponse)
async def learn_page(request: Request):
    return render("learn.html", request=request)

@app.get("/profile", response_class=HTMLResponse)
async def profile_page(request: Request):
    user = getattr(request.state, "user", None)
    if not user:
        return RedirectResponse("/login")
    db = next(get_db())
    try:
        db_user = db.query(User).filter(User.id == user.user_id).first()
        bookmarks = db.query(Bookmark).filter(Bookmark.user_id == user.user_id).order_by(Bookmark.saved_at.desc()).all()
        history = db.query(ReadingHistory).filter(ReadingHistory.user_id == user.user_id).order_by(ReadingHistory.read_at.desc()).limit(50).all()
        return render("profile.html", request=request, profile=db_user, bookmarks=bookmarks, history=history)
    finally:
        db.close()

# ==== API ROUTES ====

@app.get("/api/articles")
async def get_articles(request: Request, category: str = "", search: str = "", country: str = "", page: int = 1, limit: int = 30):
    db = next(get_db())
    try:
        q = db.query(NewsArticle)
        if category:
            q = q.filter(NewsArticle.category == category)
        if search:
            q = q.filter(NewsArticle.title.ilike(f"%{search}%"))
        # Country filtering: if a country is selected, also filter from enterprise_engine articles
        # For main DB, we use category-based filtering as proxy for country
        # (country info is stored in enterprise_engine's own DB with region_tags)
        total = q.count()
        articles = q.order_by(NewsArticle.score.desc()).offset((page-1)*limit).limit(limit).all()
        
        result_articles = [{
            "id": a.id, "title": a.title, "url": a.url, "source": a.source,
            "category": a.category, "summary": a.summary[:200],
            "published": str(a.published)[:10] if a.published else "",
            "time_ago": time_ago(a.published) if a.published else "",
            "score": round(a.score, 1)
        } for a in articles]
        
        return {
            "articles": result_articles,
            "total": total,
            "page": page,
            "pages": (total + limit - 1) // limit,
            "current_country": CURRENT_COUNTRY
        }
    finally:
        db.close()

@app.get("/api/articles/{article_id}")
async def get_article(article_id: int, request: Request):
    db = next(get_db())
    try:
        a = db.query(NewsArticle).filter(NewsArticle.id == article_id).first()
        if not a:
            raise HTTPException(404)
        user = getattr(request.state, "user", None)
        if user:
            existing = db.query(ReadingHistory).filter(
                ReadingHistory.user_id == user.user_id,
                ReadingHistory.article_url == a.url
            ).first()
            if existing:
                existing.read_count += 1
                existing.read_at = datetime.now(timezone.utc)
            else:
                db.add(ReadingHistory(user_id=user.user_id, article_title=a.title, article_url=a.url, article_category=a.category))
            db.commit()
        return {
            "id": a.id, "title": a.title, "url": a.url, "source": a.source,
            "category": a.category, "summary": a.summary, "content": a.content,
            "published": a.published, "author": a.author
        }
    finally:
        db.close()

@app.post("/api/bookmarks")
async def add_bookmark(request: Request, data: dict):
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(401)
    db = next(get_db())
    try:
        existing = db.query(Bookmark).filter(
            Bookmark.user_id == user.user_id,
            Bookmark.article_url == data.get("url", "")
        ).first()
        if existing:
            return {"status": "already_exists", "id": existing.id}
        bm = Bookmark(
            user_id=user.user_id, article_title=data.get("title", ""),
            article_url=data.get("url", ""), article_source=data.get("source", ""),
            article_summary=data.get("summary", ""), article_category=data.get("category", "")
        )
        db.add(bm)
        db.commit()
        return {"status": "ok", "id": bm.id}
    except Exception as e:
        db.rollback()
        raise HTTPException(500, str(e))
    finally:
        db.close()

@app.get("/api/bookmarks")
async def get_bookmarks(request: Request):
    user = getattr(request.state, "user", None)
    if not user:
        return []
    db = next(get_db())
    try:
        bms = db.query(Bookmark).filter(Bookmark.user_id == user.user_id).order_by(Bookmark.saved_at.desc()).all()
        return [{"id": b.id, "title": b.article_title, "url": b.article_url, "source": b.article_source, "category": b.article_category, "summary": b.article_summary[:200], "saved_at": b.saved_at.isoformat() if b.saved_at else ""} for b in bms]
    finally:
        db.close()

@app.delete("/api/bookmarks/{bookmark_id}")
async def delete_bookmark(bookmark_id: int, request: Request):
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(401)
    db = next(get_db())
    try:
        bm = db.query(Bookmark).filter(Bookmark.id == bookmark_id, Bookmark.user_id == user.user_id).first()
        if bm:
            db.delete(bm)
            db.commit()
        return {"status": "ok"}
    finally:
        db.close()

@app.post("/api/chat")
async def chat(request: Request, data: dict):
    question = data.get("question", "").strip()
    if not question:
        return {"answer": "Please ask a question!", "sources": []}
    db = next(get_db())
    try:
        articles = get_articles_for_rag(db)
        articles_dicts = [{"id": str(a.id), "title": a.title, "url": a.url, "source": a.source, "summary": a.summary, "category": a.category} for a in articles]
        result = rag_engine.query(question, articles_dicts)
        return result
    finally:
        db.close()

@app.post("/api/agent")
async def agent_chat(request: Request, data: dict):
    question = data.get("question", "").strip()
    if not question:
        return {"response": "Ask me anything about the news!"}
    user = getattr(request.state, "user", None)
    result = agent_orchestrator.process(question, {"user": user.username if user else "anonymous"})
    return result

@app.get("/api/search/vector")
async def vector_search(q: str = Query(""), category: str = ""):
    if not q:
        return []
    results = vector_store.search(q, n_results=20)
    if category:
        results = [r for r in results if r.get("category", "").lower() == category.lower()]
    return results

@app.get("/api/categories")
async def get_categories():
    db = next(get_db())
    try:
        cats = db.query(NewsArticle.category).distinct().all()
        counts = {}
        for (c,) in cats:
            if c:
                count = db.query(NewsArticle).filter(NewsArticle.category == c).count()
                counts[c] = count
        return [{"name": k, "count": v} for k, v in sorted(counts.items(), key=lambda x: -x[1])]
    finally:
        db.close()

@app.get("/api/stats")
async def get_stats():
    db = next(get_db())
    try:
        total_articles = db.query(NewsArticle).count()
        total_categories = db.query(NewsArticle.category).distinct().count()
        total_users = db.query(User).count()
        return {
            "articles": total_articles,
            "categories": total_categories,
            "users": total_users,
            "embeddings": vector_store.count(),
            "current_country": CURRENT_COUNTRY,
            "last_fetch": LAST_FETCH_STATUS
        }
    finally:
        db.close()

@app.post("/api/fetch-news")
async def fetch_news(request: Request, data: dict = None):
    """Fetch news - no authentication required so anyone can trigger."""
    country = "US"
    if data and isinstance(data, dict):
        country = data.get("country", "US")
    # Validate country
    valid_countries = list(enterprise_config.COUNTRIES.keys())
    if country not in valid_countries:
        country = "US"
    
    thread = threading.Thread(target=run_news_fetch, kwargs={"country": country}, daemon=True)
    thread.start()
    return {
        "status": "started",
        "message": f"News fetch started for {country} in background",
        "country": country
    }

@app.get("/api/fetch-status")
async def fetch_status():
    """Return the current fetch status with details."""
    return LAST_FETCH_STATUS

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    WEBSOCKET_CLIENTS.add(websocket)
    try:
        await websocket.send_json(LAST_FETCH_STATUS)
        while True:
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_text("pong")
    except WebSocketDisconnect:
        pass
    except Exception:
        pass
    finally:
        WEBSOCKET_CLIENTS.discard(websocket)

@app.get("/api/countries")
async def get_countries():
    """Return list of available countries for news filtering."""
    countries = []
    for name, info in enterprise_config.COUNTRIES.items():
        countries.append({
            "name": name,
            "code": info.get("code", ""),
            "display": info.get("name", name)
        })
    return sorted(countries, key=lambda c: (c["name"] != "Global", c["name"]))

# ==== NEWS FETCHING ENGINE ====

def sync_enterprise_to_main(country: str = "Global", pipeline_result: dict = None):
    """Sync articles from enterprise engine DB to main app DB.
    The pipeline handles country filtering at fetch time."""
    global LAST_FETCH_STATUS
    db = SessionLocal()
    try:
        # Handle pipeline failure
        if pipeline_result and pipeline_result.get("status") == "failed":
            logger.error(f"[Sync] Pipeline failed: {pipeline_result.get('error', 'Unknown error')}")
            return 0, 0, 0
        
        fetched_count = pipeline_result.get("fetched", 0) if pipeline_result else 0
        curated_count = pipeline_result.get("curated", 0) if pipeline_result else 0
        total_saved = 0
        
        try:
            ee_session = get_session()
            # Get latest articles from enterprise DB (pipeline already filters by country at fetch time)
            ee_articles = get_latest_articles(ee_session, limit=200)
            
            for ee_article in ee_articles:
                try:
                    url = ee_article.url
                    if not url:
                        continue
                    existing = db.query(NewsArticle).filter(NewsArticle.url == url).first()
                    if not existing:
                        industry = ee_article.industry_tags[0] if ee_article.industry_tags else "General"
                        summary = ee_article.summary or ""
                        article = NewsArticle(
                            title=ee_article.title,
                            url=url,
                            source=ee_article.source or "Enterprise Engine",
                            category=industry,
                            summary=summary[:500],
                            content=(ee_article.summary or "")[:2000],
                            published=str(ee_article.published)[:19] if ee_article.published else "",
                            score=max(1.0, float(ee_article.final_score or 0) * 10)
                        )
                        db.add(article)
                        db.flush()
                        try:
                            vector_store.add_article(
                                str(article.id), ee_article.title, summary, summary,
                                {"category": industry, "url": url, "source": ee_article.source or ""}
                            )
                        except Exception as ve:
                            logger.debug(f"Vector store error: {ve}")
                        total_saved += 1
                except Exception as e:
                    logger.debug(f"EE save error: {e}")
            ee_session.close()
        except Exception as e:
            logger.debug(f"EE DB sync error: {e}")
        
        db.commit()
        
        if pipeline_result:
            msg = f"Fetch complete for {country}: {fetched_count} fetched, {total_saved} new articles saved"
            logger.info(f"[Pipeline] {msg}")
            LAST_FETCH_STATUS = {
                "status": "completed",
                "message": msg,
                "time": datetime.now(timezone.utc).isoformat(),
                "details": {
                    "country": country,
                    "fetched": fetched_count,
                    "saved": total_saved,
                    "curated": curated_count,
                    "insights": pipeline_result.get("insights", []),
                    "alerts": pipeline_result.get("alerts_list", []),
                }
            }
        return fetched_count, curated_count, total_saved
    except Exception as e:
        logger.error(f"[Sync] Main DB save failed: {e}")
        db.rollback()
        LAST_FETCH_STATUS = {
            "status": "error",
            "message": f"Save failed: {str(e)}",
            "time": datetime.now(timezone.utc).isoformat()
        }
        return 0, 0, 0
    finally:
        db.close()


_fetch_lock = threading.Lock()

def run_news_fetch(country: str = "Global"):
    """Run news fetch using config.yaml sources directly. Sets timeout via watchdog."""
    global CURRENT_COUNTRY, LAST_FETCH_STATUS
    
    if not _fetch_lock.acquire(blocking=False):
        logger.warning("[Fetch] Already running, skipping duplicate fetch")
        return {"country": country, "fetched": 0, "saved": 0, "skipped": True}
    
    try:
        CURRENT_COUNTRY = country
        LAST_FETCH_STATUS = {"status": "running", "message": f"Fetching news for {country}...", "time": datetime.now(timezone.utc).isoformat()}
        
        import time as _time
        start_ts = _time.time()
        MAX_FETCH_SECONDS = 120
        
        cfg = load_config()
        from src.sources import SourceFetcher
        fetcher = SourceFetcher(cfg)
        from src.curator import CuratorAgent
        curator = CuratorAgent(cfg)
        
        domains = cfg.get("domains", {})
        total_fetched = 0
        total_saved = 0
        
        for domain_name, domain_config in domains.items():
            if _time.time() - start_ts > MAX_FETCH_SECONDS:
                logger.warning(f"[Fetch] Timeout reached after {domain_name}, stopping")
                break
            if not domain_config.get("enabled", True):
                continue
            keywords = domain_config.get("keywords", [])
            sources = domain_config.get("sources", [])
            if not sources:
                continue
            
            try:
                items = fetcher.fetch_all(sources)
                curated = curator.curate(items, keywords)
                total_fetched += len(items)
            except Exception as e:
                logger.warning(f"[Fetch] Domain {domain_name} failed: {e}")
                continue
            
            db = SessionLocal()
            try:
                domain_saved = 0
                for item in curated:
                    if _time.time() - start_ts > MAX_FETCH_SECONDS:
                        break
                    try:
                        url = item.url if hasattr(item, "url") else ""
                        if not url:
                            continue
                        existing = db.query(NewsArticle).filter(NewsArticle.url == url).first()
                        if existing:
                            continue
                        title = item.title if hasattr(item, "title") else ""
                        summary = item.summary if hasattr(item, "summary") else ""
                        source = item.source if hasattr(item, "source") else domain_name
                        published = item.published if hasattr(item, "published") else ""
                        article = NewsArticle(
                            title=str(title)[:300],
                            url=str(url),
                            source=str(source)[:100],
                            category=domain_name,
                            summary=str(summary)[:500],
                            content=str(summary)[:2000],
                            published=str(published)[:19] if published else datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
                            score=5.0
                        )
                        db.add(article)
                        db.flush()
                        try:
                            vector_store.add_article(
                                str(article.id), str(title), str(summary), str(summary),
                                {"category": domain_name, "url": str(url), "source": str(source)}
                            )
                        except Exception:
                            pass
                        total_saved += 1
                    except Exception as e:
                        logger.debug(f"[Fetch] Save error: {e}")
                db.commit()
            except Exception as e:
                db.rollback()
                logger.warning(f"[Fetch] DB error for {domain_name}: {e}")
            finally:
                db.close()
        
        elapsed = _time.time() - start_ts
        msg = f"Fetch complete: {total_fetched} fetched, {total_saved} new articles saved in {elapsed:.0f}s"
        LAST_FETCH_STATUS = {
            "status": "completed",
            "message": msg,
            "time": datetime.now(timezone.utc).isoformat(),
            "details": {"country": country, "fetched": total_fetched, "saved": total_saved, "elapsed_sec": round(elapsed)}
        }
        return {"country": country, "fetched": total_fetched, "saved": total_saved}
    except Exception as e:
        logger.error(f"[Fetch] Error: {e}")
        LAST_FETCH_STATUS = {"status": "error", "message": f"Fetch error: {str(e)}", "time": datetime.now(timezone.utc).isoformat()}
        return None
    finally:
        _fetch_lock.release()


def delayed_initial_fetch():
    import time as _time
    _time.sleep(10)
    logger.info("[Startup] Running initial news fetch...")
    try:
        result = run_news_fetch(country="Global")
        if result:
            fetched = result.get("fetched", 0) or 0
            saved = result.get("saved", 0)
            logger.info(f"[Startup] Initial fetch complete: {fetched} fetched, {saved} saved")
        try:
            asyncio.run(broadcast_status())
        except Exception:
            pass
    except Exception as e:
        logger.warning(f"[Startup] Initial fetch failed (non-fatal): {e}")

async def broadcast_status():
    msg = json.dumps(LAST_FETCH_STATUS)
    dead = set()
    for ws in WEBSOCKET_CLIENTS:
        try:
            await ws.send_text(msg)
        except:
            dead.add(ws)
    WEBSOCKET_CLIENTS.difference_update(dead)

def run_news_fetch_with_notify(country: str = "Global"):
    """Run fetch and send notifications on completion."""
    result = run_news_fetch(country)
    if result and result.get("saved", 0) > 0:
        try:
            db = SessionLocal()
            try:
                recent = db.query(NewsArticle).order_by(NewsArticle.score.desc()).limit(10).all()
                headlines = "\n".join([f"• {a.title}" for a in recent[:10]])
            finally:
                db.close()
            summary = (
                f"NovaPulse AI - Daily News Update\n"
                f"Country: {country}\n"
                f"Articles fetched: {result.get('fetched', 0)}\n"
                f"New articles saved: {result.get('saved', 0)}\n\n"
                f"Top Headlines:\n{headlines}\n\n"
                f"View full news at: http://localhost:8000"
            )
            notif_results = send_notifications(
                f"Daily News Update - {country}",
                summary
            )
            log_msg = []
            if notif_results.get("email"): log_msg.append("email sent")
            if notif_results.get("whatsapp"): log_msg.append("whatsapp sent")
            if log_msg:
                logger.info(f"Notifications: {', '.join(log_msg)}")
        except Exception as e:
            logger.warning(f"Notification send failed (non-fatal): {e}")
    return result



# ==== SCHEDULE & NOTIFICATION SETTINGS ====

@app.get("/api/schedule")
async def get_schedule():
    """Get current schedule configuration."""
    sched_cfg = load_schedule_config()
    job = scheduler.get_job("news_fetch_every_2h")
    sched_cfg["active"] = job is not None
    if job and job.next_run_time:
        sched_cfg["next_run"] = job.next_run_time.isoformat()
        sched_cfg["next_run_display"] = job.next_run_time.strftime("%d %b %Y, %H:%M UTC")
    return sched_cfg


@app.post("/api/schedule")
async def set_schedule(data: dict):
    """Set schedule configuration."""
    from apscheduler.triggers.interval import IntervalTrigger
    enabled = data.get("enabled", True)
    interval_minutes = int(data.get("interval_minutes", 35))

    cfg = {"enabled": enabled, "interval_minutes": interval_minutes, "timezone": "UTC"}
    save_schedule_config(cfg)

    if enabled:
        scheduler.add_job(
            run_news_fetch_with_notify,
            trigger=IntervalTrigger(minutes=interval_minutes, jitter=1500),
            id="news_fetch_every_2h",
            replace_existing=True,
            kwargs={"country": CURRENT_COUNTRY}
        )
        logger.info(f"Schedule updated: every {interval_minutes} min ±25 min jitter")
        return {"status": "ok", "message": f"Fetching news every {interval_minutes} minutes (10-60m window)", "active": True}
    else:
        job = scheduler.get_job("news_fetch_every_2h")
        if job:
            job.remove()
            logger.info("Scheduler disabled")
        return {"status": "ok", "message": "Schedule disabled", "active": False}


@app.get("/api/notifications")
async def get_notifications():
    """Get current notification configuration (sanitized - no passwords)."""
    cfg = load_notif_config()
    return {
        "email": {
            "enabled": cfg.get("email", {}).get("enabled", False),
            "from_email": cfg.get("email", {}).get("from_email", ""),
            "to_email": cfg.get("email", {}).get("to_email", ""),
            "smtp_server": cfg.get("email", {}).get("smtp_server", "smtp.gmail.com"),
            "smtp_port": cfg.get("email", {}).get("smtp_port", 587),
            "subject_prefix": cfg.get("email", {}).get("subject_prefix", "[NovaPulse AI]"),
            "password_configured": bool(cfg.get("email", {}).get("password", ""))
        },
        "whatsapp": {
            "enabled": cfg.get("whatsapp", {}).get("enabled", False),
            "from_number": cfg.get("whatsapp", {}).get("from_number", ""),
            "to_number": cfg.get("whatsapp", {}).get("to_number", ""),
            "credentials_configured": bool(cfg.get("whatsapp", {}).get("account_sid", "")) and bool(cfg.get("whatsapp", {}).get("auth_token", ""))
        }
    }


@app.post("/api/notifications")
async def set_notifications(data: dict):
    """Update notification configuration."""
    cfg = load_notif_config()
    channel = data.get("channel", "")

    if channel == "email":
        email_cfg = cfg.setdefault("email", {})
        if "enabled" in data: email_cfg["enabled"] = data["enabled"]
        if "from_email" in data and data["from_email"]: email_cfg["from_email"] = data["from_email"]
        if "password" in data and data["password"]: email_cfg["password"] = data["password"]
        if "to_email" in data and data["to_email"]: email_cfg["to_email"] = data["to_email"]
        if "smtp_server" in data: email_cfg["smtp_server"] = data["smtp_server"]
        if "smtp_port" in data: email_cfg["smtp_port"] = int(data["smtp_port"])
        if "subject_prefix" in data: email_cfg["subject_prefix"] = data["subject_prefix"]
        save_notif_config(cfg)
        return {"status": "ok", "message": "Email notifications updated"}

    elif channel == "whatsapp":
        wa_cfg = cfg.setdefault("whatsapp", {})
        if "enabled" in data: wa_cfg["enabled"] = data["enabled"]
        if "account_sid" in data and data["account_sid"]: wa_cfg["account_sid"] = data["account_sid"]
        if "auth_token" in data and data["auth_token"]: wa_cfg["auth_token"] = data["auth_token"]
        if "from_number" in data: wa_cfg["from_number"] = data["from_number"]
        if "to_number" in data: wa_cfg["to_number"] = data["to_number"]
        save_notif_config(cfg)
        return {"status": "ok", "message": "WhatsApp notifications updated"}
    else:
        # Save both
        updated = False
        if "email" in data:
            for k, v in data["email"].items():
                cfg.setdefault("email", {})[k] = v
            updated = True
        if "whatsapp" in data:
            for k, v in data["whatsapp"].items():
                cfg.setdefault("whatsapp", {})[k] = v
            updated = True
        if updated:
            save_notif_config(cfg)
        return {"status": "ok", "message": "Notifications updated"}


@app.post("/api/notifications/test")
async def test_notifications_api(data: dict):
    """Send a test notification."""
    channel = data.get("channel", "email")
    result = test_notification(channel)
    return result


# ==== TOOLS CATALOG ROUTES ====

def _generate_tool_tags(t: dict) -> list:
    kw_map = {"AI":"ai","ML":"machine-learning","LLM":"llm","agent":"agent","RAG":"rag","vector":"vector","database":"database","search":"search","framework":"framework","workflow":"workflow","automation":"automation","code":"coding","API":"api","analytics":"analytics","monitor":"monitoring","security":"security","auth":"authentication","deploy":"deployment","backend":"backend","frontend":"frontend","visual":"visual","no-code":"no-code","open-source":"open-source","self-host":"self-hosted"}
    tags = set()
    cat = t.get("category","").lower()
    if "ai" in cat or "machine" in cat: tags.add("ai")
    if "developer" in cat: tags.add("developer-tools")
    if "data" in cat: tags.add("data")
    if "security" in cat: tags.add("security")
    if "infrastructure" in cat: tags.add("devops")
    if "productivity" in cat: tags.add("productivity")
    desc = t.get("description","").lower()
    for word, tag in kw_map.items():
        if word.lower() in desc: tags.add(tag)
    name = t.get("name","").lower()
    if any(x in name for x in ["ai","gpt","llm","agent","gen","intelli"]): tags.add("ai")
    return list(tags)[:4]

def _get_tool_type(t: dict) -> str:
    cat = t.get("category","").lower()
    name = t.get("name","").lower()
    desc = t.get("description","").lower()
    if any(x in cat or x in name or x in desc for x in ["video","conferenc","stream","media server","screen record"]): return "Video"
    if any(x in cat or x in name or x in desc for x in ["image","photo","design","creative","3d","blender","gimp","inkscape","penpot"]): return "Image"
    if any(x in cat or x in name or x in desc for x in ["code","ide","developer tool","git","orm","build","frontend","vite","editor"]): return "Coding"
    if any(x in cat or x in name or x in desc for x in ["ai","machine learning","llm","ml","rag","agent","vector","chatbot","language model"]): return "AI"
    if any(x in cat or x in name or x in desc for x in ["data","analytics","database","bi ","sql","column"]): return "Data"
    if any(x in cat or x in name or x in desc for x in ["monitor","observ","prometheus","grafana","sentry","open-telemetry"]): return "Monitoring"
    if any(x in cat or x in name or x in desc for x in ["devops","ci/cd","deploy","container","kubernetes","docker","terraform"]): return "DevOps"
    if any(x in cat or x in name or x in desc for x in ["security","auth","password","privacy","keycloak","bitwarden"]): return "Security"
    if any(x in cat or x in name or x in desc for x in ["cms","blog","publishing","ghost","wordpress","strapi"]): return "CMS"
    if any(x in cat or x in name or x in desc for x in ["crm","erp","finance","payment","invoice","billing"]): return "Business"
    if any(x in cat or x in name or x in desc for x in ["note","doc","wiki","knowledge","logseq","joplin","outline","affine"]): return "Docs"
    if any(x in cat or x in name or x in desc for x in ["message","chat","communic","slack","mattermost","rocket"]): return "Chat"
    if any(x in cat or x in name or x in desc for x in ["automation","workflow","no-code","low-code","n8n"]): return "Automation"
    if any(x in cat or x in name or x in desc for x in ["backend","baas","firebase","supabase","storage","hosting"]): return "Backend"
    if any(x in cat or x in name or x in desc for x in ["form","survey","typebot","formbrick"]): return "Forms"
    if any(x in cat or x in name or x in desc for x in ["project","jira","linear","plane","focalboard","taiga"]): return "Project Mgmt"
    return "Tool"

def _get_install_cmd(t: dict) -> str:
    name = t.get("name","").lower()
    desc = t.get("description","").lower()
    cat = t.get("category","").lower()
    github = t.get("github","")
    if any(x in name or x in desc for x in ["ollama","run llms locally","local llm"]): return "ollama pull llama3.2"
    if any(x in name or x in desc for x in ["docker","container"]): return "docker pull " + name.replace(" ","").lower()
    if any(x in name or x in desc for x in ["pip","python","mlflow","transformers","hugging face"]): return "pip install " + ("transformers" if "hugging" in name else name.lower().replace(" ","-"))
    if any(x in name or x in desc for x in ["npm","node","vite","prisma","drizzle","vscodium","vite"]): return "npm install -g " + name.lower().replace(" ","-")
    if any(x in name or x in desc for x in ["brew","homebrew"]): return "brew install " + name.lower().replace(" ","")
    if any(x in name or x in desc for x in ["git","devops","ci/cd","gitea","gitlab"]): return "git clone https://github.com/" + github if github else "Visit website to install"
    if "kubernetes" in name: return "kubectl apply -f https://raw.githubusercontent.com/kubernetes/master/deploy/manifests"
    if "postgresql" in name: return "brew install postgresql@16"
    if "redis" in name: return "brew install redis"
    if "clickhouse" in name: return "curl https://clickhouse.com/ | sh"
    if "wordpress" in name: return "docker run --name wp -e WORDPRESS_DB_HOST=db -d wordpress"
    if "keycloak" in name: return "docker run -p 8080:8080 -e KEYCLOAK_ADMIN=admin -e KEYCLOAK_ADMIN_PASSWORD=admin quay.io/keycloak/keycloak:latest start-dev"
    if "grafana" in name: return "docker run -d -p 3000:3000 grafana/grafana"
    if "prometheus" in name: return "docker run -d -p 9090:9090 prom/prometheus"
    if any(x in cat for x in ["backend","baas","hosting","infrastructure"]): return "docker run -d -p 8080:80 " + name.lower().replace(" ","")
    return "docker pull " + name.lower().replace(" ","") if not github else "Visit " + t.get("url","website") + " to install"

def build_tools_data():
    """Build tools data with icons and accent classes for template rendering."""
    tools = []
    for t in AI_TOOLS_CATALOG["tools"]:
        cat = t["category"]
        tools.append({
            "name": t["name"],
            "description": t["description"],
            "category": cat,
            "icon": CATEGORY_ICONS.get(cat, "🔧"),
            "accent_class": CATEGORY_ACCENTS.get(cat, "blue"),
            "tags": t["tags"],
            "url": t["url"],
            "stars": t["stars"],
            "forks": t["forks"],
            "openSource": t["openSource"],
            "alternativeTo": t.get("alternativeTo", []),
            "featured": t.get("featured", False)
        })
    return tools

def build_categories_data():
    """Build categories with counts."""
    cat_counts = {}
    for t in AI_TOOLS_CATALOG["tools"]:
        cat = t["category"]
        cat_counts[cat] = cat_counts.get(cat, 0) + 1
    cats = []
    for cat in AI_TOOLS_CATALOG["categories"]:
        name = cat["name"]
        cats.append({
            "name": name,
            "icon": cat["icon"],
            "description": cat["description"],
            "color": cat["color"],
            "count": cat_counts.get(name, 0)
        })
    return cats

@app.get("/tools", response_class=HTMLResponse)
async def tools_page(request: Request):
    tools = build_tools_data()
    categories = build_categories_data()
    open_source_count = sum(1 for t in tools if t["openSource"])
    featured_count = sum(1 for t in tools if t["featured"])
    return render("tools.html", request=request, tools=tools, categories=categories, open_source_count=open_source_count, featured_count=featured_count)

@app.get("/api/tools")
async def get_tools(category: str = "", search: str = "", sort: str = "stars"):
    tools = build_tools_data()
    if category:
        tools = [t for t in tools if t["category"] == category]
    if search:
        q = search.lower()
        tools = [t for t in tools if q in t["name"].lower() or q in t["description"].lower() or any(q in tag.lower() for tag in t["tags"])]
    if sort == "name":
        tools.sort(key=lambda t: t["name"])
    elif sort == "featured":
        tools.sort(key=lambda t: (0 if t["featured"] else 1, -t["stars"]))
    else:
        tools.sort(key=lambda t: -t["stars"])
    return tools

@app.get("/api/tools/categories")
async def get_tools_categories():
    return build_categories_data()

# ==== OPENALTERNATIVE ROUTES ====

@app.get("/oa", response_class=HTMLResponse)
async def oa_home_page(request: Request):
    data = OPENALTERNATIVE_DATA["advertise"]
    cats = OPENALTERNATIVE_DATA["categories"]
    popular = OPENALTERNATIVE_DATA["popular_alternatives"]
    popular_sw = OPENALTERNATIVE_DATA["popular_software_list"]
    popular_cats = OPENALTERNATIVE_DATA["popular_categories_list"]
    tags = OPENALTERNATIVE_DATA["tags"]
    licenses = OPENALTERNATIVE_DATA["licenses"]
    codes = OPENALTERNATIVE_DATA["discount_codes"]
    sh_count = len(OPENALTERNATIVE_DATA["self_hosted_tools"])
    all_tools = OPENALTERNATIVE_DATA["tools"]
    for t in all_tools:
        t["icon"] = {"AI & Machine Learning":"🤖","Business Software":"💼","Community & Social":"👥","Content & Publishing":"📝","Data & Analytics":"📊","Developer Tools":"🛠️","Infrastructure & Operations":"☁️","Miscellaneous":"📦","Productivity & Utilities":"⚡","Security & Privacy":"🔒"}.get(t.get("category",""),"🔧")
    popular_tools = sorted(all_tools, key=lambda t: -t.get("stars",0))[:20]
    return render("openalt_home.html", request=request,
        data=data, categories=cats, popular_alternatives=popular,
        popular_software_list=popular_sw, popular_categories_list=popular_cats,
        tags=tags, licenses=licenses, codes=codes, self_hosted_count=sh_count, popular_tools=popular_tools)

@app.get("/browse", response_class=HTMLResponse)
async def browse_page(request: Request):
    tools = OPENALTERNATIVE_DATA["tools"]
    cats = OPENALTERNATIVE_DATA["categories"]
    popular = OPENALTERNATIVE_DATA["popular_alternatives"]
    for t in tools:
        t["icon"] = {"AI & Machine Learning":"🤖","Business Software":"💼","Community & Social":"👥","Content & Publishing":"📝","Data & Analytics":"📊","Developer Tools":"🛠️","Infrastructure & Operations":"☁️","Miscellaneous":"📦","Productivity & Utilities":"⚡","Security & Privacy":"🔒"}.get(t.get("category",""),"🔧")
        u = t.get("url", "")
        t["domain"] = u.replace("https://","").replace("http://","").split("/")[0] if u else ""
        g = t.get("github", "")
        t["github_owner"] = g.split("/")[0] if g else ""
        t["github_img"] = f"https://github.com/{g.split('/')[0]}.png?size=64" if g else ""
        t["tags"] = _generate_tool_tags(t)
        t["tool_type"] = _get_tool_type(t)
        t["install_cmd"] = _get_install_cmd(t)
    return render("openalt_browse.html", request=request, tools=tools, categories=cats, popular=popular)

@app.get("/alternatives", response_class=HTMLResponse)
async def alternatives_page(request: Request):
    alternatives = OPENALTERNATIVE_DATA["popular_alternatives"]
    return render("openalt_alternatives.html", request=request, alternatives=alternatives)

@app.get("/categories", response_class=HTMLResponse)
async def open_categories_page(request: Request):
    return render("openalt_categories.html", request=request, categories=OPENALTERNATIVE_DATA["categories"])

@app.get("/tech-stacks", response_class=HTMLResponse)
async def tech_stacks_page(request: Request):
    return render("openalt_techstacks.html", request=request, categories=OPENALTERNATIVE_DATA["categories"], tags=OPENALTERNATIVE_DATA["tags"])

@app.get("/self-hosted", response_class=HTMLResponse)
async def self_hosted_page(request: Request):
    tools = OPENALTERNATIVE_DATA["self_hosted_tools"]
    cat_filter = request.query_params.get("category", "")
    if cat_filter:
        tools = [t for t in tools if t["category"].lower() == cat_filter.lower()]
    page = int(request.query_params.get("page", 1))
    per_page = 50
    total_pages = max(1, (len(tools) + per_page - 1) // per_page)
    page = max(1, min(page, total_pages))
    start = (page - 1) * per_page
    end = start + per_page
    page_tools = tools[start:end]
    for t in page_tools:
        g = t.get("github", "")
        t["github_owner"] = g.split("/")[0] if g else ""
        t["github_img"] = f"https://github.com/{g.split('/')[0]}.png?size=64" if g else ""
        t["tags"] = _generate_tool_tags(t)
    return render("openalt_selfhosted.html", request=request, tools=page_tools, categories=OPENALTERNATIVE_DATA["categories"], page=page, total_pages=total_pages)

@app.get("/advertise", response_class=HTMLResponse)
async def advertise_page(request: Request):
    data = OPENALTERNATIVE_DATA["advertise"]
    return render("openalt_advertise.html", request=request, data=data)

@app.get("/tags", response_class=HTMLResponse)
async def tags_page(request: Request):
    tags = sorted(OPENALTERNATIVE_DATA["tags"], key=lambda t: t["count"], reverse=True)
    return render("openalt_tags.html", request=request, tags=tags)

@app.get("/licenses", response_class=HTMLResponse)
async def licenses_page(request: Request):
    licenses = sorted(OPENALTERNATIVE_DATA["licenses"], key=lambda l: l["count"], reverse=True)
    return render("openalt_licenses.html", request=request, licenses=licenses)

@app.get("/about", response_class=HTMLResponse)
async def about_page(request: Request):
    return render("openalt_about.html", request=request)

@app.get("/contact", response_class=HTMLResponse)
async def contact_page(request: Request):
    return render("openalt_contact.html", request=request)

@app.post("/contact")
async def contact_submit(request: Request):
    try:
        data = await request.json()
        name = data.get("name", "")
        email = data.get("email", "")
        message = data.get("message", "")
        logger.info(f"Contact form: {name} <{email}>: {message[:100]}")
        return {"status": "ok", "message": "Message sent successfully!"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/submit", response_class=HTMLResponse)
async def submit_page(request: Request):
    data = OPENALTERNATIVE_DATA["advertise"]
    cats = OPENALTERNATIVE_DATA["categories"]
    popular = OPENALTERNATIVE_DATA["popular_alternatives"]
    popular_sw = OPENALTERNATIVE_DATA["popular_software_list"]
    popular_cats = OPENALTERNATIVE_DATA["popular_categories_list"]
    tags = OPENALTERNATIVE_DATA["tags"]
    licenses = OPENALTERNATIVE_DATA["licenses"]
    codes = OPENALTERNATIVE_DATA["discount_codes"]
    sh_count = len(OPENALTERNATIVE_DATA["self_hosted_tools"])
    return render("openalt_submit.html", request=request,
        data=data, categories=cats, popular_alternatives=popular,
        popular_software_list=popular_sw, popular_categories_list=popular_cats,
        tags=tags, licenses=licenses, codes=codes, self_hosted_count=sh_count)

@app.post("/submit")
async def submit_tool(request: Request):
    try:
        data = await request.json()
        name = data.get("name", "")
        url = data.get("url", "")
        desc = data.get("description", "")
        logger.info(f"Tool submission: {name} ({url}): {desc[:100]}")
        return {"status": "ok", "message": "Tool submitted for review!"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/blog", response_class=HTMLResponse)
async def blog_page(request: Request):
    posts = OPENALTERNATIVE_DATA["blog_posts"]
    return render("openalt_blog.html", request=request, posts=posts)

@app.get("/blog/{slug}", response_class=HTMLResponse)
async def blog_post(request: Request, slug: str):
    posts = OPENALTERNATIVE_DATA["blog_posts"]
    post = next((p for p in posts if p["slug"] == slug), None)
    if not post:
        return HTMLResponse("Post not found", status_code=404)
    return render("openalt_blog_post.html", request=request, post=post)

@app.get("/discount-codes", response_class=HTMLResponse)
async def discount_codes_page(request: Request):
    codes = OPENALTERNATIVE_DATA["discount_codes"]
    return render("openalt_discounts.html", request=request, codes=codes)

@app.get("/subscribe", response_class=HTMLResponse)
async def subscribe_page(request: Request, plan: str = "silver"):
    plans = OPENALTERNATIVE_DATA["advertise"]["plans"]
    found = next((p for p in plans if p["name"].lower() == plan.lower()), plans[0])
    return render("openalt_subscribe.html", request=request, plan=found)

# Tool detail page
@app.get("/tool/{tool_name}", response_class=HTMLResponse)
async def tool_detail(request: Request, tool_name: str):
    tools = OPENALTERNATIVE_DATA["tools"] + OPENALTERNATIVE_DATA["self_hosted_tools"]
    tool = next((t for t in tools if t["name"].lower().replace(" ", "-") == tool_name.lower()), None)
    if not tool:
        return HTMLResponse("Tool not found", status_code=404)
    return render("openalt_tool.html", request=request, tool=tool)

# ==== MAIN ====

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8000"))
    print(f"""
{'='*60}
  NOVAPULSE AI - Next Generation AI News Platform
{'='*60}
  Server: http://localhost:{port}
  Features:
    • Apple Design System (iMac/iPad/iPhone)
    • JWT Authentication
    • RAG with ChromaDB Vector Store
    • AI Agent Orchestration (LangGraph pattern)
    • Semantic Search with Sentence Transformers
    • Multi-Source News Aggregation
    • Bookmarking & Reading History
    • AI Learning Hub
{'='*60}
""")
    uvicorn.run("main_v2:app", host="0.0.0.0", port=port, reload=False)
