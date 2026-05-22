import re
import logging
import json
from datetime import datetime
from typing import List, Dict
from pathlib import Path
from src.sources import NewsItem

logger = logging.getLogger("NewsAgent.Curator")
HISTORY_FILE = Path("history.json")

NON_ENGLISH_RE = re.compile(
    r'[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff'  # CJK
    r'\uac00-\ud7af\u1100-\u11ff'                 # Korean
    r'\u3040-\u309f\u30a0-\u30ff\u31f0-\u31ff'     # Japanese
    r'\u0600-\u06ff\u0750-\u077f'                  # Arabic
    r'\u0400-\u04ff\u0500-\u052f'                  # Cyrillic
    r'\u0e00-\u0e7f'                                # Thai
    r'\u0900-\u097f\u0980-\u09ff'                  # Devanagari/Bengali
    r']'
)

def is_english_text(text: str, threshold: float = 0.15) -> bool:
    if not text:
        return True
    non_eng_chars = len(NON_ENGLISH_RE.findall(text))
    total_chars = len(text.strip())
    if total_chars == 0:
        return True
    ratio = non_eng_chars / total_chars
    return ratio < threshold

class CuratorAgent:
    def __init__(self, config: dict):
        self.config = config
        self.mode = config.get("agent", {}).get("curation_mode", "relevance")
        self.max_items = config.get("output", {}).get("max_items_per_section", 15)
        self.seen_items = self.load_history()

    def load_history(self) -> set:
        if HISTORY_FILE.exists():
            try:
                with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                    return set(json.load(f))
            except:
                return set()
        return set()

    def save_history(self):
        # Keep only last 1000 items to avoid file bloat
        recent_history = list(self.seen_items)[-1000:]
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(recent_history, f)

    def keyword_score(self, item: NewsItem, keywords: List[str]) -> float:
        text = f"{item.title} {item.summary}".lower()
        score = 0.0
        for kw in keywords:
            kw_lower = kw.lower()
            count = text.count(kw_lower)
            if count > 0:
                score += count * 10.0
                if kw_lower in item.title.lower():
                    score += 20.0
        if re.search(r"\b(2026|breakthrough|new|launch|release|announce)\b", text, re.I):
            score += 5.0
        item.score = score
        return score

    def deduplicate(self, items: List[NewsItem]) -> List[NewsItem]:
        deduped = []
        for item in items:
            key = re.sub(r"[^a-zA-Z0-9]", "", item.title.lower())[:60]
            if key not in self.seen_items:
                self.seen_items.add(key)
                deduped.append(item)
        self.save_history()
        return deduped

    def is_recent(self, item: NewsItem) -> bool:
        if not item.published:
            return True
        try:
            pub_date = None
            if isinstance(item.published, str):
                pub_date = datetime.fromisoformat(item.published.replace('Z', '+00:00'))
            else:
                pub_date = item.published
            
            # Use naive comparison for simplicity
            diff = datetime.now(pub_date.tzinfo) - pub_date
            return diff.days <= 7
        except Exception:
            return True

    def curate(self, items: List[NewsItem], keywords: List[str]) -> List[NewsItem]:
        if not items:
            return []
        
        recent_items = [i for i in items if self.is_recent(i)]
        
        scored = []
        for item in recent_items:
            self.keyword_score(item, keywords)
            scored.append(item)
        scored.sort(key=lambda x: x.score, reverse=True)
        if self.mode == "relevance":
            scored = [i for i in scored if i.score > 0]
        english_only = [i for i in scored if is_english_text(i.title) and is_english_text(i.summary)]
        
        deduped = self.deduplicate(english_only)
        result = deduped[:self.max_items]
        logger.info(f"Curated {len(items)} items -> {len(recent_items)} recent -> {len(result)} relevant")
        return result

