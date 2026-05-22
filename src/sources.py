import os
import requests
import feedparser
import logging
import re
from datetime import datetime
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
from urllib.parse import urlparse, urljoin
from firecrawl import FirecrawlApp

logger = logging.getLogger("NewsAgent.Sources")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
}

class NewsItem:
    def __init__(self, title: str, url: str, source: str, domain: str,
                 summary: str = "", published: str = "", author: str = ""):
        self.title = title
        self.url = url
        self.source = source
        self.domain = domain
        self.summary = summary
        self.published = published or datetime.now().isoformat()
        self.author = author
        self.score = 0.0

    def to_dict(self) -> Dict:
        return {
            "title": self.title,
            "url": self.url,
            "source": self.source,
            "domain": self.domain,
            "summary": self.summary[:200],
            "published": self.published,
            "author": self.author,
            "score": self.score,
        }

class SourceFetcher:
    def __init__(self, config: dict):
        self.config = config
        self.timeout = config.get("agent", {}).get("request_timeout", 30)
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        self.serper_api_key = os.getenv("SERPER_API_KEY", "")
        self.firecrawl = FirecrawlApp(api_key=os.getenv("FIRECRAWL_API_KEY", ""))

    def fetch_serper(self, query: str) -> List[NewsItem]:
        items = []
        try:
            logger.info(f"Searching Serper: {query}")
            url = "https://google.serper.dev/news"
            response = requests.post(url, headers={"X-API-KEY": self.serper_api_key, "Content-Type": "application/json"}, 
                                     json={"q": query, "num": 10})
            data = response.json()
            for res in data.get("news", []):
                # Use Firecrawl to get clean content if possible
                link = res.get("link", "")
                content = self._fetch_clean_content(link)
                items.append(NewsItem(
                    title=res.get("title", ""),
                    url=link,
                    source=f"SERPER:{res.get('source', '')}",
                    domain=self._domain_from_source_tag(link),
                    summary=content[:300] if content else res.get("snippet", ""),
                    published=datetime.now().isoformat()
                ))
            logger.info(f"  -> {len(items)} items from Serper")
        except Exception as e:
            logger.error(f"Serper search failed for {query}: {e}")
        return items

    def _fetch_clean_content(self, url: str) -> Optional[str]:
        try:
            crawl_result = self.firecrawl.scrape_url(url, params={"formats": ["markdown"]})
            return crawl_result.get("markdown", "")
        except Exception as e:
            logger.warning(f"Firecrawl failed for {url}: {e}")
            return None

    def fetch_rss(self, url: str) -> List[NewsItem]:
        items = []
        try:
            logger.info(f"Fetching RSS: {url}")
            parsed = feedparser.parse(url)
            for entry in parsed.entries[:25]:
                title = entry.get("title", "").strip()
                link = entry.get("link", "")
                summary = entry.get("summary", entry.get("description", ""))
                published = entry.get("published", entry.get("updated", ""))
                author = ""
                if hasattr(entry, "author"):
                    author = entry.author
                if summary:
                    soup = BeautifulSoup(summary, "html.parser")
                    clean_summary = soup.get_text(strip=True)[:300]
                else:
                    clean_summary = ""
                if title:
                    domain_hint = self._domain_from_source_tag(url)
                    items.append(NewsItem(
                        title=title, url=link, source=f"RSS:{domain_hint}",
                        domain=domain_hint, summary=clean_summary,
                        published=published, author=author
                    ))
            logger.info(f"  -> {len(items)} items from RSS")
        except Exception as e:
            logger.error(f"RSS fetch failed for {url}: {e}")
        return items

    def fetch_web(self, url: str) -> List[NewsItem]:
        items = []
        try:
            logger.info(f"Fetching web: {url}")
            resp = self.session.get(url, timeout=self.timeout, allow_redirects=True)
            resp.raise_for_status()

            soup = BeautifulSoup(resp.text, "html.parser")
            domain_hint = self._domain_from_source_tag(url)
            parsed_url = urlparse(url)
            base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

            domain = parsed_url.netloc.lower()

            if "gartner.com" in domain:
                items.extend(self._parse_gartner(soup, base_url, domain_hint))
            elif "mit.edu" in domain:
                items.extend(self._parse_mit_news(soup, base_url, domain_hint))
            elif "wired.com" in domain:
                items.extend(self._parse_wired(soup, base_url, domain_hint))
            elif "quantamagazine.org" in domain:
                items.extend(self._parse_quanta(soup, base_url, domain_hint))
            elif "nature.com" in domain:
                items.extend(self._parse_nature(soup, base_url, domain_hint))
            elif "therobotreport.com" in domain:
                items.extend(self._parse_therobotreport(soup, base_url, domain_hint))
            elif "roboticsbusinessreview.com" in domain:
                items.extend(self._parse_rbr(soup, base_url, domain_hint))
            elif "thequantuminsider.com" in domain:
                items.extend(self._parse_quantum_insider(soup, base_url, domain_hint))
            elif "quantumzeitgeist.com" in domain:
                items.extend(self._parse_quantum_zeitgeist(soup, base_url, domain_hint))
            elif "humanoid.press" in domain:
                items.extend(self._parse_humanoid_press(soup, base_url, domain_hint))
            elif "aitrends.com" in domain:
                items.extend(self._parse_aitrends(soup, base_url, domain_hint))
            elif "analyticsvidhya.com" in domain:
                items.extend(self._parse_analyticsvidhya(soup, base_url, domain_hint))
            else:
                items.extend(self._parse_generic(soup, base_url, domain_hint))

            logger.info(f"  -> {len(items)} items from web ({domain_hint})")
        except requests.exceptions.HTTPError as e:
            logger.error(f"Web fetch HTTP error for {url}: {e}")
        except requests.exceptions.Timeout:
            logger.error(f"Web fetch timeout for {url}")
        except Exception as e:
            logger.error(f"Web fetch failed for {url}: {e}")
        return items

    def _parse_gartner(self, soup: BeautifulSoup, base: str, domain: str) -> List[NewsItem]:
        items = []
        seen_urls = set()
        for article in soup.find_all(["article", "a"], class_=re.compile(r"teaser|card|promo|list-item|story", re.I)):
            self._extract_link_items(article, items, seen_urls, base, domain)

        if len(items) < 5:
            for tag in soup.find_all(["h2", "h3"]):
                a = tag.find("a", href=True)
                if a:
                    title = tag.get_text(strip=True)
                    link = urljoin(base, a["href"])
                    if title and len(title) > 15 and link not in seen_urls:
                        summary = ""
                        parent = tag.find_parent()
                        if parent:
                            p = parent.find("p")
                            if p:
                                summary = p.get_text(strip=True)[:300]
                        items.append(NewsItem(
                            title=title, url=link, source=f"WEB:{domain}",
                            domain=domain, summary=summary
                        ))
                        seen_urls.add(link)

        if len(items) < 3:
            for a in soup.find_all("a", href=True):
                title = a.get_text(strip=True)
                link = urljoin(base, a["href"])
                if title and len(title) > 20 and link not in seen_urls and "/en/" in link:
                    parent = a.find_parent(["li", "div", "article"])
                    if parent and (parent.find("time") or parent.find(class_=re.compile(r"date", re.I))):
                        items.append(NewsItem(
                            title=title, url=link, source=f"WEB:{domain}",
                            domain=domain, summary=title
                        ))
                        seen_urls.add(link)
                if len(items) >= 20:
                    break

        return items[:20]

    def _parse_mit_news(self, soup: BeautifulSoup, base: str, domain: str) -> List[NewsItem]:
        items = []
        seen_urls = set()
        for article in soup.find_all("article"):
            title_el = article.find(["h2", "h3"])
            if title_el:
                a = title_el.find("a", href=True)
                if a:
                    title = a.get_text(strip=True)
                    link = urljoin(base, a["href"])
                    summary_el = article.find("p")
                    summary = summary_el.get_text(strip=True)[:300] if summary_el else ""
                    if title and len(title) > 10 and link not in seen_urls:
                        items.append(NewsItem(
                            title=title, url=link, source=f"WEB:{domain}",
                            domain=domain, summary=summary
                        ))
                        seen_urls.add(link)
        return items[:20]

    def _parse_wired(self, soup: BeautifulSoup, base: str, domain: str) -> List[NewsItem]:
        items = []
        seen_urls = set()
        for card in soup.find_all("a", class_=re.compile(r"summary|card", re.I)):
            self._extract_link_items(card, items, seen_urls, base, domain)
        if len(items) < 5:
            for h2 in soup.find_all("h2"):
                a = h2.find("a", href=True)
                if a:
                    title = a.get_text(strip=True)
                    link = urljoin(base, a["href"])
                    if title and len(title) > 15 and link not in seen_urls:
                        items.append(NewsItem(
                            title=title, url=link, source=f"WEB:{domain}",
                            domain=domain, summary=title
                        ))
                        seen_urls.add(link)
        return items[:20]

    def _parse_quanta(self, soup: BeautifulSoup, base: str, domain: str) -> List[NewsItem]:
        items = []
        seen_urls = set()
        for article in soup.find_all("article"):
            a = article.find("a", href=True)
            if a:
                title = a.get_text(strip=True) or a.find("img", {}).get("alt", "")
                if not title:
                    h = article.find(["h2", "h3", "h4"])
                    title = h.get_text(strip=True) if h else ""
                link = urljoin(base, a["href"])
                if title and len(title) > 10 and link not in seen_urls:
                    items.append(NewsItem(
                        title=title, url=link, source=f"WEB:{domain}",
                        domain=domain, summary=title
                    ))
                    seen_urls.add(link)
        return items[:20]

    def _parse_nature(self, soup: BeautifulSoup, base: str, domain: str) -> List[NewsItem]:
        items = []
        seen_urls = set()
        for article in soup.find_all("article"):
            h3 = article.find("h3")
            if h3:
                a = h3.find("a", href=True)
                if a:
                    title = a.get_text(strip=True)
                    link = urljoin(base, a["href"])
                    desc = article.find("p")
                    summary = desc.get_text(strip=True)[:300] if desc else ""
                    if title and len(title) > 10 and link not in seen_urls:
                        items.append(NewsItem(
                            title=title, url=link, source=f"WEB:{domain}",
                            domain=domain, summary=summary
                        ))
                        seen_urls.add(link)
        return items[:20]

    def _parse_therobotreport(self, soup: BeautifulSoup, base: str, domain: str) -> List[NewsItem]:
        items = []
        seen_urls = set()
        for article in soup.find_all("article"):
            h2 = article.find("h2")
            if h2:
                a = h2.find("a", href=True)
                if a:
                    title = a.get_text(strip=True)
                    link = urljoin(base, a["href"])
                    excerpt = article.find(class_=re.compile(r"excerpt|summary|description", re.I))
                    summary = excerpt.get_text(strip=True)[:300] if excerpt else ""
                    if title and len(title) > 10 and link not in seen_urls:
                        items.append(NewsItem(
                            title=title, url=link, source=f"WEB:{domain}",
                            domain=domain, summary=summary
                        ))
                        seen_urls.add(link)
        if len(items) < 5:
            for a in soup.find_all("a", class_=re.compile(r"post|article", re.I)):
                self._extract_link_items(a, items, seen_urls, base, domain)
        return items[:20]

    def _parse_rbr(self, soup: BeautifulSoup, base: str, domain: str) -> List[NewsItem]:
        items = []
        seen_urls = set()
        for article in soup.find_all(["article", "div"], class_=re.compile(r"post|article", re.I)):
            h2 = article.find(["h2", "h3"])
            if h2:
                a = h2.find("a", href=True)
                if a:
                    title = a.get_text(strip=True)
                    link = urljoin(base, a["href"])
                    if title and len(title) > 10 and link not in seen_urls:
                        items.append(NewsItem(
                            title=title, url=link, source=f"WEB:{domain}",
                            domain=domain, summary=title
                        ))
                        seen_urls.add(link)
        return items[:20]

    def _parse_quantum_insider(self, soup: BeautifulSoup, base: str, domain: str) -> List[NewsItem]:
        items = []
        seen_urls = set()
        for article in soup.find_all("article"):
            h2 = article.find("h2")
            if not h2:
                h2 = article.find("h3")
            if h2:
                a = h2.find("a", href=True)
                if a:
                    title = a.get_text(strip=True)
                    link = urljoin(base, a["href"])
                    if title and len(title) > 10 and link not in seen_urls:
                        items.append(NewsItem(
                            title=title, url=link, source=f"WEB:{domain}",
                            domain=domain, summary=title
                        ))
                        seen_urls.add(link)
        return items[:20]

    def _parse_quantum_zeitgeist(self, soup: BeautifulSoup, base: str, domain: str) -> List[NewsItem]:
        items = []
        seen_urls = set()
        for article in soup.find_all("article"):
            h3 = article.find("h3")
            if h3:
                a = h3.find("a", href=True)
                if a:
                    title = a.get_text(strip=True)
                    link = urljoin(base, a["href"])
                    if title and len(title) > 10 and link not in seen_urls:
                        items.append(NewsItem(
                            title=title, url=link, source=f"WEB:{domain}",
                            domain=domain, summary=title
                        ))
                        seen_urls.add(link)
        return items[:20]

    def _parse_humanoid_press(self, soup: BeautifulSoup, base: str, domain: str) -> List[NewsItem]:
        items = []
        seen_urls = set()
        for article in soup.find_all("article"):
            h2 = article.find("h2")
            if h2:
                a = h2.find("a", href=True)
                if a:
                    title = a.get_text(strip=True)
                    link = urljoin(base, a["href"])
                    if title and len(title) > 10 and link not in seen_urls:
                        items.append(NewsItem(
                            title=title, url=link, source=f"WEB:{domain}",
                            domain=domain, summary=title
                        ))
                        seen_urls.add(link)
        return items[:20]

    def _parse_aitrends(self, soup: BeautifulSoup, base: str, domain: str) -> List[NewsItem]:
        items = []
        seen_urls = set()
        for article in soup.find_all("article"):
            h2 = article.find("h2")
            if h2:
                a = h2.find("a", href=True)
                if a:
                    title = a.get_text(strip=True)
                    link = urljoin(base, a["href"])
                    excerpt = article.find(["p", "div"], class_=re.compile(r"excerpt|summary", re.I))
                    summary = excerpt.get_text(strip=True)[:300] if excerpt else ""
                    if title and len(title) > 10 and link not in seen_urls:
                        items.append(NewsItem(
                            title=title, url=link, source=f"WEB:{domain}",
                            domain=domain, summary=summary
                        ))
                        seen_urls.add(link)
        return items[:20]

    def _parse_analyticsvidhya(self, soup: BeautifulSoup, base: str, domain: str) -> List[NewsItem]:
        items = []
        seen_urls = set()
        for article in soup.find_all("article"):
            h2 = article.find("h2")
            if h2:
                a = h2.find("a", href=True)
                if a:
                    title = a.get_text(strip=True)
                    link = urljoin(base, a["href"])
                    if title and len(title) > 10 and link not in seen_urls:
                        items.append(NewsItem(
                            title=title, url=link, source=f"WEB:{domain}",
                            domain=domain, summary=title
                        ))
                        seen_urls.add(link)
        if len(items) < 5:
            for a in soup.find_all("a", href=True):
                title = a.get_text(strip=True)
                if title and len(title) > 20 and "/blog/" in a["href"]:
                    link = urljoin(base, a["href"])
                    if link not in seen_urls:
                        items.append(NewsItem(
                            title=title, url=link, source=f"WEB:{domain}",
                            domain=domain, summary=title
                        ))
                        seen_urls.add(link)
                if len(items) >= 20:
                    break
        return items[:20]

    def _parse_generic(self, soup: BeautifulSoup, base: str, domain: str) -> List[NewsItem]:
        items = []
        seen_urls = set()

        for article in soup.find_all("article"):
            h2 = article.find(["h2", "h3"])
            if h2:
                a = h2.find("a", href=True)
                if a:
                    title = a.get_text(strip=True)
                    link = urljoin(base, a["href"])
                    summary_el = article.find("p")
                    summary = summary_el.get_text(strip=True)[:300] if summary_el else ""
                    if title and len(title) > 15 and link not in seen_urls:
                        items.append(NewsItem(
                            title=title, url=link, source=f"WEB:{domain}",
                            domain=domain, summary=summary
                        ))
                        seen_urls.add(link)

        if len(items) < 5:
            for tag in soup.find_all(["h1", "h2", "h3"]):
                a = tag.find("a", href=True)
                if a:
                    title = a.get_text(strip=True)
                    link = urljoin(base, a["href"])
                    if title and len(title) > 15 and link not in seen_urls:
                        items.append(NewsItem(
                            title=title, url=link, source=f"WEB:{domain}",
                            domain=domain, summary=title
                        ))
                        seen_urls.add(link)
                if len(items) >= 15:
                    break

        if len(items) < 3:
            for a in soup.find_all("a", href=True):
                title = a.get_text(strip=True)
                link = urljoin(base, a["href"])
                if title and len(title) > 15 and link not in seen_urls:
                    parent = a.find_parent(["article", "li", "div"])
                    if parent:
                        items.append(NewsItem(
                            title=title, url=link, source=f"WEB:{domain}",
                            domain=domain, summary=title
                        ))
                        seen_urls.add(link)
                if len(items) >= 15:
                    break

        return items[:20]

    def _extract_link_items(self, element, items: list, seen: set, base: str, domain: str):
        a = element.find("a", href=True)
        if a:
            title = a.get_text(strip=True)
            link = urljoin(base, a["href"])
            if title and len(title) > 15 and link not in seen:
                items.append(NewsItem(
                    title=title, url=link, source=f"WEB:{domain}",
                    domain=domain, summary=title
                ))
                seen.add(link)

    def _domain_from_source_tag(self, url: str) -> str:
        domain = urlparse(url).netloc.lower()
        domain = domain.replace("www.", "")
        parts = domain.split(".")
        if len(parts) >= 2:
            return parts[-2].capitalize()
        return parts[0].capitalize()

    def fetch_all(self, sources: List[dict]) -> List[NewsItem]:
        items = []
        for src in sources:
            if not isinstance(src, dict):
                continue
            for stype, svalue in src.items():
                if stype == "rss":
                    items.extend(self.fetch_rss(svalue))
                elif stype == "web":
                    items.extend(self.fetch_web(svalue))
                elif stype == "serper":
                    items.extend(self.fetch_serper(svalue))
        return items
