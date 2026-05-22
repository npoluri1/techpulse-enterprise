import json
import hashlib
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional

from enterprise_engine.config import config
from enterprise_engine.sources import FreeSourceFetcher, NewsItem
from enterprise_engine.vector_store import FreeVectorStore
from enterprise_engine.rag_engine import FreeRAGEngine
from enterprise_engine.industry_categories import get_all_keywords, tag_industries, tag_sectors

logger = logging.getLogger("EnterpriseAgents")


class CurationAgent:
    def __init__(self):
        self.keywords = get_all_keywords()
        self.max_items = config.MAX_ARTICLES_PER_CYCLE
        self.threshold = config.CURATION_THRESHOLD

    def score(self, article: dict) -> float:
        text = f"{article.get('title', '')} {article.get('summary', '')}".lower()
        score = 0.0

        for kw in self.keywords:
            if kw.lower() in text:
                score += 5
                if kw.lower() in article.get("title", "").lower():
                    score += 10

        source_cred = article.get("source_credibility", 5)
        score += source_cred * 2

        num_patterns = ["$", "million", "billion", "trillion", "%", "percent"]
        if any(p in text for p in num_patterns):
            score += 10

        if article.get("funding_amount_usd") and article["funding_amount_usd"] > 0:
            score += 15
        if article.get("has_regulatory_impact"):
            score += 10

        industry_count = len(article.get("industry_tags", []))
        score += min(industry_count * 3, 10)

        return min(score, 100)

    def curate(self, articles: List[dict]) -> List[dict]:
        for article in articles:
            article["final_score"] = self.score(article)

        scored = sorted(articles, key=lambda x: x.get("final_score", 0), reverse=True)
        scored = [a for a in scored if a.get("final_score", 0) >= self.threshold]
        scored = self.deduplicate(scored)
        return scored[:self.max_items]

    def deduplicate(self, articles: List[dict]) -> List[dict]:
        seen = set()
        unique = []
        for a in articles:
            key = re.sub(r"[^a-z0-9]", "",
                         a.get("title", "").lower())[:60]
            if key not in seen:
                seen.add(key)
                unique.append(a)
        return unique

    def detect_alerts(self, articles: List[dict]) -> List[dict]:
        alerts = []
        threshold = config.ALERT_THRESHOLD
        for a in articles:
            score = a.get("final_score", 0)
            if score >= threshold:
                alert_type = self._classify_alert(a)
                if alert_type:
                    alerts.append({
                        "type": alert_type,
                        "severity": self._calc_severity(score),
                        "headline": a.get("title", ""),
                        "body": a.get("summary", "")[:200],
                        "industry_tags": a.get("industry_tags", []),
                        "region": ", ".join(a.get("region_tags", ["Global"])),
                        "action_url": a.get("url", ""),
                        "suggested_push_text": f"[{alert_type}] {a.get('title', '')[:100]}",
                    })
        return alerts

    def _classify_alert(self, article: dict) -> Optional[str]:
        text = f"{article.get('title', '')} {article.get('summary', '')}".lower()
        score = article.get("final_score", 0) or 0

        funding_keywords = ["raises", "funding", "series ", "million", "billion", "ipo", "acquisition"]
        if any(kw in text for kw in funding_keywords) and score >= 80:
            return "BREAKING_INVESTMENT"

        regulatory_keywords = ["regulation", "policy", "law", "compliance", "ban", "restriction",
                               "executive order", "legislation", "sanction"]
        if any(kw in text for kw in regulatory_keywords):
            return "REGULATORY_ALERT"

        model_keywords = ["new model", "gpt-", "gemini", "claude", "llama", "release",
                          "launched", "unveiled", "breakthrough"]
        if any(kw in text for kw in model_keywords):
            return "MODEL_RELEASE"

        quantum_keywords = ["quantum", "qubit", "quantum error", "quantum supremacy"]
        if any(kw in text for kw in quantum_keywords) and score >= 80:
            return "QUANTUM_BREAKTHROUGH"

        security_keywords = ["vulnerability", "breach", "ransomware", "zero-day", "cve-", "exploit"]
        if any(kw in text for kw in security_keywords):
            return "SECURITY_ALERT"

        return None

    def _calc_severity(self, score: float) -> int:
        if score >= 90: return 10
        if score >= 85: return 9
        if score >= 80: return 8
        if score >= 75: return 7
        return 6


import re


class ReportGenerator:
    def __init__(self, rag: Optional[FreeRAGEngine] = None):
        self.rag = rag

    def generate_markdown(self, insights: dict, alerts: list,
                          article_count: int, stats: dict) -> str:
        date_str = datetime.now().strftime("%d %B %Y")
        lines = [
            f"# \U0001f9e0 Global AI Intelligence Brief \u2014 {date_str}",
            "",
            f"> **Articles Curated:** {article_count} | **Alerts:** {len(alerts)} | "
            f"**Industries:** {stats.get('industries_covered', 0)}",
            f"> **Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')} UTC",
            "",
        ]

        breaking = insights.get("breaking_today", [])
        if breaking:
            lines.append("## \U0001f525 Breaking Today")
            for item in breaking:
                sev = item.get("severity", 0)
                icon = "\U0001f534" if sev >= 8 else "\U0001f7e1" if sev >= 6 else "\U0001f535"
                lines.append(f"- {icon} **[{sev}/10]** {item.get('headline', '')}")
                lines.append(f"  - {item.get('impact', '')} (_Industry: {item.get('industry', 'General')}_)")
            lines.append("")

        heatmap = insights.get("investment_heatmap", {})
        if heatmap:
            lines.append("## \U0001f4ca Investment Heatmap")
            lines.append(f"**Total Funding Mentioned:** {heatmap.get('total_funding_mentioned', 'N/A')}")
            for r in heatmap.get("top_rounds", []):
                lines.append(f"- {r}")
            lines.append("")

        industry_impact = insights.get("industry_impact", [])
        if industry_impact:
            lines.append("## \U0001f3ed Industry Impact Matrix")
            emojis = {"Transformative": "\U0001f680", "High": "\U0001f4c8",
                      "Medium": "\U0001f4ca", "Low": "\U0001f4c9", "None": "\u26aa"}
            for s in industry_impact:
                em = emojis.get(s.get("disruption_level", "None"), "\u26aa")
                lines.append(f"{em} **{s.get('sector', '')}** \u2014 {s.get('disruption_level', 'None')}")
                lines.append(f"  - {s.get('key_development', '')}")
            lines.append("")

        regional = insights.get("regional_pulse", {})
        if regional:
            lines.append("## \U0001f30d Regional Pulse")
            for region, dev in regional.items():
                if dev:
                    lines.append(f"- **{region}:** {dev}")
            lines.append("")

        if alerts:
            lines.append("## \u26a0\ufe0f Active Alerts")
            for a in alerts:
                lines.append(f"- [{a.get('type', '')}] Sev {a.get('severity', '')}: "
                             f"{a.get('headline', '')}")
            lines.append("")

        lines.append("---")
        lines.append(f"*End of Brief \u2014 TechPulse Global Intelligence*")
        return "\n".join(lines)

    def generate_mobile_brief(self, insights: dict) -> str:
        bullets = []
        for item in insights.get("breaking_today", [])[:5]:
            sev = item.get("severity", 0)
            icon = "\U0001f534" if sev >= 8 else "\U0001f7e1"
            bullets.append(f"{icon} {item.get('headline', '')[:80]}")
        while len(bullets) < 5:
            bullets.append("\U0001f4e1 Check dashboard for full briefing")
        return "\n".join(bullets[:5])
