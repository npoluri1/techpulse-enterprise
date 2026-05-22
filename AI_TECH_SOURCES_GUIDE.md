# AI & Tech News Sources Master Guide — Global, Country-Wise & Industry-Specific

> **Purpose:** Comprehensive directory of websites, blogs, YouTube channels, Instagram accounts, and Facebook pages to track developments in AI, AI Agents, Cybersecurity, Quantum Computing, Robotics, and core industries.
>
> **Last Updated:** May 2026

---

## 1. Industry-Specific News Sources

| # | Industry | Publication | URL | Focus |
|---|----------|-------------|-----|-------|
| 1 | **Fintech** | Finextra | https://www.finextra.com | Banking AI, finance tech |
| 2 | **Fintech** | Fintech Futures | https://www.fintechfutures.com | Financial services, AI |
| 3 | **EdTech** | EdSurge | https://www.edsurge.com | AI in education |
| 4 | **EdTech** | eLearning Industry | https://elearningindustry.com | AI learning tools |
| 5 | **AgriTech** | AgriTech Tomorrow | https://www.agritechtomorrow.com | Smart farming, robotics |
| 6 | **AgriTech** | Future Farming | https://www.futurefarming.com | Agriculture technology |
| 7 | **ClimateTech** | Climate Tech VC | https://www.ctvc.co | Climate, energy, sustainability |
| 8 | **ClimateTech** | Canary Media | https://www.canarymedia.com | Clean energy tech |
| 9 | **Automotive** | Automotive News | https://www.autonews.com | Autonomous driving, AI |
| 10 | **Automotive** | Electrek | https://electrek.co | EV, autonomy tech |
| 11 | **LegalTech** | Law Technology Today | https://www.lawtechnologytoday.org | Legal AI, law software |
| 12 | **MarTech** | MarTech Series | https://martechseries.com | AI in marketing |
| 13 | **Retail/E-com** | Retail Dive | https://www.retaildive.com | AI in retail, commerce |
| 14 | **Manufacturing** | IndustryWeek | https://www.industryweek.com | Industry 4.0, smart factory |

---

## 2. Setting Up Automated Data Feeds

To turn these sources into a live monitoring system, use these approaches:

### 2.1 RSS Discovery (Easiest)
Most of the industry news websites listed support RSS. Use [Feedly](https://feedly.com) or [Inoreader](https://inoreader.com) and input the base URL; the tools will automatically discover the RSS feed (usually ending in `/feed` or `/rss`).

### 2.2 API Monitoring (For Devs)
- **Aggregators:** Use services like [NewsAPI](https://newsapi.org) or [Serper.dev](https://serper.dev) to query specific industry keywords (e.g., "Fintech AI") across all indexed news sites.
- **Scrapers:** Use frameworks like [Firecrawl](https://www.firecrawl.dev) (as implemented in your project's `src/sources.py`) to scrape specific industry URL lists and convert them into structured JSON/Markdown daily.

### 2.3 Curated Alerting
- **Google Alerts:** Set up alerts for specific industry domains (e.g., `site:finextra.com AND "AI"`).
- **RSS-to-Email:** Use [IFTTT](https://ifttt.com) or [Zapier](https://zapier.com) to trigger an email summary whenever a new post is detected on an industry-specific RSS feed.

---

> **Note:** See your local `news_agent.log` for existing source fetcher performance and check `src/sources.py` to see how these URLs are programmatically scraped.
