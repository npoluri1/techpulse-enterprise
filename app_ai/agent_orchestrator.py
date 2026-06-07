import os
import logging
import json
from typing import Dict, List, Any, Optional, TypedDict

logger = logging.getLogger("NewsAI.Agent")

class AgentState(TypedDict):
    messages: List[Dict]
    actions: List[str]
    context: Dict
    next_step: str

class ToolRegistry:
    def __init__(self):
        self.tools = {}

    def register(self, name: str, func: callable, description: str):
        self.tools[name] = {"func": func, "description": description}

    def get_descriptions(self) -> str:
        return "\n".join([f"- {n}: {t['description']}" for n, t in self.tools.items()])

    def execute(self, name: str, **kwargs) -> Any:
        if name in self.tools:
            return self.tools[name]["func"](**kwargs)
        return {"error": f"Tool {name} not found"}

tool_registry = ToolRegistry()

def register_news_tools(get_reports_func, get_articles_func, get_summary_func):
    tool_registry.register("get_reports", get_reports_func, "Get list of available daily news reports")
    tool_registry.register("search_articles", get_articles_func, "Search news articles by query and category")
    tool_registry.register("get_summary", get_summary_func, "Get summary of latest or specific report")
    return tool_registry

class AgentOrchestrator:
    def __init__(self):
        self.tools = tool_registry

    def process(self, user_input: str, user_context: Dict = None) -> Dict:
        query = user_input.lower()
        context = user_context or {}
        response_parts = []

        if not self.tools.tools:
            return {"response": "Agent tools not initialized.", "actions": []}

        try:
            search_terms = self._extract_search_terms(query)
            category = self._detect_category(query)

            if any(w in query for w in ["latest", "today", "recent", "new", "headlines", "news"]):
                result = self.tools.execute("get_summary")
                if result and not isinstance(result, dict):
                    try: result = {"summary": result[:500]}
                    except: result = {"summary": str(result)[:500]}
                summary = (result or {}).get("summary", "")
                if summary:
                    response_parts.append(f"📰 **Latest News Summary:**\n{summary[:400]}")

            if search_terms:
                result = self.tools.execute("search_articles", query=user_input, category=category)
                if result and isinstance(result, list) and len(result) > 0:
                    articles = result[:5]
                    response_parts.append(f"\n\n🔍 **Found {len(articles)} relevant articles:**")
                    for a in articles:
                        response_parts.append(f"\n• [{a.get('title', 'Untitled')}]({a.get('url', '#')})")
                        response_parts.append(f"  *{a.get('source', 'Unknown')}*")
                else:
                    response_parts.append(f"\n\nSearching for '{user_input}'...")

            if not response_parts:
                response_parts.append(f"I'll help you find information about: **{user_input}**")
                response_parts.append("\nTry asking about:")
                response_parts.append("- What's the latest AI news?")
                response_parts.append("- Show me tech headlines today")
                response_parts.append("- News about cybersecurity")
                response_parts.append("- Articles about quantum computing")

            return {
                "response": "\n".join(response_parts),
                "actions": ["search", "analyze"],
                "context": {"query": user_input, "category": category}
            }
        except Exception as e:
            logger.error(f"Agent orchestration failed: {e}")
            return {
                "response": f"I encountered an issue processing your request. Please try again.",
                "actions": [],
                "context": {}
            }

    def _extract_search_terms(self, query: str) -> List[str]:
        stop_words = {"the","a","an","is","are","was","were","in","on","at","to","for","of","with","and","or","but","what","how","why","who","where","when","does","do","did","can","tell","me","about","give","show","list","find","any","all","latest","recent","news","this","that","i","you","we","they","it","please","could","would","should"}
        import re
        words = re.findall(r'\b\w{3,}\b', query.lower())
        return [w for w in words if w not in stop_words]

    def _detect_category(self, query: str) -> Optional[str]:
        categories = {
            "ai_agents": ["ai agent", "agentic", "multi-agent", "autonomous agent"],
            "cybersecurity": ["cyber", "security", "hack", "breach", "malware", "ransomware"],
            "quantum_computing": ["quantum", "qubit"],
            "fintech": ["fintech", "blockchain", "crypto", "payment", "banking"],
            "healthcare_ai": ["health", "medical", "healthcare", "drug", "clinical"],
            "semiconductor": ["chip", "semiconductor", "gpu", "nvidia", "intel"],
            "space_tech": ["space", "nasa", "spacex", "rocket", "satellite"],
            "automotive": ["car", "automotive", "ev", "electric vehicle", "self-driving"],
            "cloud_native": ["cloud", "kubernetes", "docker", "devops", "aws"],
            "developer_tools": ["developer", "coding", "programming", "github", "open source"],
        }
        q = query.lower()
        for cat, keywords in categories.items():
            for kw in keywords:
                if kw in q:
                    return cat
        return None

agent_orchestrator = AgentOrchestrator()
