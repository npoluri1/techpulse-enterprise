"""
NovaPulse AI - Analytics & Trends Module
========================================
Provides topic extraction, chart data APIs, trend analysis,
and word cloud generation from news articles.
"""

import re
import logging
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any, Optional, Tuple
from sqlalchemy.orm import Session

logger = logging.getLogger("NewsAI.Analytics")

# Common stop words to filter out from topics
STOP_WORDS = {
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "as", "is", "are", "was", "were", "be",
    "been", "being", "have", "has", "had", "do", "does", "did", "will",
    "would", "could", "should", "may", "might", "shall", "can", "need",
    "dare", "ought", "used", "this", "that", "these", "those", "i",
    "you", "he", "she", "it", "we", "they", "me", "him", "her", "us",
    "them", "my", "your", "his", "its", "our", "their", "mine", "yours",
    "hers", "its", "ours", "theirs", "what", "which", "who", "whom",
    "when", "where", "why", "how", "all", "each", "every", "both",
    "few", "more", "most", "other", "some", "such", "no", "nor", "not",
    "only", "own", "same", "so", "than", "too", "very", "just", "because",
    "about", "into", "over", "after", "before", "between", "under",
    "above", "below", "out", "off", "up", "down", "new", "ai", "like",
    "also", "get", "got", "make", "made", "use", "used", "using",
    "take", "took", "come", "came", "know", "known", "see", "saw",
    "think", "thought", "want", "give", "find", "tell", "work"
}

# Domain-specific phrases to boost (tech terms that should be topics)
TECH_PHRASES = [
    "artificial intelligence", "machine learning", "deep learning",
    "large language model", "natural language processing", "computer vision",
    "reinforcement learning", "neural network", "transformer",
    "generative ai", "agentic ai", "autonomous agent",
    "vector database", "retrieval augmented generation", "fine tuning",
    "quantum computing", "quantum error correction", "post quantum",
    "autonomous vehicle", "self driving", "electric vehicle",
    "cloud computing", "edge computing", "serverless",
    "cybersecurity", "zero trust", "ransomware",
    "blockchain", "cryptocurrency", "defi", "fintech",
    "semiconductor", "chip design", "processor",
    "space exploration", "satellite", "aerospace",
    "robotics", "humanoid robot", "embodied ai",
    "digital twin", "internet of things", "augmented reality",
    "virtual reality", "mixed reality", "metaverse",
    "open source", "devops", "mlops", "platform engineering",
    "data engineering", "data science", "data pipeline",
    "saas", "paas", "iaas", "api",
    "regulation", "governance", "compliance", "ethics",
    "multimodal", "reasoning", "planning", "memory"
]


def extract_keywords(text: str, max_keywords: int = 20) -> List[Tuple[str, int]]:
    """Extract meaningful keywords from text with frequency counts."""
    if not text:
        return []

    text_lower = text.lower()
    words = re.findall(r'\b[a-z]{3,}\b', text_lower)
    
    # Count single words (filtering stop words)
    word_counts = Counter()
    for w in words:
        if w not in STOP_WORDS and len(w) > 2:
            word_counts[w] += 1

    # Extract multi-word phrases
    phrases_found = []
    for phrase in TECH_PHRASES:
        count = text_lower.count(phrase)
        if count > 0:
            phrases_found.append((phrase, count))

    # Combine results, boosting phrases
    result = []
    result.extend(phrases_found)
    
    # Add top single words (avoid double-counting)
    for word, count in word_counts.most_common(max_keywords * 2):
        # Skip if word is part of a found phrase
        skip = False
        for phrase, _ in phrases_found:
            if word in phrase.split():
                skip = True
                break
        if not skip:
            result.append((word, count))

    # Sort by count descending, take top N
    result.sort(key=lambda x: -x[1])
    return result[:max_keywords]


