import os
import json
import logging
from datetime import datetime
from typing import Optional

import uvicorn
from fastapi import FastAPI, BackgroundTasks, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from enterprise_engine.config import config
from enterprise_engine.pipeline import EnterprisePipeline
from enterprise_engine.models import init_db, get_session, get_top_articles, get_alerts, get_pipeline_stats
from enterprise_engine.vector_store import FreeVectorStore

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s")
logger = logging.getLogger("EnterpriseAPI")

app = FastAPI(title="Enterprise Tech Intelligence API", version="2.0.0",
              docs_url="/docs", redoc_url="/redoc")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pipeline = EnterprisePipeline()
vector_store = FreeVectorStore()


class ChatRequest(BaseModel):
    question: str
    industry: Optional[str] = None
    mode: str = "report"


class PipelineRunRequest(BaseModel):
    background: bool = True


@app.on_event("startup")
async def startup():
    init_db()
    logger.info("[API] Database initialized")


@app.get("/")
async def root():
    return {
        "name": "Enterprise Tech Intelligence API",
        "version": "2.0.0",
        "status": "running",
        "docs": "/docs",
        "free_tools": {
            "llm": f"Google Gemini ({config.LLM_MODEL})",
            "vector_db": "ChromaDB (local)",
            "embeddings": f"HuggingFace ({config.EMBEDDING_MODEL})",
            "database": "SQLite",
            "sources": "NewsAPI + RSS + Reddit + Serper",
        }
    }


@app.get("/health")
async def health():
    vs_stats = vector_store.get_stats()
    return {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat(),
        "vector_store": vs_stats,
    }


@app.post("/api/pipeline/run")
async def run_pipeline(req: PipelineRunRequest, background_tasks: BackgroundTasks):
    if req.background:
        background_tasks.add_task(pipeline.run_full)
        return {"status": "started", "message": "Pipeline running in background"}
    result = pipeline.run_full()
    return result


@app.get("/api/pipeline/latest")
async def get_latest(limit: int = Query(50, ge=1, le=200)):
    session = get_session()
    try:
        articles = get_top_articles(session, limit=limit)
        alerts = get_alerts(session, limit=20, unsent_only=True)
        stats = get_pipeline_stats(session)
        return {
            "articles": [
                {
                    "id": a.id,
                    "title": a.title,
                    "url": a.url,
                    "source": a.source,
                    "summary": a.summary[:200],
                    "industry_tags": a.industry_tags or [],
                    "final_score": a.final_score,
                    "funding_amount_usd": a.funding_amount_usd,
                    "category": a.category,
                    "published": str(a.published) if a.published else "",
                }
                for a in articles
            ],
            "alerts": [
                {
                    "type": al.type,
                    "severity": al.severity,
                    "headline": al.headline,
                    "body": al.body[:100],
                    "suggested_push_text": al.suggested_push_text,
                }
                for al in alerts
            ],
            "stats": {
                "total_articles": stats["total_articles"],
                "total_alerts": stats["total_alerts"],
                "avg_score": stats["avg_score"],
            },
        }
    finally:
        session.close()


@app.get("/api/insights/{industry:path}")
async def industry_insights(industry: str, k: int = Query(10, ge=1, le=50)):
    results = vector_store.search_by_industry(industry, k=k)
    if not results:
        raise HTTPException(status_code=404, detail=f"No articles found for '{industry}'")
    return {
        "industry": industry,
        "articles_count": len(results),
        "articles": results,
    }


@app.post("/api/chat")
async def chat(req: ChatRequest):
    if not req.question:
        raise HTTPException(status_code=400, detail="Question is required")
    result = pipeline.rag.ask(
        question=req.question,
        industry=req.industry,
    )
    return result


@app.get("/api/search")
async def search(q: str = Query(..., min_length=2),
                 k: int = Query(10, ge=1, le=50)):
    results = vector_store.search(q, k=k)
    return {
        "query": q,
        "count": len(results),
        "results": results,
    }


@app.get("/api/pipeline/stats")
async def stats():
    session = get_session()
    try:
        return get_pipeline_stats(session)
    finally:
        session.close()


@app.get("/api/industries")
async def list_industries():
    from enterprise_engine.industry_categories import get_all_industries
    return {"industries": get_all_industries(), "total": len(get_all_industries())}


@app.post("/api/pipeline/run-now")
async def run_now():
    result = pipeline.run_full()
    return result


def start():
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")


if __name__ == "__main__":
    start()
