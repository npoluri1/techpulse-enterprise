import re
import logging
from openai import OpenAI

logger = logging.getLogger("NewsAgent.Chat")

SYSTEM_REPORT = """You are TechPulse AI, an expert news analyst for the TechPulse Daily dashboard.
You have access to today's full news report.

Rules:
1. ONLY answer from the provided report content — never make up facts.
2. If the answer isn't in the report, say "I couldn't find that in today's report. Want to ask about something else?"
3. ALWAYS cite article titles and their source URLs when you reference specific news.
4. Be conversational and engaging — give context, not just bullet points.
5. When comparing industries or topics, reference specific articles.
6. Keep answers well-structured with line breaks."""

SYSTEM_GENERAL = """You are TechPulse AI, an intelligent assistant on the TechPulse Daily dashboard.
You can discuss anything — tech, coding, business, science, or general conversation.

Rules:
1. Be knowledgeable, thoughtful, and engaging.
2. When discussing technology, give real, accurate information.
3. If you don't know something, say so honestly.
4. Keep responses well-structured and easy to read."""


class ChatEngine:
    def __init__(self, config: dict, env_vars: dict):
        self.config = config
        self.api_key = env_vars.get("OPENAI_API_KEY", "")
        self.client = OpenAI(api_key=self.api_key) if self.api_key else None
        self._llm_available = None

    def _check_llm(self) -> bool:
        if self._llm_available is not None:
            return self._llm_available
        if not self.client or not self.api_key or self.api_key == "your_key_here" or self.api_key.startswith("sk-..."):
            self._llm_available = False
            return False
        self._llm_available = True
        return True

    def ask(self, question: str, report_content: str = "", mode: str = "report", history: list = None) -> dict:
        h = history or []
        if mode == "general":
            return self._general_chat(question, h)
        if not report_content:
            llm_ok = self._check_llm()
            if llm_ok:
                try:
                    return self._general_chat(question, h)
                except Exception:
                    pass
            return {"answer": "No report content available — fetch today's news first, or switch to **💬 General** mode to chat about anything.", "sources": []}
        if self._check_llm():
            try:
                return self._ask_llm(question, report_content, h)
            except Exception as e:
                logger.error(f"LLM report chat failed: {e}")
        return self._ask_keyword(question, report_content)

    def _general_chat(self, question: str, history: list) -> dict:
        if self._check_llm():
            try:
                messages = [{"role": "system", "content": SYSTEM_GENERAL}]
                for h in history[-12:]:
                    messages.append({"role": h["role"], "content": h["content"]})
                messages.append({"role": "user", "content": question})

                resp = self.client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=messages,
                    temperature=0.7,
                    max_tokens=1200,
                )
                answer = resp.choices[0].message.content.strip()
                return {"answer": answer, "sources": []}
            except Exception as e:
                logger.error(f"LLM general chat failed: {e}")

        return {"answer": "My general AI chat is currently unavailable (API quota exhausted). Try the **📋 Report** tab — I can search today's news articles! Ask me about AI agents, cybersecurity, fintech, or any industry.", "sources": []}

    def _ask_llm(self, question: str, report_content: str, history: list) -> dict:
        max_chars = 120000
        truncated = report_content[:max_chars]
        if len(report_content) > max_chars:
            truncated += "\n\n[Report truncated due to length...]"

        messages = [{"role": "system", "content": SYSTEM_REPORT}]
        messages.append({"role": "user", "content": f"Here is today's TechPulse Daily report:\n\n{truncated}"})
        messages.append({"role": "assistant", "content": "Got it. I've read today's report and I'm ready to answer questions about it."})

        for h in history[-8:]:
            messages.append({"role": h["role"], "content": h["content"]})
        messages.append({"role": "user", "content": question})

        resp = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.5,
            max_tokens=1000,
        )
        answer = resp.choices[0].message.content.strip()
        sources = self._extract_relevant_sources(answer, report_content)
        return {"answer": answer, "sources": sources}

    GREETINGS = {
        "hi": "Hey there! I'm TechPulse AI. Ask me about anything in today's news — AI agents, cybersecurity, fintech, or any industry.",
        "hello": "Hello! I'm here to help with today's news. What industry are you curious about?",
        "hey": "Hey! Want to know what's happening in tech today? Just ask about any industry.",
        "how are you": "I'm doing great, thanks for asking! Ready to dive into today's tech news. What topic interests you?",
        "how are you doing": "All good here! Eager to help you explore today's headlines. What would you like to know?",
        "what's up": "Not much — just keeping up with all the latest tech news! Ask me about any industry.",
        "good morning": "Good morning! ☀️ A fresh day of tech news awaits. What industry would you like to explore?",
        "good afternoon": "Good afternoon! Ready to catch up on today's tech developments?",
        "good evening": "Good evening! Let's see what happened in tech today. What are you interested in?",
        "thanks": "You're welcome! Feel free to ask about any topic in today's news.",
        "thank you": "Happy to help! Just ask if you want to know more about any industry.",
    }

    def _is_greeting(self, question: str) -> str:
        q = question.lower().strip().rstrip(".!?").strip()
        if q in self.GREETINGS:
            return self.GREETINGS[q]
        for pattern, response in self.GREETINGS.items():
            if q == pattern or q.startswith(pattern + " "):
                return response
        return ""

    def _ask_keyword(self, question: str, report_content: str) -> dict:
        greeting_resp = self._is_greeting(question)
        if greeting_resp:
            return {"answer": greeting_resp, "sources": []}

        keywords = self._extract_keywords(question)
        if not keywords:
            return {"answer": "Hi! Ask me about topics in today's news — like AI agents, cybersecurity, fintech, or any industry you're interested in.", "sources": []}

        sections = self._split_sections(report_content)
        matches = []
        for section_name, section_content in sections:
            score = 0
            for kw in keywords:
                score += section_content.lower().count(kw.lower())
            if score > 0:
                urls = re.findall(r"\*\*URL:\*\*\s*(.+)", section_content)
                titles = re.findall(r"^###\s+\d+\.\s*(.+?)$", section_content, re.MULTILINE)
                matches.append({
                    "section": section_name,
                    "score": score,
                    "urls": urls,
                    "titles": titles,
                })

        matches.sort(key=lambda x: x["score"], reverse=True)

        if not matches:
            return {"answer": "I couldn't find information about that in today's report. Try asking about a specific industry like AI agents, cybersecurity, fintech, or cloud native.", "sources": []}

        top = matches[:3]
        parts = []
        seen_urls = set()
        sources = []
        for m in top:
            for i, title in enumerate(m["titles"][:3]):
                url = m["urls"][i] if i < len(m["urls"]) else ""
                sname = m["section"].replace("_", " ").title()
                parts.append(f"- {title} (_{sname}_)")
                if url and url not in seen_urls:
                    seen_urls.add(url)
                    sources.append({"title": title, "url": url})

        answer = f"I found {len(parts)} relevant article{'s' if len(parts) != 1 else ''}:\n\n" + "\n".join(parts)
        return {"answer": answer, "sources": sources[:5]}

    def _extract_keywords(self, question: str) -> list:
        stop_words = {"the", "a", "an", "is", "are", "was", "were", "in", "on", "at",
                      "to", "for", "of", "with", "and", "or", "but", "what", "how",
                      "why", "who", "where", "when", "does", "do", "did", "can",
                      "tell", "me", "about", "give", "show", "list", "find",
                      "any", "all", "latest", "recent", "news", "this", "that"}
        words = re.findall(r'\b\w+\b', question.lower())
        return [w for w in words if w not in stop_words and len(w) > 2]

    def _split_sections(self, content: str) -> list:
        sections = []
        pattern = re.compile(r"##\s+(.+?)\s*--\s*LATEST NEWS")
        pos = 0
        while True:
            m = pattern.search(content, pos)
            if not m:
                break
            section_name = m.group(1).strip()
            block_start = m.end()
            next_m = pattern.search(content, block_start)
            block_end = next_m.start() if next_m else len(content)
            sections.append((section_name, content[block_start:block_end]))
            pos = block_end
        return sections

    def _extract_relevant_sources(self, answer: str, report_content: str) -> list:
        urls = re.findall(r"\*\*URL:\*\*\s*(.+)", report_content)
        titles = re.findall(r"^###\s+\d+\.\s*(.+?)$", report_content, re.MULTILINE)
        sources = []
        for i, title in enumerate(titles[:5]):
            url = urls[i] if i < len(urls) else ""
            if url:
                sources.append({"title": title.strip(), "url": url.strip()})
        return sources[:5]
