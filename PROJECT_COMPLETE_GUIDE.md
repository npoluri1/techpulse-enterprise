# TechPulse Daily — Project Complete Guide

> **Full architecture, design, code walkthrough, and AI tech stack analysis**
>
> **Generated:** May 2026

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Architecture & Design](#2-architecture--design)
3. [Directory Structure](#3-directory-structure)
4. [AI Tech Stack Analysis](#4-ai-tech-stack-analysis)
5. [File-by-File Code Explanation](#5-file-by-file-code-explanation)
   - [config.yaml](#51-configyaml)
   - [main.py](#52-mainpy)
   - [web_app.py](#53-web_apppy)
   - [src/agent.py](#54-srcagentpy)
   - [src/sources.py](#55-srcsourcespy)
   - [src/curator.py](#56-srccuratorpy)
   - [src/formatter.py](#57-srcformatterpy)
   - [src/chat.py](#58-srcchatpy)
   - [src/utils.py](#59-srcutilspy)
   - [src/notifiers/email_notifier.py](#510-srcnotifiersemail_notifierpy)
   - [src/notifiers/whatsapp_notifier.py](#511-srcnotifierswhatsapp_notifierpy)
   - [generate_historical.py](#512-generate_historicalpy)
   - [generate_historical_v2.py](#513-generate_historical_v2py)
   - [templates/dashboard.html](#514-templatesdashboardhtml)
   - [templates/report_view.html](#515-templatesreport_viewhtml)
6. [Data Flow Diagrams](#6-data-flow-diagrams)
7. [Configuration Reference](#7-configuration-reference)
8. [Deployment & Usage](#8-deployment--usage)

---

## 1. Project Overview

**TechPulse Daily** is an automated AI-curated tech news aggregator that:

- Fetches news from **80+ RSS feeds + web sources** across **20 tech domains**
- **Filters by keyword relevance** to find high-quality articles
- **Removes duplicates** across runs using a history tracker
- **Generates a formatted Markdown report** with domain-grouped articles
- **Sends notifications** via Email (SMTP) and WhatsApp (Twilio / pywhatkit)
- **Provides a Flask web dashboard** with:
  - Real-time fetch status and progress tracking
  - Daily scheduling with APScheduler
  - Domain toggle (enable/disable specific industries)
  - Notification settings management
  - Archive browser with year/month filtering
  - **AI chat assistant** (OpenAI GPT-4o-mini) for report Q&A or general chat
- **Generates historical data** (2020–2026) using templated AI content

### Core Features

| Feature | Implementation |
|---------|---------------|
| RSS Fetching | `feedparser` library |
| Web Scraping | `BeautifulSoup` + site-specific parsers |
| AI Web Search | Serper.dev API for Google News |
| Content Cleaning | Firecrawl API |
| Relevance Curation | Keyword scoring + deduplication |
| Report Format | Markdown with section grouping |
| Web Dashboard | Flask + Jinja2 + Vanilla JS |
| Scheduler | APScheduler (CronTrigger) |
| Email Notify | SMTP (Gmail) |
| WhatsApp Notify | Twilio API / pywhatkit |
| AI Chat | OpenAI GPT-4o-mini |
| Historical Data | Templated article generation |

---

## 2. Architecture & Design

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     CLI (main.py)                        │
│  python main.py | python main.py --schedule               │
└──────────────┬──────────────────────────────────────────┘
               │
┌──────────────▼──────────────────────────────────────────┐
│                    Web Dashboard (web_app.py)             │
│  Flask server :5000 | APScheduler | REST API endpoints   │
└──────────────┬──────────────────────────────────────────┘
               │
┌──────────────▼──────────────────────────────────────────┐
│                 NewsTechAgent (src/agent.py)              │
│  Orchestrates: fetch → curate → format → notify          │
└──┬───────────┬───────────┬───────────┬──────────────────┘
   │           │           │           │
   ▼           ▼           ▼           ▼
┌──────┐  ┌────────┐  ┌────────┐  ┌──────────┐
│Source│  │Curator │  │Format  │  │Notifiers │
│Fetch │──►Agent   │──►ter     │──►(Email/   │
│(RSS/ │  │(Keyword│  │(Mark-  │  │ WhatsApp)│
│Web/  │  │Score + │  │down)   │  └──────────┘
│Serper│  │Dedup)  │  └────────┘
└──────┘  └────────┘
```

### Component Responsibilities

| Component | File | Role |
|-----------|------|------|
| **NewsTechAgent** | `src/agent.py` | Orchestrator — calls fetcher, curator, formatter, notifiers |
| **SourceFetcher** | `src/sources.py` | Fetches raw news from RSS, web scraping, Serper API |
| **CuratorAgent** | `src/curator.py` | Filters by keyword relevance, deduplicates, language check |
| **NotepadPPFormatter** | `src/formatter.py` | Builds Markdown report from curated items |
| **ChatEngine** | `src/chat.py` | OpenAI-powered chat assistant (report Q&A or general) |
| **EmailNotifier** | `src/notifiers/email_notifier.py` | Sends report via SMTP |
| **WhatsAppNotifier** | `src/notifiers/whatsapp_notifier.py` | Sends summary via Twilio/pywhatkit |
| **Web App** | `web_app.py` | Flask dashboard with REST API + scheduler |
| **CLI** | `main.py` | Command-line entry point |

### Design Patterns

1. **Orchestrator Pattern** — `NewsTechAgent` coordinates all sub-components
2. **Strategy Pattern** — `SourceFetcher` has multiple fetch strategies (RSS/Web/Serper)
3. **Pipeline Pattern** — Data flows through: Fetch → Curate → Format → Save → Notify
4. **Plugin Notifiers** — `EmailNotifier` and `WhatsAppNotifier` follow a common `send()` interface
5. **Fallback Chain** — WhatsApp tries Twilio first, falls back to pywhatkit, then prints to console

---

## 3. Directory Structure

```
Latest_News_Tech/
├── main.py                          # CLI entry point
├── web_app.py                       # Flask web dashboard (717 lines)
├── config.yaml                      # All configuration (domains, sources, keywords)
├── requirements.txt                 # Python dependencies
├── .env.example                     # Credential template
├── .schedule.json                   # Persisted scheduler config
├── history.json                     # Deduplication history (hashed titles)
├── news_agent.log                   # Runtime log file
├── PyWhatKit_DB.txt                 # pywhatkit message log
├── AI_TECH_SOURCES_GUIDE.md         # Multi-industry source directory
├── news_sources_guide.md            # Country-wise + topic source guide
├── PROJECT_COMPLETE_GUIDE.md        # ← This file
│
├── src/                             # Core application package
│   ├── __init__.py                  # Empty package init
│   ├── agent.py                     # NewsTechAgent orchestrator (93 lines)
│   ├── sources.py                   # SourceFetcher + NewsItem (520 lines)
│   ├── curator.py                   # CuratorAgent (115 lines)
│   ├── formatter.py                 # NotepadPPFormatter (73 lines)
│   ├── chat.py                      # ChatEngine for AI assistant (210 lines)
│   ├── utils.py                     # Helpers: logging, env, filenames (41 lines)
│   │
│   └── notifiers/                   # Notification plugins
│       ├── __init__.py              # Empty package init
│       ├── email_notifier.py        # SMTP email sender (87 lines)
│       └── whatsapp_notifier.py     # Twilio/pywhatkit WhatsApp sender (93 lines)
│
├── templates/                       # Flask Jinja2 templates
│   ├── dashboard.html               # Main dashboard UI (1039 lines)
│   └── report_view.html             # Single report view (150 lines)
│
├── output/                          # Generated report archives
│   └── techpulse-daily-YYYY-MM-DD.md  # Reports from 2020-01 to present
│
├── generate_historical.py           # Historical data gen v1 (weekly, 2024–2026)
├── generate_historical_v2.py        # Historical data gen v2 (monthly, 2020–2026)
│
└── .venv/                           # Python virtual environment
```

---

## 4. AI Tech Stack Analysis

### What's ACTUALLY Used vs What's NOT

| Technology | Used? | Details |
|-----------|-------|---------|
| **LLM (OpenAI GPT-4o-mini)** | ✅ YES | Chat assistant in `src/chat.py`, historical gen in `generate_historical.py` |
| **Keyword-Based Curation** | ✅ YES | `CuratorAgent` scores articles against domain keyword lists |
| **Deduplication (Hash-based)** | ✅ YES | Stores title hashes in `history.json` |
| **Non-English Filter (Regex)** | ✅ YES | Filters CJK/Arabic/Cyrillic/Thai text |
| **Firecrawl (Web Scraping)** | ✅ YES | Cleans article content via Firecrawl API |
| **Serper.dev (Google News)** | ✅ YES | Searches Google News for query terms |
| **Flask (Python Web)** | ✅ YES | Backend web framework |
| **APScheduler** | ✅ YES | Daily cron scheduling |
| **Jinja2 Templates** | ✅ YES | Server-side HTML rendering |
| **Vanilla JavaScript** | ✅ YES | Frontend interactivity (no framework) |
| **RAG (Retrieval-Augmented Generation)** | ❌ NO | There is no vector database or embedding retrieval. The chat simply passes the full report text as context to GPT |
| **Vector Database** | ❌ NO | No Chroma, Pinecone, Weaviate, FAISS, etc. |
| **LangGraph** | ❌ NO | No LangGraph graph-based agent workflows |
| **LangChain** | ❌ NO | No LangChain chains or abstractions |
| **ReactJS** | ❌ NO | Frontend is server-rendered Jinja2 + vanilla JS |
| **LangChain Agents** | ❌ NO | No agent tool-use framework |
| **Semantic Search** | ❌ NO | Only keyword-based search, no embeddings |

### What Each AI Technology Does in This Project

#### OpenAI GPT-4o-mini (LLM)
- **Powering the Chat Assistant** (`src/chat.py`):
  - Receives user questions and the full Markdown report
  - Generates context-aware answers with source citations
  - Two modes: `report` (answers from news content) and `general` (open chat)
  - Model: `gpt-4o-mini`, temperature: 0.5 (report) / 0.7 (general), max_tokens: 1000-1200
- **Historical Article Generation** (`generate_historical.py`):
  - Generates realistic tech news headlines with GPT-4o-mini
  - Falls back to template-based generation if API unavailable

#### Keyword-Based Curation (AI-Lite)
- Each domain has ~10-20 keywords in `config.yaml`
- `CuratorAgent.keyword_score()` scores each article:
  - +10 per keyword match in title/summary
  - +20 bonus if keyword appears in title
  - +5 for certain trigger words (breakthrough, new, launch, etc.)
- Items with score > 0 pass curation
- This is a **rule-based system**, not ML

#### Deduplication Engine
- Stores a hash (first 60 alphanumeric chars of lowercase title) in `history.json`
- Keeps last 1000 unique item hashes
- Prevents the same article from appearing across multiple runs

#### Language Detection
- Uses Unicode range regex to detect non-English characters
- Filters out articles where >15% characters are non-Latin
- Covers CJK, Korean, Japanese, Arabic, Cyrillic, Thai, Devanagari/Bengali

### If You Want Real RAG + LangGraph + Vector DB

The current project is intentionally **lightweight** — no heavy vector infrastructure. To upgrade:

```python
# For RAG (instead of passing full report):
# 1. Split report text into chunks
from langchain.text_splitter import RecursiveCharacterTextSplitter
# 2. Embed with OpenAI embeddings
from langchain_openai import OpenAIEmbeddings
# 3. Store in Chroma
from langchain_chroma import Chroma
# 4. Retrieve relevant chunks per query
retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
# 5. Use LangGraph for multi-step agent workflows
from langgraph.graph import StateGraph
```

---

## 5. File-by-File Code Explanation

### 5.1 config.yaml

**Path:** `config.yaml` — 472 lines

This is the **central configuration** that controls the entire agent. No code logic, but essential.

#### Structure

```yaml
agent:
  curation_mode: relevance          # Only 'relevance' mode exists
  max_sources_per_domain: 15        # Cap sources per domain
  request_timeout: 30               # HTTP request timeout (seconds)
  user_agent: AI-News-Tech-Agent/1.0

domains:                            # 20 domain groups
  ai_agents:                        # Snake-case key
    enabled: true                   # Toggle on/off
    keywords: [...]                 # Curation filter words (10-20 each)
    sources:                        # List of source configs
      - rss: https://...            # RSS feed URL
      - web: https://...            # Web scraping URL
      - serper: search query        # Serper API search

notifications:
  email:
    enabled: true
    subject_prefix: '[TechPulse Daily]'
  whatsapp:
    enabled: true

output:
  filename_prefix: techpulse-daily
  format: notepadpp_tables          # Markdown format
  max_items_per_section: 15         # Max articles per domain
  save_path: output                 # Output directory
```

#### Domain Sources (20 domains)

| Domain Key | Label | Sources Count | Example Sources |
|-----------|-------|-------------|----------------|
| ai_agents | AI Agents | 9 | Reddit, TechCrunch, VentureBeat |
| automotive | Automotive | 2 | AutoNews, Electrek |
| autonomous_vehicles | Autonomous Vehicles | 5 | Reddit, TechCrunch, Electrek |
| business_innovation | Business Innovation | 7 | Reddit, FastCompany, Wired |
| climatetech | ClimateTech | 2 | CTVC, Canary Media |
| cloud_native | Cloud Native | 7 | Reddit, InfoWorld, TheNewStack |
| cybersecurity | Cybersecurity | 7 | Reddit, Krebs, HackerNews |
| data_ai_infra | Data & AI Infra | 7 | Reddit, ZDNet, Databricks |
| developer_tools | Developer Tools | 5 | Reddit, GitHub, StackOverflow |
| edtech | EdTech | 2 | EdSurge, eLearning Industry |
| energy_cleantech | Energy & Cleantech | 8 | Reddit, ScienceDaily, CleanTechnica |
| fintech | Fintech | 5 | Reddit, TechCrunch, Finextra |
| gaming_xr | Gaming & XR | 7 | Reddit, TheVerge, TechCrunch |
| healthcare_ai | Healthcare AI | 7 | Reddit, STAT, HealthcareITNews |
| industrial_ai | Industrial AI | 7 | Reddit, ControlEng, AutomationWorld |
| legaltech | LegalTech | 1 | LawTechnologyToday |
| martech | MarTech | 1 | MarTech Series |
| quantum_computing | Quantum Computing | 7 | Reddit, ScienceDaily, Phys.org |
| semiconductor | Semiconductor | 7 | Reddit, Tom's Hardware, Ars Technica |
| space_tech | Space Tech | 5 | Reddit, Space.com, NASA |
| vibe_coding | Vibe Coding | 7 | Reddit, Aider, Cursor blog |

---

### 5.2 main.py

**Path:** `main.py` — 111 lines

The **CLI entry point**. Parses arguments and kicks off the agent.

#### Key Functions

```python
# Line 33-39: load_config()
#   Reads config.yaml using PyYAML.
#   Returns a dict. Exits if file not found.

# Line 41-46: run_agent(config, env_vars)
#   Creates NewsTechAgent, calls run_and_notify().
#   Returns the saved filepath.

# Line 48-68: run_scheduled(config, env_vars)
#   Uses the 'schedule' library (not APScheduler!).
#   Reads SCHEDULE_HOUR/MINUTE from env vars (default 08:00).
#   Runs once immediately, then waits for scheduled time.
#   Loops with time.sleep(60) checking schedule.run_pending().

# Line 70-108: main()
#   Argparse with:
#     --schedule: Run on daily cron schedule
#     --test: One source per domain (for testing)
#     --init-env: Create .env from .env.example
#   In --test mode: slices domain sources to [:1].
#   Calls run_agent() or run_scheduled().
```

#### CLI Usage
```bash
python main.py                    # Run once
python main.py --schedule         # Run daily at 08:00
python main.py --test             # Quick test (1 source/domain)
python main.py --init-env         # Create .env file
```

---

### 5.3 web_app.py

**Path:** `web_app.py` — 717 lines

The **Flask web dashboard** with REST API. The most complex file.

#### Architecture

```
web_app.py
├── Global State
│   ├── config_cache / env_cache    # Cached config (lazy load)
│   ├── scheduler (APScheduler)     # BackgroundScheduler
│   ├── is_running / stop_requested  # Threading events
│   └── last_run_status             # Run state tracker
│
├── Jinja Filters
│   ├── extract_date()              # Extract YYYY-MM-DD from filename
│   └── format_date()               # Format date readable
│
├── Config Loaders
│   ├── load_config() / load_env()
│   ├── load_schedule_config()       # .schedule.json
│   ├── save_schedule_config()
│   ├── load_notifications_config()  # Merges config.yaml + .env
│   └── save_notifications_config()  # Writes back to both
│
├── Agent Runner
│   └── run_news_agent(selected_domains)
│       └── Threaded to avoid blocking
│
├── Report Parsers
│   ├── parse_summary_from_content()  # Regex-based parser
│   ├── parse_latest_summary()
│   └── parse_historical_summary()
│
├── Routes (25 endpoints)
│   ├── GET  /                      # Dashboard page
│   ├── GET  /api/status            # Agent status JSON
│   ├── POST /api/trigger           # Start fetch
│   ├── POST /api/cancel            # Stop fetch
│   ├── GET  /api/progress          # Poll running state
│   ├── GET  /api/schedule          # Get schedule config
│   ├── POST /api/schedule          # Set schedule config
│   ├── GET  /api/reports           # List all reports
│   ├── GET  /api/reports/<file>    # Get report content
│   ├── GET  /api/reports/<file>/download  # Download report
│   ├── GET  /api/report-articles/<file>   # Parsed articles
│   ├── GET  /api/summary           # Latest summary
│   ├── GET  /api/summary/<file>    # Summary for specific report
│   ├── GET  /api/notifications     # Get notification config
│   ├── POST /api/notifications     # Set notification config
│   ├── POST /api/notifications/test # Test notification
│   ├── GET  /api/domains           # List domains
│   ├── POST /api/domains           # Toggle one domain
│   ├── POST /api/domains/batch     # Toggle multiple domains
│   ├── POST /api/chat              # AI chat endpoint
│   └── GET  /view-report/<file>    # Report view page
│
└── main()
    └── Starts Flask on 0.0.0.0:5000 + scheduler
```

#### Key Code Details

**Lines 41-53 — Global State:**
```python
SINGAPORE_TZ = ZoneInfo("Asia/Singapore")
scheduler = BackgroundScheduler(timezone=SINGAPORE_TZ)
is_running = threading.Event()     # Thread-safe flag
stop_requested = threading.Event() # Cancellation flag
last_run_status = {...}            # Tracks current/previous runs
```

**Lines 165-213 — `run_news_agent()`:**
This runs in a **background thread** to avoid blocking Flask. Key behavior:
- Checks `is_running` to prevent concurrent runs
- Stores previous run info before updating
- If `selected_domains` provided, filters which domains run
- After completion, checks `stop_requested` for cancellation
- Updates `last_run_status` with success/error/cancelled

**Lines 229-268 — `parse_summary_from_content()`:**
Uses **regex parsing** to extract structured data from Markdown:
- Finds `Generated:` timestamp
- Splits content by `DOMAIN_NAME -- LATEST NEWS` headers
- Extracts titles `(### \d+. title)`, sources, URLs, summaries
- Returns structured dict with domains[] and highlights[]

**Lines 370-395 — Dashboard Route (`/`):**
Renders `dashboard.html` with:
- `reports` — list of all .md files sorted newest-first
- `schedule` — scheduler config
- `notifications` — email/whatsapp settings
- `domains` — all domain configs
- `status` — last run status
- `latest_summary` — parsed current report
- `historical_summary` — aggregated historical data
- `can_fetch` / `lock_reason` — fetch button state

**Lines 421-442 — Trigger/Cancel:**
```python
@app.route("/api/trigger", methods=["POST"])
# Starts fetch in a new thread
# Returns immediately with status "started"
# Frontend polls /api/status every 2 seconds

@app.route("/api/cancel", methods=["POST"])
# Sets stop_requested event
# Agent checks this between domains
```

**Lines 647-667 — Chat Endpoint:**
```python
@app.route("/api/chat", methods=["POST"])
# Accepts: {question, mode, history}
# Loads latest report content
# Creates ChatEngine, calls engine.ask()
# Returns {answer, sources}
```

---

### 5.4 src/agent.py

**Path:** `src/agent.py` — 93 lines

The **orchestrator** that ties everything together.

```python
class NewsTechAgent:
    def __init__(self, config, env_vars):
        # Creates all sub-components:
        self.fetcher = SourceFetcher(config)     # Sources
        self.curator = CuratorAgent(config)       # Curation
        self.formatter = NotepadPPFormatter(config) # Formatting
        self.email_notifier = EmailNotifier(config, env_vars)
        self.whatsapp_notifier = WhatsAppNotifier(config, env_vars)
        self.results = {}  # Stores {domain_name: {items, curated}}

    def run_domain(self, domain_name, domain_config):
        # 1. Skip if disabled
        # 2. Get keywords + sources from config
        # 3. Cap sources at max_sources_per_domain
        # 4. Call fetcher.fetch_all(sources) → raw items
        # 5. Call curator.curate(items, keywords) → filtered items
        # 6. Return {items, curated}

    def run_all(self, stop_event=None):
        # Iterates ALL enabled domains
        # Checks stop_event between domains (cancellation support)
        # Stores results in self.results

    def generate_report(self):
        # Calls formatter.build_full_report(self.results)
        # Returns Markdown string

    def save_report(self, report):
        # Builds filename: techpulse-daily-YYYY-MM-DD.md
        # Ensures output dir exists
        # Writes file, returns filepath

    def notify(self, report, filepath):
        # Sends email and WhatsApp
        # Both notifiers check their own enabled flag

    def run_and_notify(self, stop_event=None):
        # run_all() → generate_report() → save_report() → notify()
        # Handles cancellation mid-run
        # Returns filepath or None on error
```

**Pipeline Flow:**
```
run_and_notify()
  ├── run_all() [for each domain]
  │     ├── fetcher.fetch_all(sources)    → List[NewsItem]
  │     └── curator.curate(items, keywords) → List[NewsItem] (filtered)
  ├── generate_report()                   → str (Markdown)
  ├── save_report(report)                 → str (filepath)
  └── notify(report, filepath)
        ├── email_notifier.send(report, filepath)
        └── whatsapp_notifier.send(report)
```

---

### 5.5 src/sources.py

**Path:** `src/sources.py` — 520 lines

The **data acquisition layer**. Fetches news from three source types.

#### NewsItem Data Class

```python
class NewsItem:
    def __init__(self, title, url, source, domain,
                 summary="", published="", author=""):
        self.title = title       # Article headline
        self.url = url           # Permalink
        self.source = source     # "RSS:TechCrunch" | "WEB:..." | "SERPER:..."
        self.domain = domain     # "Techcrunch" (source hint)
        self.summary = summary   # First 300 chars
        self.published = published  # ISO date string
        self.author = author     # Byline
        self.score = 0.0         # Set by CuratorAgent later
```

#### SourceFetcher Class

**Fetch Methods:**

| Method | Input | Source | Output |
|--------|-------|--------|--------|
| `fetch_rss(url)` | RSS feed URL | `feedparser` | Up to 25 NewsItems |
| `fetch_web(url)` | Web page URL | `BeautifulSoup` + site parsers | Up to 20 NewsItems |
| `fetch_serper(query)` | Search query | Serper.dev API | Up to 10 NewsItems |

**`fetch_all(sources)`** — Dispatches to the right method:
```python
def fetch_all(self, sources):
    for src in sources:
        for stype, svalue in src.items():
            if stype == "rss":    items.extend(self.fetch_rss(svalue))
            elif stype == "web":   items.extend(self.fetch_web(svalue))
            elif stype == "serper": items.extend(self.fetch_serper(svalue))
```

**RSS Fetching (`fetch_rss`):**
```python
def fetch_rss(self, url):
    parsed = feedparser.parse(url)    # Parse RSS/Atom
    for entry in parsed.entries[:25]: # Limit 25 per feed
        # HTML-to-text via BeautifulSoup for summary
        soup = BeautifulSoup(summary, "html.parser")
        clean_summary = soup.get_text(strip=True)[:300]
```

**Web Scraping (`fetch_web`):**
Has **14 site-specific parsers** for domain-specific HTML structure:

| Parser | Target Sites |
|--------|-------------|
| `_parse_gartner()` | gartner.com |
| `_parse_mit_news()` | mit.edu |
| `_parse_wired()` | wired.com |
| `_parse_quanta()` | quantamagazine.org |
| `_parse_nature()` | nature.com |
| `_parse_therobotreport()` | therobotreport.com |
| `_parse_rbr()` | roboticsbusinessreview.com |
| `_parse_quantum_insider()` | thequantuminsider.com |
| `_parse_quantum_zeitgeist()` | quantumzeitgeist.com |
| `_parse_humanoid_press()` | humanoid.press |
| `_parse_aitrends()` | aitrends.com |
| `_parse_analyticsvidhya()` | analyticsvidhya.com |
| `_parse_generic()` | Fallback for any site |

Each parser follows a similar pattern:
1. Find `<article>` elements (or site-specific selectors)
2. Extract `<h2>`/`<h3>` → title + link
3. Find `<p>` → summary
4. Return up to 20 NewsItems
5. Fallback strategies if primary parsing finds <5 items

**Serper API (`fetch_serper`):**
```python
def fetch_serper(self, query):
    response = requests.post(
        "https://google.serper.dev/news",
        headers={"X-API-KEY": self.serper_api_key},
        json={"q": query, "num": 10}
    )
    data = response.json()
    for res in data.get("news", []):
        # Optionally clean content via Firecrawl
        content = self._fetch_clean_content(link)
        items.append(NewsItem(...))
```

**Firecrawl Integration:**
```python
def _fetch_clean_content(self, url):
    crawl_result = self.firecrawl.scrape_url(
        url, params={"formats": ["markdown"]}
    )
    return crawl_result.get("markdown", "")
```
Used optionally to get clean Markdown from article URLs. Silently fails if unavailable.

---

### 5.6 src/curator.py

**Path:** `src/curator.py` — 115 lines

The **intelligence layer** — filters raw items to find relevant ones.

#### CuratorAgent Class

**`__init__`:**
```python
def __init__(self, config):
    self.mode = config["agent"]["curation_mode"]  # "relevance"
    self.max_items = config["output"]["max_items_per_section"]  # 15
    self.seen_items = self.load_history()  # Load from history.json
```

**`keyword_score(item, keywords)` — Line 55:**
```python
def keyword_score(self, item, keywords):
    text = f"{item.title} {item.summary}".lower()
    score = 0.0
    for kw in keywords:
        count = text.count(kw.lower())
        if count > 0:
            score += count * 10.0        # +10 per match
            if kw.lower() in item.title.lower():
                score += 20.0            # +20 if in title
    if re.search(r"\b(2026|breakthrough|new|launch|release|announce)\b", text, re.I):
        score += 5.0                     # +5 for trigger words
    item.score = score
    return score
```

**`deduplicate(items)` — Line 70:**
```python
def deduplicate(self, items):
    for item in items:
        key = re.sub(r"[^a-zA-Z0-9]", "", item.title.lower())[:60]
        if key not in self.seen_items:
            self.seen_items.add(key)
            deduped.append(item)
    self.save_history()  # Persist to history.json
```
Creates a 60-char hash from alphanumeric lowercase title. Stores in `history.json` (last 1000).

**`curate(items, keywords)` — Line 96 — The Main Pipeline:**
```python
def curate(self, items, keywords):
    recent_items = [i for i in items if self.is_recent(i)]  # Within 7 days
    scored = []
    for item in recent_items:
        self.keyword_score(item, keywords)
        scored.append(item)
    scored.sort(key=lambda x: x.score, reverse=True)  # Best first
    scored = [i for i in scored if i.score > 0]  # Only relevant
    english_only = [i for i in scored if is_english_text(...)]  # English filter
    deduped = self.deduplicate(english_only)  # Remove duplicates
    result = deduped[:self.max_items]  # Cap at max_items
    return result
```

**Non-English Detection (Line 12-31):**
```python
NON_ENGLISH_RE = re.compile(r'[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff...]')

def is_english_text(text, threshold=0.15):
    non_eng_chars = len(NON_ENGLISH_RE.findall(text))
    ratio = non_eng_chars / len(text.strip())
    return ratio < threshold  # <15% non-Latin chars
```
Blocks CJK, Korean, Japanese, Arabic, Cyrillic, Thai, Devanagari/Bengali text.

---

### 5.7 src/formatter.py

**Path:** `src/formatter.py` — 73 lines

Converts curated items into the final Markdown report.

#### NotepadPPFormatter Class

**`format_section(title, items)` — Line 25:**
```python
def format_section(self, title, items):
    lines = [f"## {title}", ""]
    for idx, item in enumerate(items, 1):
        lines.append(f"### {idx}. {item.title}")
        lines.append(f"- **Source:** {item.source}")
        lines.append(f"- **URL:** {item.url if item.url else 'N/A'}")
        lines.append(f"- **Summary:** {item.summary}")
    return "\n".join(lines)
```

**Output example:**
```markdown
## AI_AGENTS -- LATEST NEWS

### 1. New breakthrough in multi-agent systems announced
- **Source:** RSS:TechCrunch
- **URL:** https://techcrunch.com/...
- **Summary:** Researchers demonstrate a new multi-agent AI system...
```

**`build_full_report(domain_data)` — Line 47:**
```python
def build_full_report(self, domain_data):
    now = datetime.now(SGT).strftime("%Y-%m-%d %H:%M SGT")
    lines = [
        "# TechPulse Daily -- Comprehensive Tech & Industry Digest\n",
        f"> **Generated:** {now} | **Sources:** RSS + Web | **Mode:** AI-Curated\n"
    ]
    for domain_name, data in domain_data.items():
        if data.get("curated"):
            section = self.format_section(f"{domain_name.upper()} -- LATEST NEWS", curated)
            lines.append(section)
    lines.append(f"**Total Articles:** {total_items}")
    lines.append("*End of Report — TechPulse Daily*")
```

---

### 5.8 src/chat.py

**Path:** `src/chat.py` — 210 lines

The **AI-powered chat assistant** using OpenAI GPT-4o-mini.

#### ChatEngine Class

**System Prompts:**

**Report mode** (Line 7-16):
```
You are TechPulse AI, an expert news analyst...
Rules:
1. ONLY answer from the provided report content
2. If not found, say "I couldn't find that..."
3. ALWAYS cite article titles and URLs
4. Be conversational and engaging
```

**General mode** (Line 18-25):
```
You are TechPulse AI, an intelligent assistant...
Rules:
1. Be knowledgeable, thoughtful, and engaging
2. Give real, accurate information
3. If you don't know, say so honestly
```

**`ask(question, report_content, mode, history)` — Line 44 — The Main Entry:**
```python
def ask(self, question, report_content, mode, history):
    if mode == "general":
        return self._general_chat(question, history)  # Open chat
    if not report_content:
        # No report available → try general or show error
        llm_ok = self._check_llm()
        if llm_ok:
            return self._general_chat(question, history)
        return {"answer": "No report...", "sources": []}
    if self._check_llm():
        return self._ask_llm(question, report_content, history)  # GPT-4o-mini
    return self._ask_keyword(question, report_content)  # Fallback: keyword search
```

**`_ask_llm()` — Line 84 — GPT-4o-mini with Report Context:**
```python
def _ask_llm(self, question, report_content, history):
    truncated = report_content[:120000]  # Truncate to fit context window
    messages = [
        {"role": "system", "content": SYSTEM_REPORT},
        {"role": "user", "content": f"Here is today's report:\n\n{truncated}"},
        {"role": "assistant", "content": "Got it. I've read today's report."},
        # ... conversation history ...
        {"role": "user", "content": question}
    ]
    resp = self.client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.5,
        max_tokens=1000,
    )
    sources = self._extract_relevant_sources(answer, report_content)
    return {"answer": answer, "sources": sources}
```

**`_ask_keyword()` — Line 131 — Fallback (No OpenAI):**
When API key is missing, falls back to pure keyword search:
1. Check for greeting responses (hardcoded map)
2. Extract keywords from question (remove stop words)
3. Split report into domain sections
4. Score sections by keyword match count
5. Return top 3 sections with matching article titles
6. Provide source URLs

**Greeting Detection (Line 108-129):**
Hardcoded response map for common greetings:
```python
GREETINGS = {
    "hi": "Hey there! I'm TechPulse AI...",
    "hello": "Hello! I'm here to help...",
    "how are you": "I'm doing great...",
    ...
}
```

**`_check_llm()` — Line 35:**
Validates API key exists and isn't placeholder (`sk-...` or `your_key_here`).

---

### 5.9 src/utils.py

**Path:** `src/utils.py` — 41 lines

Utility helpers used across the project.

| Function | Line | Purpose |
|----------|------|---------|
| `setup_logging(log_file)` | 8 | Configures file + console logging with format: `timestamp \| LEVEL \| Logger \| Message` |
| `sanitize_filename(prefix)` | 19 | Creates `techpulse-daily-2026-05-22` from prefix + current date |
| `ensure_dir(path)` | 24 | `mkdir -p` equivalent |
| `load_env_file(env_path)` | 27 | Manual `.env` parser (no python-dotenv dependency). Parses `KEY=VALUE` lines, skips comments and blanks |
| `truncate(text, max_len)` | 40 | Cuts text to `max_len` chars with `...` |

---

### 5.10 src/notifiers/email_notifier.py

**Path:** `src/notifiers/email_notifier.py` — 87 lines

Sends the report via SMTP email with HTML formatting.

#### EmailNotifier Class

**`send(report_text, report_file)` — Line 39:**
```python
def send(self, report_text, report_file=None):
    self._load_latest_config()  # Reload config/env for fresh values
    if not self.enabled: return False

    # Build MIME multipart message
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"{prefix} Daily AI-Tech Report"

    # HTML body with inline styles
    html = f"""<html><body style="...">
    <h1>AI-TECH-DAILY Report</h1>
    <pre>{report_text}</pre>
    </body></html>"""
    msg.attach(MIMEText(html, "html"))

    # Attach .md file if available
    if report_file:
        with open(report_file) as f:
            attachment = MIMEText(f.read())
            attachment.add_header("Content-Disposition",
                                  "attachment", filename=filename)
            msg.attach(attachment)

    # SMTP send via TLS
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(email_from, password)
    server.send_message(msg)
```

**`_load_latest_config()` — Line 31:**
Hot-reloads config.yaml and .env before sending to get latest credentials.

---

### 5.11 src/notifiers/whatsapp_notifier.py

**Path:** `src/notifiers/whatsapp_notifier.py` — 93 lines

Sends WhatsApp notification with **two fallback methods**.

#### WhatsAppNotifier Class

**`send(report_text)` — Line 72 — Main Method:**
```python
def send(self, report_text):
    if not self.enabled: return False
    phone = self.env.get("WHATSAPP_PHONE_NUMBER", "")

    # Truncate to 1500 chars (Twilio limit)
    preview = report_text[:1500]
    preview = preview.replace("=" * 80, "\n" + "=" * 40 + "\n")

    # Try Twilio first
    if self.send_twilio(phone, preview): return True

    # Fallback to pywhatkit
    if self.send_pywhatkit(phone, preview): return True

    # Final fallback: print to console
    print(preview)
    return False
```

**`send_twilio()` — Line 37:**
```python
def send_twilio(self, phone, message):
    from twilio.rest import Client
    client = Client(account_sid, auth_token)
    msg = client.messages.create(
        body=message,
        from_=f"whatsapp:{twilio_from}",
        to=f"whatsapp:{phone}"
    )
```

**`send_pywhatkit()` — Line 57:**
```python
def send_pywhatkit(self, phone, message):
    import pywhatkit
    pywhatkit.sendwhatmsg_instantly(
        phone_no=phone,
        message=message,
        wait_time=20,
        tab_close=True
    )
```
Opens WhatsApp Web in a browser, types and sends the message, then closes tab.

---

### 5.12 generate_historical.py

**Path:** `generate_historical.py` — 654 lines

Generates **weekly historical reports** from 2024-05 to 2026-05.

#### Architecture

```
generate_historical.py
├── DOMAIN_TEMPLATES (20 domains × 20 article templates each)
│   └── Each template has {placeholder} variables
├── COMPANIES / CITIES / COUNTRIES (data pools)
├── gen_value(placeholder) → fills templates with realistic values
├── fill_template(template) → regex substitution
├── gen_articles_for_domain() → template-based generation
├── try_openai_generate() → GPT-4o-mini generation (optional)
├── build_report() → assembles Markdown
└── main() → iterates dates, generates missing reports
```

**Template Example (Line 22):**
```python
"ai_agents": {
    "label": "AI Agents",
    "articles": [
        "OpenAI announces GPT-{ver}, claims {metric} improvement...",
        "Anthropic releases Claude {ver} with enhanced {feature}...",
        "Google DeepMind unveils {project}, a breakthrough in {field}...",
        ...
    ]
}
```

**`gen_value()` — Line 443:**
Maps `{placeholder}` to realistic random values:
```python
"n": lambda: str(random.choice([3, 5, 10, 15, 20, 25, ...])),
"B": lambda: f"{random.choice([1, 2, 3, 5, 10, ...])}",
"company": lambda: random.choice(COMPANIES),
"metric": lambda: f"{random.choice([85, 90, 95, ...])}.{random.choice([0, 1, 2, 5])}%",
```

**`try_openai_generate()` — Line 559:**
```python
def try_openai_generate(domain_key, domain_label, date_str, api_key):
    prompt = f"""Generate {random.randint(8, 12)} realistic tech news headlines
    for "{domain_label}" dated around {date_str}.
    Format as JSON list..."""
    resp = client.chat.completions.create(
        model="gpt-4o-mini", temperature=0.8, max_tokens=2000
    )
    data = json.loads(resp.choices[0].message.content)
```

**Two-tier generation:**
- If OpenAI key available → use GPT-4o-mini for realistic articles
- Otherwise → template-based random generation

---

### 5.13 generate_historical_v2.py

**Path:** `generate_historical_v2.py` — 55 lines

**Extended version** generating **monthly** reports from 2020-01 to 2026-05.

```python
def main():
    start_date = datetime(2020, 1, 15, tzinfo=SGT)
    end_date = datetime(2026, 5, 19, tzinfo=SGT)
    # ...
    while current <= end_date:
        # Skip existing files
        # Generate using template-based approach only (no OpenAI)
        domain_articles[domain_key] = gh.gen_articles_for_domain(
            domain_key, domain_info, count=random.randint(8, 12)
        )
        current += relativedelta(months=1)
```
Reuses `gen_articles_for_domain()` and `build_report()` from `generate_historical.py`.

---

### 5.14 templates/dashboard.html

**Path:** `templates/dashboard.html` — 1039 lines

Single-page application with **no JavaScript framework** — pure vanilla JS + CSS.

#### UI Structure

```
┌──────────────────────────────────────┐
│ Nav: Logo + Status Badge              │
├──────────────────────────────────────┤
│ Meta: Date · Domains · Articles       │
├──────────────────────────────────────┤
│ Industry Pills (scrollable)           │
├──────────────────┬───────────────────┤
│ Actions Card     │ Notifications Card │
│ ├ Fetch/Stop Btn │ ├ Email Config    │
│ ├ Stats (3)      │ ├ WhatsApp Config │
│ ├ Schedule        │ └ Test buttons   │
│ ├ Toggle + Time   │                   │
│ └ Hour/Min Inputs │                   │
├──────────────────┴───────────────────┤
│ Today's Highlights (paginated)        │
│ ├ Industry filter dropdown            │
│ ├ 10 articles per page               │
│ └ Prev/Next navigation               │
├──────────────────────────────────────┤
│ Archive Browser                       │
│ ├ Year/Month filters                  │
│ ├ Monthly groups (collapsible)        │
│ └ Card grid per report                │
│   ├ Day number · Size                 │
│   ├ Date label                        │
│   └ View / Download buttons           │
└──────────────────────────────────────┘
```

#### Key JavaScript Functions

| Function | Line | What It Does |
|----------|------|-------------|
| `loadDomains()` | 482 | Fetches `/api/domains`, creates pill UI |
| `togglePill(el)` | 549 | Enables/disables a domain, syncs with backend |
| `triggerFetch()` | 584 | POSTs selected domains to `/api/trigger`, starts polling |
| `cancelFetch()` | 612 | POSTs to `/api/cancel` |
| `pollUntilDone()` | 620 | Polls `/api/status` every 2s, reloads on completion |
| `renderTodayPage()` | 772 | Shows paginated articles for current report |
| `renderArchive()` | 698 | Renders month-grouped archive cards |
| `sendChat()` | 939 | Sends chat message to `/api/chat`, renders response |
| `switchChatMode()` | 915 | Toggles between Report and General chat modes |
| `saveSchedule()` | 831 | POSTs schedule config to `/api/schedule` |
| `saveChannel()` | 874 | Saves notification config to backend |
| `testChannel()` | 893 | Sends test notification |
| `toggleChat()` | 930 | Opens/closes chat panel |

#### Chat UI (Lines 417-469, 907-993)

Floating chat button → opens panel with:
- Two tabs: **Report** (answers from news) and **General** (open chat)
- Messages area with user/AI bubbles
- Auto-resizing textarea input
- Loading animation (bouncing dots)
- Source link display when available

---

### 5.15 templates/report_view.html

**Path:** `templates/report_view.html` — 150 lines

Dedicated page for viewing a single report's full content.

#### Features
- Back to Dashboard link
- Download button
- Industry filter pills (filter by domain)
- All articles rendered as styled cards with:
  - Title (clickable link to original)
  - Source attribution
  - Summary
- Article count badge

#### Rendering
- Receives `report_data` as Jinja JSON injection: `{{ report_data | tojson }}`
- Client-side rendering via vanilla JS `render()` function
- Escape HTML for XSS protection

---

## 6. Data Flow Diagrams

### 6.1 Full News Fetch Flow

```
User clicks "Fetch" on dashboard (or schedule triggers)
         │
         ▼
run_news_agent() [web_app.py:165]
         │
         ▼
NewsTechAgent.run_and_notify() [agent.py:75]
         │
         ▼
NewsTechAgent.run_all() [agent.py:48]
         │
         ├── [Domain: ai_agents]
         │     │
         │     ├── SourceFetcher.fetch_all(sources)
         │     │     ├── fetch_rss("https://reddit.com/...")      → [5 NewsItems]
         │     │     ├── fetch_rss("https://techcrunch.com/...")  → [8 NewsItems]
         │     │     ├── fetch_web("https://artificial-intelligence.blog/...")
         │     │     │     └── _parse_generic()                   → [10 NewsItems]
         │     │     └── Total: 23 items
         │     │
         │     └── CuratorAgent.curate(23 items, keywords)
         │           ├── Filter: is_recent() (within 7 days)      → 18 items
         │           ├── Score: keyword_score() per item
         │           ├── Sort: by score descending
         │           ├── Filter: score > 0                         → 12 items
         │           ├── Filter: is_english_text()                 → 11 items
         │           ├── Deduplicate() against history.json         → 10 items
         │           └── Cap: [:15]                                → 10 items
         │
         ├── [Domain: cybersecurity]
         │     ├── fetch_all() → 30 items
         │     └── curate() → 8 items
         │
         └── [19 more domains...]
               │
               └── Results stored in self.results
                     │
                     ▼
         NewsTechAgent.generate_report() [agent.py:57]
               │
               └── NotepadPPFormatter.build_full_report(results)
                     │
                     ├── ## AI_AGENTS -- LATEST NEWS
                     │     ├── ### 1. Title ...
                     │     ├── **Source:** RSS:TechCrunch
                     │     └── **Summary:** ...
                     │
                     ├── ## CYBERSECURITY -- LATEST NEWS
                     │     └── ...
                     │
                     └── **Total Articles:** 145
                           │
                           ▼
         NewsTechAgent.save_report(report) [agent.py:61]
               │
               ├── Filename: output/techpulse-daily-2026-05-22.md
               └── File written to disk
                     │
                     ▼
         NewsTechAgent.notify(report, filepath) [agent.py:71]
               │
               ├── EmailNotifier.send()
               │     ├── HTML email with report in <pre> tag
               │     ├── Attachment: .md file
               │     ├── SMTP → Gmail → Recipient inbox
               │     └── Success/Error logged
               │
               └── WhatsAppNotifier.send()
                     ├── Try: send_twilio() → Twilio API
                     ├── Fail? Try: send_pywhatkit() → WhatsApp Web
                     └── Fail? Print to console
```

### 6.2 AI Chat Flow

```
User types question in chat panel
         │
         ▼
sendChat() [dashboard.html:939]
         │
         ├── POST /api/chat [web_app.py:647]
         │     ├── Loads latest report content
         │     ├── Creates ChatEngine
         │     └── Calls engine.ask(question, report, mode, history)
         │
         ▼
ChatEngine.ask() [chat.py:44]
         │
         ├── Mode = "report"?
         │     ├── YES → Report available?
         │     │     ├── YES → OpenAI key valid?
         │     │     │     ├── YES → _ask_llm()
         │     │     │     │     ├── Truncate report to 120K chars
         │     │     │     │     ├── Build messages with system prompt
         │     │     │     │     ├── GPT-4o-mini generates answer
         │     │     │     │     └── Extract source URLs from answer
         │     │     │     │
         │     │     │     └── NO → _ask_keyword()
         │     │     │           ├── Check greetings
         │     │     │           ├── Extract keywords from question
         │     │     │           ├── Score report sections by keyword match
         │     │     │           └── Return top matches with URLs
         │     │     │
         │     │     └── NO → Try general chat or return "No report"
         │     │
         │     └── NO (General mode) → _general_chat()
         │           ├── OpenAI key valid?
         │           │     ├── YES → GPT-4o-mini with SYSTEM_GENERAL
         │           │     └── NO → Return "API unavailable" message
         │           └── Return {answer, sources}
         │
         ▼
Frontend renders response
├── User bubble with question
├── AI bubble with answer
└── Source links (if available)
```

### 6.3 Historical Data Generation Flow

```
generate_historical.py main()
         │
         ├── Dates: 2024-05-15 to 2026-05-14 (weekly)
         │
         ├── For each date:
         │     ├── Skip if file already exists
         │     │
         │     ├── For each of 20 domains:
         │     │     ├── OpenAI key available?
         │     │     │     ├── YES → try_openai_generate()
         │     │     │     │     ├── GPT-4o-mini generates JSON article list
         │     │     │     │     └── Parse JSON → NewsItem-like dicts
         │     │     │     │
         │     │     │     └── NO/Fail → gen_articles_for_domain()
         │     │     │           ├── Pick random template
         │     │     │           ├── Fill {placeholders} with gen_value()
         │     │     │           └── Generate 8-12 articles
         │     │     │
         │     │     └── Store in domain_articles[domain_key]
         │     │
         │     └── build_report(domain_articles, date_str)
         │           └── Write to output/techpulse-daily-{date}.md
         │
         └── Result: ~100 weekly reports
```

---

## 7. Configuration Reference

### config.yaml Domains

Each domain has this structure:

```yaml
domain_key:                 # Snake-case identifier
  enabled: true             # Toggle on/off
  keywords:                 # Curation filter (10-20 terms)
    - keyword 1
    - keyword 2
  sources:                  # News sources (list of dicts)
    - rss: https://...      # RSS/Atom feed
    - web: https://...      # Web scraping target
    - serper: search query  # Serper API search
```

### .env File

```ini
EMAIL_FROM=your_email@gmail.com
EMAIL_TO=recipient@example.com
EMAIL_PASSWORD=your_app_password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587

WHATSAPP_PHONE_NUMBER=+6591234567
TWILIO_ACCOUNT_SID=your_sid
TWILIO_AUTH_TOKEN=your_token
TWILIO_WHATSAPP_NUMBER=+14155238886

OPENAI_API_KEY=sk-proj-...

SCHEDULE_HOUR=08
SCHEDULE_MINUTE=00

SERPER_API_KEY=your_serper_key
FIRECRAWL_API_KEY=your_firecrawl_key
```

### Existing .md Guide Files

| File | Content | Purpose |
|------|---------|---------|
| `news_sources_guide.md` | Country-wise & topic-wise source directory with 100+ entries across 10 categories | Manual reference for finding new sources to add to config.yaml |
| `AI_TECH_SOURCES_GUIDE.md` | Industry-specific sources + setup guide for RSS/API/scraping | Helps configure automated news feeds |
| `PROJECT_COMPLETE_GUIDE.md` | ← This file | Full technical documentation |
| `output/techpulse-daily-*.md` | ~100 generated reports from 2020-present | Archived news digests |

---

## 8. Deployment & Usage

### Installation

```bash
# 1. Clone & enter project
cd Latest_News_Tech

# 2. Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env from example
python main.py --init-env
# Edit .env with your credentials

# 5. Run once
python main.py

# 6. Run web dashboard
python web_app.py
# Open http://localhost:5000
```

### Dependencies (requirements.txt)

| Package | Version | Purpose |
|---------|---------|---------|
| `requests` | >=2.31.0 | HTTP client for web scraping & APIs |
| `beautifulsoup4` | >=4.12.0 | HTML parsing for web sources |
| `feedparser` | >=6.0.10 | RSS/Atom feed parsing |
| `pyyaml` | >=6.0 | YAML config file parsing |
| `schedule` | >=1.2.0 | Periodic scheduler for CLI mode |
| `python-dotenv` | >=1.0.0 | (Available but not used — custom parser used instead) |
| `rich` | >=13.0.0 | Terminal formatting (not actively used in code) |
| `flask` | >=3.0.0 | Web dashboard framework |
| `apscheduler` | >=3.10.0 | Cron scheduler for web mode |

**Optional Dependencies** (not in requirements.txt but used by code):

| Package | Used In | Purpose |
|---------|---------|---------|
| `openai` | `chat.py`, `generate_historical.py` | GPT-4o-mini API |
| `firecrawl` | `sources.py` | Clean article content to Markdown |
| `twilio` | `whatsapp_notifier.py` | WhatsApp Business API |
| `pywhatkit` | `whatsapp_notifier.py` | WhatsApp Web fallback |
| `python-dateutil` | `generate_historical_v2.py` | relativedelta for monthly stepping |

### Running Modes

| Command | Mode | Description |
|---------|------|-------------|
| `python main.py` | Once | Fetch news, generate report, send notifications |
| `python main.py --schedule` | Scheduled | Run daily at configured time (uses `schedule` lib) |
| `python main.py --test` | Test | 1 source per domain for quick testing |
| `python web_app.py` | Dashboard | Flask web UI + APScheduler on port 5000 |
| `python generate_historical.py` | Historical | Generate weekly reports 2024-2026 |
| `python generate_historical_v2.py` | Historical | Generate monthly reports 2020-2026 |

### Tech Stack Summary

```
Backend:      Python 3.14, Flask 3.x
Frontend:     Jinja2, Vanilla JavaScript, CSS3
Scheduler:    APScheduler 3.x (web), Schedule 1.x (CLI)
AI/ML:        OpenAI GPT-4o-mini (chat + generation)
Search:       Serper.dev (Google News API)
Scraping:     BeautifulSoup4, Firecrawl
Notification: SMTP (email), Twilio + pywhatkit (WhatsApp)
Data:         YAML (config), JSON (history), Markdown (reports)
Storage:      Local filesystem (output/*.md)
```

---

*End of Project Complete Guide — TechPulse Daily*
