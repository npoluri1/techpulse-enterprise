import os
import json
import logging
import asyncio
from datetime import datetime
from typing import Optional

from enterprise_engine.config import config
from enterprise_engine.sources import FreeSourceFetcher
from enterprise_engine.vector_store import FreeVectorStore
from enterprise_engine.rag_engine import FreeRAGEngine
from enterprise_engine.agents import CurationAgent, ReportGenerator
from enterprise_engine.models import (init_db, get_session, save_article,
                                       save_alert, PipelineRun, get_pipeline_stats)
from enterprise_engine.industry_categories import get_all_industries

logger = logging.getLogger("EnterprisePipeline")


class EnterprisePipeline:
    def __init__(self):
        self.db_engine = init_db()
        self.fetcher = FreeSourceFetcher()
        self.vector_store = FreeVectorStore()
        self.rag = FreeRAGEngine(self.vector_store)
        self.curator = CurationAgent()
        self.reporter = ReportGenerator(self.rag)

    def run_full(self) -> dict:
        run_id = f"run_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        session = get_session()
        pipeline_run = PipelineRun(
            id=run_id,
            started_at=datetime.utcnow(),
            status="running",
        )
        session.add(pipeline_run)
        session.commit()

        try:
            logger.info(f"[Pipeline] {run_id} started")
            raw = self.fetcher.fetch_all()
            pipeline_run.articles_fetched = len(raw)
            logger.info(f"[Pipeline] Fetched {len(raw)} articles")

            curated = self.curator.curate(raw)
            pipeline_run.articles_curated = len(curated)
            logger.info(f"[Pipeline] Curated {len(curated)} articles")

            for article in curated:
                self.vector_store.index_article(article)
                save_article(session, article)
            session.commit()

            insights = self.rag.generate_insights(curated)
            alerts = self.curator.detect_alerts(curated)
            for alert in alerts:
                save_alert(session, alert)
            session.commit()
            pipeline_run.alerts_generated = len(alerts)

            stats = get_pipeline_stats(session)
            industries_covered = len(set(
                t for a in curated for t in a.get("industry_tags", [])
            ))
            stats["industries_covered"] = industries_covered

            markdown = self.reporter.generate_markdown(
                insights, alerts, len(curated), stats
            )
            mobile = self.reporter.generate_mobile_brief(insights)

            pipeline_run.status = "completed"
            pipeline_run.completed_at = datetime.utcnow()
            session.commit()

            result = {
                "run_id": run_id,
                "status": "completed",
                "fetched": len(raw),
                "curated": len(curated),
                "alerts": len(alerts),
                "insights": insights,
                "alerts_list": alerts,
                "markdown_report": markdown,
                "mobile_brief": mobile,
                "stats": stats,
            }
            logger.info(f"[Pipeline] {run_id} completed successfully")
            return result

        except Exception as e:
            pipeline_run.status = "failed"
            pipeline_run.error = str(e)
            pipeline_run.completed_at = datetime.utcnow()
            session.commit()
            logger.error(f"[Pipeline] {run_id} failed: {e}", exc_info=True)
            return {
                "run_id": run_id,
                "status": "failed",
                "error": str(e),
                "fetched": pipeline_run.articles_fetched,
                "curated": pipeline_run.articles_curated,
            }
        finally:
            session.close()
