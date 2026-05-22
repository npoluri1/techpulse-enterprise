import os
import re
import json
import hashlib
import logging
import feedparser
import httpx
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from typing import List, Dict, Optional

from enterprise_engine.config import config
from enterprise_engine.industry_categories import tag_industries, tag_sectors

logger = logging.getLogger("EnterpriseSources")


class NewsItem:
    def __init__(self, title: str, url: str, source: str, source_type: str = "rss",
                 summary: str = "", published: str = "", category: str = "General",
                 funding_amount: Optional[float] = None, funding_round: Optional[str] = None,
                 has_regulatory: bool = False):
        self.title = title
        self.url = url
        self.source = source
        self.source_type = source_type
        self.summary = summary[:500] if summary else ""
        self.published = published
        self.category = category
        self.funding_amount_usd = funding_amount
        self.funding_round = funding_round
        self.has_regulatory_impact = has_regulatory
        self.relevance_score = 0.0
        self.final_score = 0.0
        self.source_credibility = self._calc_credibility()
        self.industry_tags = tag_industries(f"{title} {summary}")
        self.sector_tags = tag_sectors(f"{title} {summary}")
        self.region_tags = self._detect_region(f"{title} {summary}")
        self.sentiment = "neutral"
        self.key_entities = self._extract_entities(f"{title} {summary}")

    def _calc_credibility(self) -> float:
        source_lower = self.source.lower()
        high = ["gartner", "mckinsey", "bcg", "deloitte", "pwc", "ieee", "nature", "science",
                "reuters", "bloomberg", "ft.com", "financial times", "bbc", "npr"]
        mid = ["techcrunch", "venturebeat", "wired", "theverge", "arstechnica", "zdnet",
               "infoworld", "theregister", "cnbc", "cnn"]
        for s in high:
            if s in source_lower:
                return 8.0
        for s in mid:
            if s in source_lower:
                return 6.0
        return 4.0

    def _detect_region(self, text: str) -> list:
        regions = {
            "North America": ["united states", "us", "usa", "canada", "silicon valley", "california",
                              "new york", "washington dc", "ottawa", "toronto"],
            "Europe": ["europe", "eu", "germany", "france", "uk", "britain", "london", "berlin",
                       "paris", "switzerland", "sweden", "finland", "european union"],
            "APAC": ["china", "japan", "south korea", "korea", "india", "singapore", "australia",
                     "beijing", "tokyo", "seoul", "bengaluru", "sydney", "taiwan"],
            "Middle East": ["uae", "dubai", "saudi arabia", "israel", "tel aviv", "qatar", "abudhabi"],
            "Africa": ["africa", "nigeria", "kenya", "south africa", "lagos", "nairobi", "cairo"],
            "LATAM": ["brazil", "mexico", "argentina", "chile", "colombia", "sao paulo", "latin america"],
        }
        text_lower = text.lower()
        detected = []
        for region, keywords in regions.items():
            if any(kw in text_lower for kw in keywords):
                detected.append(region)
        return detected if detected else ["Global"]

    def _extract_entities(self, text: str) -> list:
        companies = [
            "Google", "Microsoft", "Apple", "Amazon", "Meta", "NVIDIA", "Intel", "AMD",
            "IBM", "OpenAI", "Anthropic", "Tesla", "SpaceX", "Samsung", "TSMC", "ASML",
            "ByteDance", "Tencent", "Alibaba", "Baidu", "Huawei", "Sony", "Toyota", "VW",
            "Uber", "Airbnb", "Netflix", "Salesforce", "Oracle", "Palantir", "CrowdStrike",
            "Cloudflare", "Snowflake", "Databricks", "GitHub", "GitLab", "MongoDB",
        ]
        found = []
        for c in companies:
            if c.lower() in text.lower():
                found.append(c)
        return found

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "url": self.url,
            "source": self.source,
            "source_type": self.source_type,
            "summary": self.summary,
            "published": str(self.published) if self.published else "",
            "category": self.category,
            "funding_amount_usd": self.funding_amount_usd,
            "funding_round": self.funding_round,
            "has_regulatory_impact": self.has_regulatory_impact,
            "relevance_score": self.relevance_score,
            "final_score": self.final_score,
            "source_credibility": self.source_credibility,
            "industry_tags": self.industry_tags,
            "sector_tags": self.sector_tags,
            "region_tags": self.region_tags,
            "sentiment": self.sentiment,
            "key_entities": self.key_entities,
            "id": hashlib.md5(self.url.encode()).hexdigest(),
        }