def extract_trending_topics(
    db: Session,
    limit: int = 15,
    days_back: int = 7
) -> List[Dict[str, Any]]:
    """Extract trending topics from recent articles."""
    from app_ai.database import NewsArticle
    
    cutoff = datetime.now(timezone.utc) - timedelta(days=days_back)
    
    articles = (
        db.query(NewsArticle)
        .filter(NewsArticle.fetched_at >= cutoff)
        .order_by(NewsArticle.score.desc())
        .limit(100)
        .all()
    )
    
    if not articles:
        # Fallback to all articles
        articles = (
            db.query(NewsArticle)
            .order_by(NewsArticle.score.desc())
            .limit(100)
            .all()
        )

    # Collect text from titles and summaries
    all_text = []
    for a in articles:
        title = a.title or ""
        summary = a.summary or ""
        all_text.append(f"{title} {summary[:200]}")

    text_combined = " ".join(all_text)
    keywords = extract_keywords(text_combined, max_keywords=limit)

    # Build topic items with category mappings
    category_keywords = {
        "AI & ML": ["artificial intelligence", "machine learning", "deep learning", "neural network",
                    "transformer", "llm", "large language model", "generative ai", "openai", "gpt",
                    "claude", "gemini", "llama", "mistral"],
        "AI Agents": ["agentic ai", "autonomous agent", "multi-agent", "agent", "tool use",
                     "function calling", "orchestration", "crewai", "langchain", "langgraph"],
        "Coding & Dev Tools": ["coding", "developer", "programming", "github", "open source",
                               "cursor", "vibe coding", "ide", "code generation", "api"],
        "Cybersecurity": ["cyber", "security", "hack", "breach", "ransomware", "malware",
                         "vulnerability", "zero day", "threat"],
        "Quantum Computing": ["quantum", "qubit", "quantum computing", "quantum error",
                             "post-quantum", "quantum machine learning"],
        "Semiconductors": ["semiconductor", "chip", "processor", "gpu", "nvidia", "intel",
                          "amd", "tsmc", "foundry"],
        "Space & Aerospace": ["space", "nasa", "spacex", "rocket", "satellite", "starlink",
                             "lunar", "mars", "aerospace"],
        "Autonomous Vehicles": ["autonomous", "self driving", "ev", "electric vehicle",
                               "waymo", "tesla", "robotaxi", "lidar"],
        "Robotics": ["robot", "robotics", "humanoid", "automation", "cobot",
                    "industrial robot", "ros", "embodied"],
        "Cloud & Infra": ["cloud", "kubernetes", "docker", "devops", "serverless",
                         "aws", "azure", "gcp", "infrastructure"],
        "Healthcare AI": ["healthcare", "medical", "health", "drug discovery",
                         "clinical", "diagnostics", "genomics", "fda"],
        "Finance & Fintech": ["fintech", "blockchain", "crypto", "payment", "banking",
                             "defi", "digital currency", "stablecoin"],
        "Business & Marketing": ["business", "marketing", "enterprise", "saas",
                                "startup", "funding", "revenue", "growth"],
        "Energy & Climate": ["energy", "climate", "clean energy", "renewable",
                            "solar", "battery", "carbon", "green tech"],
    }

    topics = []
    seen_phrases = set()
    
    for keyword, count in keywords:
        # Determine category
        matched_cat = "General Tech"
        keyword_lower = keyword.lower()
        for cat, cat_kws in category_keywords.items():
            if any(kw in keyword_lower for kw in cat_kws):
                matched_cat = cat
                break

        # Determine trend direction (simple heuristic)
        trend = "stable"
        if count >= 5:
            trend = "rising"
        elif count >= 3:
            trend = "stable"
        else:
            trend = "new"

        # Calculate percentage (normalized)
        max_count = max(k[1] for k in keywords) if keywords else 1
        percentage = min(100, round((count / max_count) * 100))

        topic_id = keyword.lower().replace(" ", "_")[:50]
        if topic_id not in seen_phrases:
            seen_phrases.add(topic_id)
            topics.append({
                "id": topic_id,
                "name": keyword.title() if len(keyword.split()) <= 2 else keyword.title(),
                "count": count,
                "category": matched_cat,
                "trend": trend,
                "percentage": percentage,
                "sentiment": "positive" if "breakthrough" in keyword_lower or "launch" in keyword_lower else "neutral"
            })
    
    return topics[:limit]


def get_category_distribution(db: Session) -> List[Dict[str, Any]]:
    """Get article count per category for charts."""
    from app_ai.database import NewsArticle
    
    cats = db.query(NewsArticle.category).distinct().all()
    distribution = []
    for (cat,) in cats:
        if cat:
            count = db.query(NewsArticle).filter(NewsArticle.category == cat).count()
            distribution.append({
                "name": cat.replace("_", " ").title(),
                "value": count,
                "slug": cat
            })
    return sorted(distribution, key=lambda x: -x["value"])


def get_article_growth(db: Session, days: int = 30) -> List[Dict[str, Any]]:
    """Get article fetch counts per day for growth charts."""
    from app_ai.database import NewsArticle
    
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    articles = (
        db.query(NewsArticle)
        .filter(NewsArticle.fetched_at >= cutoff)
        .all()
    )

    daily_counts = defaultdict(int)
    for a in articles:
        if a.fetched_at:
            day_key = a.fetched_at.strftime("%Y-%m-%d")
            daily_counts[day_key] += 1

    # Fill in missing days with 0
    result = []
    for i in range(days):
        day = (datetime.now(timezone.utc) - timedelta(days=days - 1 - i)).strftime("%Y-%m-%d")
        result.append({
            "date": day,
            "count": daily_counts.get(day, 0)
        })
    return result


def get_fetch_history(db: Session, limit: int = 20) -> List[Dict[str, Any]]:
    """Get recent fetch history from notification history."""
    from app_ai.database import NotificationHistory
    
    entries = (
        db.query(NotificationHistory)
        .filter(NotificationHistory.channel == "system")
        .order_by(NotificationHistory.created_at.desc())
        .limit(limit)
        .all()
    )
    return [e.to_dict() for e in entries]


def get_trending_keywords_for_cloud(
    db: Session,
    limit: int = 40,
    days_back: int = 7
) -> List[Dict[str, Any]]:
    """Get keywords formatted for word cloud visualization."""
    from app_ai.database import NewsArticle
    
    cutoff = datetime.now(timezone.utc) - timedelta(days=days_back)
    
    articles = (
        db.query(NewsArticle)
        .filter(NewsArticle.fetched_at >= cutoff)
        .order_by(NewsArticle.score.desc())
        .limit(150)
        .all()
    )
    
    if not articles:
        articles = (
            db.query(NewsArticle)
            .order_by(NewsArticle.score.desc())
            .limit(150)
            .all()
        )

    all_text = []
    for a in articles:
        title = a.title or ""
        summary = a.summary or ""
        all_text.append(f"{title} {summary[:150]}")

    text_combined = " ".join(all_text)
    keywords = extract_keywords(text_combined, max_keywords=limit)
    
    return [
        {
            "text": kw.title() if len(kw.split()) <= 2 else kw.title(),
            "value": count * 10  # Scale for visual weight
        }
        for kw, count in keywords
    ]


def log_fetch_event(db: Session, title: str, message: str, status: str = "sent"):
    """Log a system event/fetch into notification history."""
    from app_ai.database import NotificationHistory
    
    event = NotificationHistory(
        channel="system",
        title=title,
        message=message,
        status=status
    )
    db.add(event)
    db.commit()
    return event
