import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).parent.parent
ENV_PATH = BASE_DIR / ".env"
load_dotenv(str(ENV_PATH))

class FreeConfig:
    # === FREE LLM: Google Gemini API (60 req/min, 1500/day) ===
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")

    # === FREE NEWS: NewsAPI.org (100 req/day) ===
    NEWSAPI_KEY: str = os.getenv("NEWSAPI_KEY", "")

    # === FREE SEARCH: Serper.dev (2500/month free) ===
    SERPER_API_KEY: str = os.getenv("SERPER_API_KEY", "")

    # === VECTOR DB: ChromaDB (local, free, open source) ===
    CHROMA_PERSIST_DIR: str = str(BASE_DIR / "enterprise_engine" / "data" / "chroma")

    # === DATABASE: SQLite (local, free) ===
    DB_PATH: str = str(BASE_DIR / "enterprise_engine" / "data" / "techintel.db")
    DATABASE_URL: str = f"sqlite:///{DB_PATH}"

    # === EMBEDDINGS: HuggingFace (free, local, all-MiniLM-L6-v2) ===
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"

    # === LLM SETTINGS ===
    LLM_MODEL: str = "gemini-2.5-flash"
    LLM_TEMPERATURE: float = 0.3
    LLM_MAX_TOKENS: int = 4096

    # === PIPELINE ===
    PIPELINE_INTERVAL_HOURS: int = 6
    MAX_ARTICLES_PER_CYCLE: int = 300
    CURATION_THRESHOLD: float = 40.0
    ALERT_THRESHOLD: float = 75.0

    # === FREE SOURCES ===
    RSS_FEEDS: list = [
        "https://techcrunch.com/feed/",
        "https://venturebeat.com/feed/",
        "https://www.wired.com/feed/rss",
        "https://www.theverge.com/rss/index.xml",
        "https://arstechnica.com/feed/",
        "https://www.space.com/feeds/all",
        "https://www.nasa.gov/feed/",
        "https://www.sciencedaily.com/rss/computers_math/artificial_intelligence.xml",
        "https://www.sciencedaily.com/rss/computers_math/quantum_computers.xml",
        "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml",
        "https://feeds.bloomberg.com/markets/news.rss",
        "https://www.newscientist.com/feed/home",
        "https://www.quantamagazine.org/feed/",
        "https://krebsonsecurity.com/feed/",
        "https://www.reddit.com/r/artificial/.rss",
        "https://www.reddit.com/r/MachineLearning/.rss",
        "https://www.reddit.com/r/quantum/.rss",
        "https://www.reddit.com/r/robotics/.rss",
        "https://www.reddit.com/r/Futurology/.rss",
        "https://www.reddit.com/r/technology/.rss",
        "https://www.reddit.com/r/AI_Agents/.rss",
        "https://www.reddit.com/r/LocalLLaMA/.rss",
        "https://www.reddit.com/r/cybersecurity/.rss",
        "https://www.reddit.com/r/singularity/.rss",
    ]

    NEWSAPI_QUERIES: list = [
        "artificial intelligence", "AI", "machine learning",
        "quantum computing", "robotics", "automation",
        "cybersecurity", "technology investment", "startup funding",
        "semiconductor", "cloud computing", "AI regulation",
        "autonomous vehicles", "space technology", "biotech",
        "renewable energy", "fintech", "blockchain",
        "electric vehicles", "5G", "IoT", "digital transformation",
    ]

config = FreeConfig()