class FreeSourceFetcher:
    def __init__(self):
        self.client = httpx.Client(timeout=30.0, follow_redirects=True)
        self.client.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
        })

    def fetch_all(self, country: str = "Global") -> List[dict]:
        items = []
        items.extend(self.fetch_rss_feeds())
        items.extend(self.fetch_newsapi(country=country))
        if config.SERPER_API_KEY:
            items.extend(self.fetch_serper())
        items.extend(self.fetch_reddit_trending())
        logger.info(f"[Sources] Total fetched: {len(items)}")
        return items

    def fetch_rss_feeds(self) -> List[dict]:
        items = []
        for feed_url in config.RSS_FEEDS:
            try:
                parsed = feedparser.parse(feed_url)
                for entry in parsed.entries[:8]:
                    title = entry.get("title", "").strip()
                    link = entry.get("link", "")
                    if not title or not link:
                        continue
                    summary = entry.get("summary", entry.get("description", ""))
                    if summary:
                        soup = BeautifulSoup(summary, "html.parser")
                        summary = soup.get_text(strip=True)[:500]
                    published = entry.get("published", "")
                    source_name = feed_url.split("/")[2].replace("www.", "").split(".")[0].capitalize()

                    item = NewsItem(
                        title=title, url=link,
                        source=f"RSS:{source_name}",
                        source_type="rss",
                        summary=summary,
                        published=published,
                    )
                    items.append(item.to_dict())
                logger.debug(f"[RSS] {feed_url}: {len(parsed.entries)} entries")
            except Exception as e:
                logger.warning(f"[RSS] Failed {feed_url}: {e}")
        return items

    def fetch_newsapi(self, country: str = "Global") -> List[dict]:
        if not config.NEWSAPI_KEY:
            logger.warning("[NewsAPI] No API key configured")
            return []
        items = []
        country_code = config.COUNTRIES.get(country, {}).get("code", "")
        country_keywords = config.COUNTRY_KEYWORDS.get(country, [])

        for query in config.NEWSAPI_QUERIES[:4]:
            try:
                q = query
                if country_keywords:
                    q = f"{query} {' OR '.join(country_keywords[:3])}"
                url = "https://newsapi.org/v2/everything"
                params = {
                    "q": q,
                    "language": "en",
                    "sortBy": "publishedAt",
                    "pageSize": 10,
                    "apiKey": config.NEWSAPI_KEY,
                }
                resp = self.client.get(url, params=params)
                data = resp.json()
                for article in data.get("articles", []):
                    item = NewsItem(
                        title=article.get("title", ""),
                        url=article.get("url", ""),
                        source=f"NewsAPI:{article.get('source', {}).get('name', 'Unknown')}",
                        source_type="api",
                        summary=article.get("description", ""),
                        published=article.get("publishedAt", ""),
                    )
                    items.append(item.to_dict())
                logger.debug(f"[NewsAPI] {query}: {len(data.get('articles', []))} articles")
            except Exception as e:
                logger.warning(f"[NewsAPI] Query '{query}' failed: {e}")

        if country_code:
            try:
                url = "https://newsapi.org/v2/top-headlines"
                params = {
                    "country": country_code,
                    "category": "technology",
                    "pageSize": 15,
                    "apiKey": config.NEWSAPI_KEY,
                }
                resp = self.client.get(url, params=params)
                data = resp.json()
                for article in data.get("articles", []):
                    item = NewsItem(
                        title=article.get("title", ""),
                        url=article.get("url", ""),
                        source=f"NewsAPI:{article.get('source', {}).get('name', 'Unknown')}",
                        source_type="api",
                        summary=article.get("description", ""),
                        published=article.get("publishedAt", ""),
                    )
                    items.append(item.to_dict())
                logger.debug(f"[NewsAPI] Top headlines {country_code}: {len(data.get('articles', []))} articles")
            except Exception as e:
                logger.warning(f"[NewsAPI] Top headlines {country_code} failed: {e}")
        return items

    def fetch_serper(self) -> List[dict]:
        if not config.SERPER_API_KEY:
            return []
        items = []
        queries = [
            "AI artificial intelligence news", "quantum computing breakthrough",
            "robotics automation latest", "tech investment funding startup",
            "cybersecurity threat intelligence", "semiconductor chip news",
        ]
        headers = {"X-API-KEY": config.SERPER_API_KEY, "Content-Type": "application/json"}
        for query in queries:
            try:
                resp = httpx.post(
                    "https://google.serper.dev/news",
                    headers=headers,
                    json={"q": query, "num": 8},
                    timeout=15,
                )
                data = resp.json()
                for result in data.get("news", []):
                    item = NewsItem(
                        title=result.get("title", ""),
                        url=result.get("link", ""),
                        source=f"Serper:{result.get('source', '')}",
                        source_type="api",
                        summary=result.get("snippet", ""),
                    )
                    items.append(item.to_dict())
                logger.debug(f"[Serper] {query}: {len(data.get('news', []))} results")
            except Exception as e:
                logger.warning(f"[Serper] Query '{query}' failed: {e}")
        return items

    def fetch_reddit_trending(self) -> List[dict]:
        items = []
        subreddits = [
            "artificial", "MachineLearning", "technology", "Futureology",
            "singularity", "hardware", "science", "worldnews",
        ]
        for sub in subreddits:
            try:
                url = f"https://www.reddit.com/r/{sub}/hot/.json?limit=5"
                resp = self.client.get(url, headers={"User-Agent": "TechPulse/1.0"})
                data = resp.json()
                for post in data.get("data", {}).get("children", []):
                    pdata = post.get("data", {})
                    title = pdata.get("title", "")
                    link = pdata.get("url", "")
                    if not title or not link:
                        continue
                    item = NewsItem(
                        title=title,
                        url=link,
                        source=f"Reddit:r/{sub}",
                        source_type="rss",
                        summary=pdata.get("selftext", "")[:300],
                        published=datetime.utcfromtimestamp(pdata.get("created_utc", 0)).isoformat(),
                    )
                    items.append(item.to_dict())
            except Exception as e:
                logger.debug(f"[Reddit] r/{sub} failed: {e}")
        return items
