import os
import json
import logging
import hashlib
from datetime import datetime
from typing import Dict, List, Any, Optional, Callable
from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig

logger = logging.getLogger("EnterpriseMCP")

class MCPToolRegistry:
    def __init__(self):
        self.tools: Dict[str, Dict] = {}
        self.langchain_tools = []

    def register(self, name: str, description: str, func: Callable,
                 parameters: dict = None, category: str = "general"):
        self.tools[name] = {
            "name": name,
            "description": description,
            "function": func,
            "parameters": parameters or {},
            "category": category,
        }
        @tool(name, description=description)
        def wrapped(**kwargs):
            return func(**kwargs)
        self.langchain_tools.append(wrapped)
        logger.info(f"[MCP] Registered tool: {name}")

    def get_schema(self, name: str) -> Optional[dict]:
        t = self.tools.get(name)
        if not t:
            return None
        return {
            "name": t["name"],
            "description": t["description"],
            "input_schema": {
                "type": "object",
                "properties": t["parameters"],
            },
        }

    def execute(self, name: str, **kwargs) -> Any:
        t = self.tools.get(name)
        if not t:
            return {"error": f"Tool '{name}' not found"}
        try:
            return t["function"](**kwargs)
        except Exception as e:
            logger.error(f"[MCP] Tool '{name}' failed: {e}")
            return {"error": str(e)}

    def list_tools(self) -> List[dict]:
        return [
            {"name": n, "description": t["description"], "category": t["category"]}
            for n, t in self.tools.items()
        ]

    def get_langchain_tools(self):
        return self.langchain_tools

mcp_registry = MCPToolRegistry()

def register_core_tools(fetcher, vector_store, rag_engine):
    @tool("fetch_latest_news", "Fetch latest news articles from all sources with optional country filter")
    def fetch_latest_news(country: str = "Global", max_sources: int = 5) -> List[dict]:
        articles = fetcher.fetch_all(country=country)
        return articles[:max_sources * 20]

    @tool("vector_search_news", "Semantic search across indexed news articles")
    def vector_search_news(query: str, k: int = 10) -> List[dict]:
        return vector_store.search(query, k=k)

    @tool("get_ai_insights", "Get AI-powered insights and analysis on news articles")
    def get_ai_insights(question: str, industry: str = None) -> dict:
        return rag_engine.ask(question, industry=industry)

    @tool("search_trending_topics", "Get currently trending topics in tech")
    def search_trending_topics() -> List[str]:
        results = vector_store.search("trending technology news today", k=20)
        topics = set()
        for r in results:
            title = r.get("title", "")
            tags = r.get("industry_tags", [])
            if tags:
                topics.update(tags[:3])
            words = [w for w in title.split() if len(w) > 5][:2]
            topics.update(words)
        return list(topics)[:10]

    @tool("search_by_industry", "Search news articles filtered by industry sector")
    def search_by_industry(industry: str, k: int = 10) -> List[dict]:
        return vector_store.search_by_industry(industry, k=k)

    mcp_registry.register("fetch_latest_news", "Fetch latest news from all sources", fetch_latest_news,
                          {"country": {"type": "string"}, "max_sources": {"type": "integer"}}, "news")
    mcp_registry.register("vector_search", "Semantic search across news articles", vector_search_news,
                          {"query": {"type": "string"}, "k": {"type": "integer"}}, "search")
    mcp_registry.register("ai_insights", "Get AI insights on news topics", get_ai_insights,
                          {"question": {"type": "string"}, "industry": {"type": "string"}}, "ai")
    mcp_registry.register("trending_topics", "Get trending tech topics", search_trending_topics, {}, "analytics")
    mcp_registry.register("industry_search", "Search news by industry", search_by_industry,
                          {"industry": {"type": "string"}, "k": {"type": "integer"}}, "search")
