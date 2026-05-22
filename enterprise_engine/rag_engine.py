import os
import json
import logging
from typing import List, Dict, Optional

from enterprise_engine.config import config
from enterprise_engine.vector_store import FreeVectorStore

logger = logging.getLogger("EnterpriseRAG")

try:
    from google import genai as new_genai
    HAS_GEMINI = True
except ImportError:
    HAS_GEMINI = False
    new_genai = None
    logger.warning("google-genai not installed. Try: pip install google-genai")


class FreeRAGEngine:
    def __init__(self, vector_store: FreeVectorStore):
        self.vector_store = vector_store
        self.llm = None
        self._init_llm()

    def _init_llm(self):
        if HAS_GEMINI and config.GEMINI_API_KEY:
            try:
                self.client = new_genai.Client(api_key=config.GEMINI_API_KEY)
                self.llm = config.LLM_MODEL
                logger.info(f"[LLM] Gemini initialized: {config.LLM_MODEL}")
            except Exception as e:
                logger.error(f"[LLM] Gemini init failed: {e}")
                self.llm = None
                self.client = None
        else:
            logger.warning("[LLM] No Gemini API key. Using template-based responses.")
            self.client = None

    def _call_llm(self, prompt: str) -> str:
        if self.client is None or self.llm is None:
            return "LLM not available. Please set GEMINI_API_KEY in .env"
        try:
            resp = self.client.models.generate_content(
                model=self.llm,
                contents=prompt,
                config={
                    "temperature": config.LLM_TEMPERATURE,
                    "max_output_tokens": config.LLM_MAX_TOKENS,
                }
            )
            return resp.text if resp and hasattr(resp, 'text') else str(resp)
        except Exception as e:
            logger.error(f"[LLM] Generation failed: {e}")
            return f"[LLM Error: {e}]"

    def ask(self, question: str, industry: Optional[str] = None,
            context: Optional[str] = None) -> dict:
        results = self.vector_store.search(question, k=8)
        if industry:
            industry_results = self.vector_store.search_by_industry(industry, k=5)
            all_results = results + [r for r in industry_results
                                     if r["id"] not in {x["id"] for x in results}]
        else:
            all_results = results

        context_text = context or self._format_context(all_results[:5])
        prompt = f"""You are TechPulse AI, an expert intelligence analyst.

CONTEXT from latest news articles:
{context_text}

USER QUESTION: {question}

INSTRUCTIONS:
1. Answer based ONLY on the context provided above
2. If the answer isn't in the context, say "I couldn't find that information"
3. Cite specific article titles and sources
4. Be conversational and insightful
5. When relevant, note industry impact and regional significance

ANSWER:"""
        answer = self._call_llm(prompt)
        return {
            "answer": answer,
            "sources": [{"title": r["title"], "url": r["url"], "source": r["source"]}
                       for r in all_results[:5] if r.get("url")],
        }

    def _format_context(self, articles: List[dict]) -> str:
        if not articles:
            return "No articles available."
        lines = []
        for i, a in enumerate(articles, 1):
            lines.append(f"[{i}] TITLE: {a.get('title', '')}")
            lines.append(f"    SOURCE: {a.get('source', '')}")
            lines.append(f"    SUMMARY: {a.get('content', '')[:300]}")
            lines.append(f"    INDUSTRIES: {', '.join(a.get('industry_tags', []))}")
            lines.append("")
        return "\n".join(lines)

    def generate_insights(self, articles: List[dict]) -> dict:
        if not articles:
            return {"error": "No articles to analyze"}
        top = sorted(articles, key=lambda x: x.get("final_score", 0), reverse=True)[:20]
        context = self._format_context(top)
        prompt = f"""Analyze these {len(top)} curated tech news articles and generate an executive brief.

{context}

Generate as JSON:
{{
    "breaking_today": [
        {{"severity": 1-10, "headline": "...", "impact": "...", "industry": "..."}}
    ],
    "investment_heatmap": {{
        "total_funding_mentioned": "$X",
        "top_rounds": ["..."],
        "emerging_patterns": ["..."]
    }},
    "industry_impact": [
        {{"sector": "...", "disruption_level": "None|Low|Medium|High|Transformative", "key_development": "..."}}
    ],
    "regional_pulse": {{
        "North America": "...",
        "Europe": "...",
        "APAC": "...",
        "Middle East": "...",
        "Africa": "...",
        "LATAM": "..."
    }},
    "technology_maturity": [
        {{"tech": "...", "phase": "Innovation Trigger|Peak|Trough|Slope|Plateau", "evidence": "..."}}
    ],
    "regulatory_watch": ["..."],
    "innovation_leaderboard": {{"companies": ["..."], "countries": ["..."], "universities": ["..."]}},
    "executive_summary": "2-3 sentence brief"
}}

Return ONLY valid JSON."""
        result = self._call_llm(prompt)
        try:
            cleaned = result.strip()
            if cleaned.startswith("```"):
                cleaned = cleaned.split("\n", 1)[1].rsplit("```", 1)[0].strip()
            return json.loads(cleaned)
        except:
            return {
                "breaking_today": [{"severity": 5, "headline": "Insight generation in progress"}],
                "executive_summary": result[:500],
            }
