import os
import re
import logging
import json
from typing import List, Dict, Optional, Any

import google.generativeai as genai

logger = logging.getLogger("NewsAI.RAG")

SYSTEM_PROMPT = """You are AI News Assistant, an expert AI-powered news analyst.
You have access to relevant news articles via RAG (Retrieval Augmented Generation).
ALWAYS cite specific article titles and sources when referencing information.
If you don't have relevant information, say so honestly.
Be conversational, insightful, and engaging."""

class RAGEngine:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY", "")
        self.model = None
        self._init_model()

    def _init_model(self):
        if self.api_key and self.api_key != "your_gemini_api_key_here":
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel("gemini-2.0-flash")
                logger.info("Gemini model initialized for RAG")
            except Exception as e:
                logger.warning(f"Gemini init failed: {e}")
                self.model = None

    def is_available(self) -> bool:
        return self.model is not None

    GREETING_PATTERNS = {
        "hi": "👋 Hi there! I'm NovaPulse AI, your tech news assistant. Ask me about today's top stories, AI developments, cybersecurity, or any tech topic!",
        "hello": "👋 Hello! Welcome to NovaPulse AI. I can help you explore the latest tech news. What are you interested in?",
        "hey": "👋 Hey! Ready to dive into today's tech news. Ask me about AI, startups, cybersecurity, or any trending topic!",
        "how are you": "I'm doing great, thanks for asking! Ready to help you explore today's tech news. What would you like to know about?",
        "good morning": "🌅 Good morning! Hope you're ready for today's tech news. What's caught your interest?",
        "good evening": "🌆 Good evening! Here's what's happening in tech today. What topic should we explore?",
        "what can you do": "I can help you explore the latest tech news! Try asking me about AI developments, cybersecurity threats, startup funding, tech company earnings, or any topic in today's headlines. I use RAG (Retrieval Augmented Generation) to ground my answers in real news articles with citations.",
        "help": "I'm here to help you navigate today's tech news. You can ask me about specific topics like 'AI', 'cybersecurity', 'funding', or just ask 'what's new today'. I'll search through the latest articles and give you answers with sources!",
        "bye": "👋 Goodbye! Check back later for more tech news. Stay informed!",
        "thanks": "You're welcome! Feel free to ask about any topic in today's news. Happy to help! 😊",
        "thank you": "You're welcome! Drop by anytime you want the latest tech scoop. 😊"
    }

    def _detect_greeting(self, question: str) -> Optional[str]:
        q = question.lower().strip().rstrip("?!.,")
        for pattern, response in self.GREETING_PATTERNS.items():
            if q == pattern or q.startswith(pattern + " ") or q.startswith(pattern + ","):
                return {"answer": response, "sources": []}
        return None

    def query(self, question: str, context_articles: List[Dict] = None, history: List[Dict] = None) -> Dict:
        greeting_resp = self._detect_greeting(question)
        if greeting_resp:
            return greeting_resp

        if not self.is_available():
            return self._fallback_response(question, context_articles)

        try:
            parts = [SYSTEM_PROMPT]
            if context_articles:
                ctx = "## Relevant News Articles:\n"
                for i, a in enumerate(context_articles[:8], 1):
                    ctx += f"\n{i}. {a.get('title', 'Untitled')}"
                    ctx += f"\n   Source: {a.get('source', 'Unknown')}"
                    ctx += f"\n   URL: {a.get('url', '#')}"
                    ctx += f"\n   Summary: {a.get('summary', 'No summary')[:300]}\n"
                parts.append(ctx)
            if history:
                parts.append("## Conversation History:")
                for h in history[-6:]:
                    role = "User" if h.get("role") == "user" else "Assistant"
                    parts.append(f"\n{role}: {h.get('content', '')[:500]}")
            parts.append(f"\n## User Question:\n{question}")
            full_prompt = "\n".join(parts)

            response = self.model.generate_content(
                full_prompt,
                generation_config={
                    "temperature": 0.5,
                    "max_output_tokens": 1024,
                    "top_p": 0.9,
                }
            )
            answer = response.text.strip() if response.text else "I couldn't process that question."
            sources = [a for a in (context_articles or [])[:5]]
            return {"answer": answer, "sources": sources}
        except Exception as e:
            logger.error(f"RAG query failed: {e}")
            return self._fallback_response(question, context_articles)

    def summarize_article(self, title: str, content: str) -> str:
        if not self.is_available() or not content:
            return content[:200]
        try:
            prompt = f"Summarize this article in 2-3 sentences:\nTitle: {title}\nContent: {content[:1500]}"
            resp = self.model.generate_content(prompt)
            return resp.text.strip() if resp.text else content[:200]
        except:
            return content[:200]

    def extract_topics(self, articles: List[Dict]) -> List[str]:
        if not self.is_available() or not articles:
            return []
        try:
            titles = "\n".join([a.get("title", "") for a in articles[:20]])
            prompt = f"From these article titles, identify 5-8 key trending topics. Return as comma-separated list:\n{titles}"
            resp = self.model.generate_content(prompt)
            topics = [t.strip() for t in (resp.text or "").split(",") if t.strip()]
            return topics[:8]
        except:
            return []

    def _fallback_response(self, question: str, context_articles: List[Dict] = None) -> Dict:
        if context_articles:
            keywords = self._extract_keywords(question)
            matches = []
            for a in context_articles:
                score = sum(1 for kw in keywords if kw.lower() in (a.get("title", "") + a.get("summary", "")).lower())
                if score > 0:
                    matches.append(a)
            matches = sorted(matches, key=lambda x: sum(1 for kw in keywords if kw.lower() in x.get("title", "").lower()), reverse=True)
            if matches:
                lines = [f"I found {len(matches)} relevant articles related to your question:"]
                for m in matches[:5]:
                    lines.append(f"- {m.get('title')} ({m.get('source', 'Unknown')})")
                return {"answer": "\n".join(lines), "sources": matches[:5]}
            return {"answer": "I couldn't find articles matching your question. Try asking about AI, technology, business, or specific categories.", "sources": []}
        return {"answer": "Hi! I'm your AI News Assistant powered by RAG. Ask me about the latest news in AI, tech, or any industry.", "sources": []}

    def _extract_keywords(self, text: str) -> List[str]:
        stops = {"the","a","an","is","are","was","were","in","on","at","to","for","of","with","and","or","but","what","how","why","who","where","when","does","do","did","can","tell","me","about","give","show","list","find","any","all","latest","recent","news","this","that","i","you","we","they","it"}
        words = re.findall(r'\b\w{3,}\b', text.lower())
        return [w for w in words if w not in stops]

rag_engine = RAGEngine()
