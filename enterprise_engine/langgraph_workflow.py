import os
import json
import logging
from typing import Dict, List, Any, Optional, TypedDict, Annotated, Literal
from datetime import datetime, timezone
from langgraph.graph import StateGraph, END, START
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage, SystemMessage

from enterprise_engine.config import config
from enterprise_engine.sources import FreeSourceFetcher
from enterprise_engine.vector_store import FreeVectorStore
from enterprise_engine.rag_engine import FreeRAGEngine
from enterprise_engine.agents import CurationAgent, ReportGenerator
from enterprise_engine.mcp_tools import mcp_registry, register_core_tools

logger = logging.getLogger("LangGraphWorkflow")

class NewsPipelineState(TypedDict):
    country: str
    raw_articles: List[dict]
    curated_articles: List[dict]
    insights: dict
    alerts: list
    markdown_report: str
    mobile_brief: str
    stats: dict
    errors: List[str]
    stage: str
    summary: str

class NewsLangGraph:
    def __init__(self):
        self.fetcher = FreeSourceFetcher()
        self.vector_store = FreeVectorStore()
        self.rag = FreeRAGEngine(self.vector_store)
        self.curator = CurationAgent()
        self.reporter = ReportGenerator(self.rag)
        self.memory = MemorySaver()
        register_core_tools(self.fetcher, self.vector_store, self.rag)
        self.app = self._build_graph()

    def _fetch_node(self, state: NewsPipelineState) -> NewsPipelineState:
        logger.info(f"[LangGraph] Fetching news for {state.get('country', 'Global')}")
        try:
            articles = self.fetcher.fetch_all(country=state.get("country", "Global"))
            state["raw_articles"] = articles or []
            state["stage"] = "fetch_complete"
            logger.info(f"[LangGraph] Fetched {len(state['raw_articles'])} articles")
        except Exception as e:
            state["errors"] = state.get("errors", []) + [f"Fetch failed: {str(e)}"]
            state["stage"] = "fetch_failed"
        return state

    def _curate_node(self, state: NewsPipelineState) -> NewsPipelineState:
        raw = state.get("raw_articles", [])
        if not raw:
            logger.warning("[LangGraph] No articles to curate")
            state["curated_articles"] = []
            state["stage"] = "curate_empty"
            return state
        try:
            curated = self.curator.curate(raw)
            state["curated_articles"] = curated
            state["stage"] = "curate_complete"
            logger.info(f"[LangGraph] Curated {len(curated)} articles from {len(raw)} raw")
        except Exception as e:
            state["errors"] = state.get("errors", []) + [f"Curation failed: {str(e)}"]
            state["stage"] = "curate_failed"
        return state

    def _vectorize_node(self, state: NewsPipelineState) -> NewsPipelineState:
        articles = state.get("curated_articles", [])
        if not articles:
            state["stage"] = "vectorize_skipped"
            return state
        indexed = 0
        for article in articles:
            try:
                self.vector_store.index_article(article)
                indexed += 1
            except Exception as e:
                logger.debug(f"[LangGraph] Vectorize error: {e}")
        logger.info(f"[LangGraph] Vectorized {indexed} articles")
        state["stage"] = "vectorize_complete"
        return state

    def _analyze_node(self, state: NewsPipelineState) -> NewsPipelineState:
        articles = state.get("curated_articles", [])
        if not articles:
            state["stage"] = "analyze_skipped"
            return state
        try:
            insights = self.rag.generate_insights(articles)
            state["insights"] = insights
            alerts = self.curator.detect_alerts(articles)
            state["alerts"] = alerts
            state["stage"] = "analyze_complete"
            logger.info(f"[LangGraph] Generated insights + {len(alerts)} alerts")
        except Exception as e:
            state["errors"] = state.get("errors", []) + [f"Analysis failed: {str(e)}"]
            state["stage"] = "analyze_failed"
        return state

    def _report_node(self, state: NewsPipelineState) -> NewsPipelineState:
        insights = state.get("insights", {})
        alerts = state.get("alerts", [])
        articles = state.get("curated_articles", [])
        stats = {"industries_covered": len(set(
            t for a in articles for t in a.get("industry_tags", [])
        ))}
        try:
            md = self.reporter.generate_markdown(insights, alerts, len(articles), stats)
            mb = self.reporter.generate_mobile_brief(insights)
            state["markdown_report"] = md
            state["mobile_brief"] = mb
            state["stats"] = stats
            state["stage"] = "report_complete"
        except Exception as e:
            state["errors"] = state.get("errors", []) + [f"Report failed: {str(e)}"]
        return state

    def _should_continue(self, state: NewsPipelineState) -> Literal["continue", "skip", "end"]:
        errors = state.get("errors", [])
        if len(errors) > 3:
            logger.error(f"[LangGraph] Too many errors: {errors}")
            return "end"
        return "continue"

    def _build_graph(self) -> StateGraph:
        builder = StateGraph(NewsPipelineState)

        builder.add_node("fetch", self._fetch_node)
        builder.add_node("curate", self._curate_node)
        builder.add_node("vectorize", self._vectorize_node)
        builder.add_node("analyze", self._analyze_node)
        builder.add_node("report", self._report_node)

        builder.add_edge(START, "fetch")
        builder.add_conditional_edges("fetch", self._should_continue, {
            "continue": "curate", "skip": "curate", "end": END
        })
        builder.add_conditional_edges("curate", self._should_continue, {
            "continue": "vectorize", "skip": "vectorize", "end": END
        })
        builder.add_conditional_edges("vectorize", self._should_continue, {
            "continue": "analyze", "skip": "analyze", "end": END
        })
        builder.add_conditional_edges("analyze", self._should_continue, {
            "continue": "report", "skip": "report", "end": END
        })
        builder.add_edge("report", END)

        return builder.compile(checkpointer=self.memory)

    def run(self, country: str = "Global", thread_id: str = None) -> dict:
        thread_id = thread_id or f"news_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}"
        config_thread = {"configurable": {"thread_id": thread_id}}

        initial_state: NewsPipelineState = {
            "country": country,
            "raw_articles": [],
            "curated_articles": [],
            "insights": {},
            "alerts": [],
            "markdown_report": "",
            "mobile_brief": "",
            "stats": {},
            "errors": [],
            "stage": "start",
            "summary": f"News pipeline for {country}",
        }

        try:
            result = self.app.invoke(initial_state, config=config_thread)
            return {
                "status": "completed" if not result.get("errors") else "partial",
                "fetched": len(result.get("raw_articles", [])),
                "curated": len(result.get("curated_articles", [])),
                "alerts": len(result.get("alerts", [])),
                "insights": result.get("insights", {}),
                "alerts_list": result.get("alerts", []),
                "markdown_report": result.get("markdown_report", ""),
                "mobile_brief": result.get("mobile_brief", ""),
                "stats": result.get("stats", {}),
                "errors": result.get("errors", []),
                "stage": result.get("stage", ""),
            }
        except Exception as e:
            logger.error(f"[LangGraph] Pipeline failed: {e}", exc_info=True)
            return {
                "status": "failed",
                "error": str(e),
                "fetched": 0,
                "curated": 0,
                "alerts": 0,
                "insights": {},
                "alerts_list": [],
                "errors": [str(e)],
            }

news_langgraph = NewsLangGraph()
