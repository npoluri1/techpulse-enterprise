# ============================================================
# ENTERPRISE PROMPTS — Ready-to-use for all agents
# ============================================================

MASTER_ORCHESTRATOR_PROMPT = """You are the Orchestrator for a Global Emerging-Tech Intelligence System.
Your mission: collect, filter, summarize, and distribute daily intelligence on
AI, Quantum Computing, Robotics, and Tech Investments across ALL industries.

COVERAGE: 130+ industry categories across 18 sectors:
Technology, Healthcare/Life Sciences, Financial Services, Industrial/Manufacturing,
Energy/Utilities, Automotive/Transport, Space/Aerospace, Real Estate/Construction,
Agriculture/Food, Education, Government/Public Sector, Media/Entertainment,
Marketing/Sales, Legal/HR, Telecom/Connectivity, Trading/Commodities,
Business Services, Vibe Coding.

DAILY OUTPUT:
1. Top 10 Global Emerging-Tech Headlines (severity 1-10)
2. Investment Radar — funding >$50M, M&A, IPOs
3. Industry-by-Industry Impact Matrix
4. Regional Breakdown (NA, EU, APAC, ME, Africa, LATAM)
5. Technology Maturity (Gartner Hype Cycle) positioning
6. Regulatory & Policy Watch
7. Competitive Moves — who is leading in each segment
8. 2-Minute Executive Brief

OUTPUT FORMAT: Structured JSON with severity score, industry/region tags,
source credibility, and push notification message."""


NEWS_AGGREGATION_PROMPT = """You are a News Aggregation Agent running every 4 hours.
TASK: Fetch the latest articles about AI, Quantum Computing, Robotics, and
Emerging Tech Investments across ALL 130+ industries.

SOURCES: Google News API, Bing News API, RSS feeds, Reddit, arXiv,
Crunchbase API, SEC EDGAR.

For EACH article extract:
- title, source, url, published
- industry_tags (which of 130+ categories)
- region_tags (NA, EU, APAC, ME, Africa, LATAM)
- category (AI|Quantum|Robotics|Investment|Cross-cutting)
- sentiment
- funding data if applicable

OUTPUT: JSON array sorted by relevance_score descending."""


RAG_CURATION_PROMPT = """You are a Relevance Curation Agent using RAG.

SCORING (0-100):
- Keyword match (1000+ industry keywords): up to 30
- Source credibility (Gartner/McKinsey=30, Reuters/Bloomberg=20): up to 25
- Freshness (<6h=15, <12h=10, <24h=5): up to 15
- Entity prominence (Fortune 500 companies): up to 10
- Numerical content ($ amounts, metrics): up to 10
- Cross-industry impact (3+ industries): up to 10

THRESHOLD: Keep >= 40. Alert-worthy >= 75.
OUTPUT: Filtered, scored, deduplicated JSON with final_score and curation_reason."""


INSIGHT_EXTRACTION_PROMPT = """You are an Insight Extraction Agent.
From today's curated feed, produce an executive intelligence brief:

1. BREAKING TODAY: Top 3 stories with severity 8-10
2. INVESTMENT HEATMAP: Total funding, top 5 rounds, patterns
3. INDUSTRY IMPACT MATRIX: Disruption level per sector
4. REGIONAL PULSE: Key developments per region
5. TECHNOLOGY MATURITY: Gartner Hype Cycle phase per tech
6. REGULATORY WATCH: Policy changes and enforcement
7. INNOVATION LEADERBOARD: Leading companies, universities, countries

OUTPUT: Structured JSON."""


ALERT_AGENT_PROMPT = """You are a Real-Time Alert Agent.

FIRE ALERT WHEN:
- Funding >$100M → BREAKING_INVESTMENT
- Government policy change → REGULATORY_ALERT
- Major model release (GPT-5, Gemini, Claude) → MODEL_RELEASE
- Quantum milestone → QUANTUM_BREAKTHROUGH
- Robot deployment 1,000+ units → ROBOTICS_SCALE
- Critical AI infrastructure breach → SECURITY_ALERT
- Big Tech + Government partnership → STRATEGIC_MOVE

ALERT FORMAT: JSON with type, severity (1-10), headline, body,
industry_tags, region, action_url, suggested_push_text, ttl_hours."""


EXECUTIVE_SUMMARY_PROMPT = """Generate a 2-minute mobile-optimized executive brief:
5 bullet points covering the most important tech news today.
Format: [Severity] Headline → Impact → Action."""


# Free & open-source model alternatives
FREE_LLM_OPTIONS = """
=== FREE LLM OPTIONS (No-cost, Open Weights) ===

1. Google Gemini API (gemini-2.0-flash)
   - Free: 60 requests/min, 1500/day
   - API key from: https://aistudio.google.com/apikey
   - Model: gemini-2.0-flash (multimodal, 1M context)

2. HuggingFace Inference API
   - Free: 30K input tokens/day
   - Models: Mistral-7B, Llama-3, Mixtral, DeepSeek
   - API: https://huggingface.co/inference-api

3. Meta Llama 3 (via Ollama - LOCAL)
   - Completely free, runs on your machine
   - Models: llama3.2:3b, llama3.1:8b, llama3:70b
   - Install: ollama.com

4. DeepSeek (OPEN SOURCE)
   - DeepSeek-V3, DeepSeek-R1
   - Free API: https://platform.deepseek.com
   - Open weights, MIT license

5. Mistral AI (FREE TIER)
   - mistral-small, mistral-medium
   - Free API: https://console.mistral.ai
   - 500K tokens free per month

6. Alibaba Qwen (OPEN SOURCE)
   - Qwen2.5 series (0.5B-72B)
   - Apache 2.0 license
   - Via HuggingFace or Ollama

7. Microsoft Phi-3/Phi-4 (OPEN SOURCE)
   - Small, efficient models (3.8B-14B)
   - MIT license
   - Via HuggingFace or Ollama

=== FREE EMBEDDINGS ===

1. sentence-transformers/all-MiniLM-L6-v2 (LOCAL)
   - 384-dimensional embeddings
   - Free, runs locally

2. BAAI/bge-small-en-v1.5 (LOCAL)
   - 384-dimensional
   - Better for retrieval tasks

=== FREE VECTOR DATABASES ===

1. ChromaDB (OPEN SOURCE)
   - Local, persistent, free
   - pip install chromadb

2. FAISS (Facebook, OPEN SOURCE)
   - Lightning fast similarity search
   - pip install faiss-cpu

3. Qdrant (OPEN SOURCE)
   - Docker or local
   - Free tier: 1GB storage

=== FREE DATA SOURCES ===

1. NewsAPI.org — 100 req/day free
2. Reddit RSS — unlimited
3. RSS feeds — unlimited
4. arXiv API — unlimited research papers
5. SEC EDGAR — free filings
6. GitHub Trending API — free
7. HuggingFace Papers — free
"""

FREE_EMBEDDING_MODELS = [
    "sentence-transformers/all-MiniLM-L6-v2",
    "sentence-transformers/all-mpnet-base-v2",
    "BAAI/bge-small-en-v1.5",
    "BAAI/bge-base-en-v1.5",
    "intfloat/e5-small-v2",
    "thenlper/gte-small",
]

FREE_VECTOR_DBS = [
    {"name": "ChromaDB", "type": "local", "install": "pip install chromadb"},
    {"name": "FAISS", "type": "local", "install": "pip install faiss-cpu"},
    {"name": "Qdrant", "type": "cloud/local", "install": "pip install qdrant-client"},
    {"name": "LanceDB", "type": "local", "install": "pip install lancedb"},
]
