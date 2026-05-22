# Enterprise Expansion Plan — Global AI Intelligence Platform

> **From TechPulse Daily → Enterprise-Grade Multi-Agent AI Intelligence System**
>
> **Covering:** 100+ Industries | Real-Time Data | Gartner Reports | Investment Tracking | Web + Mobile
>
> **Tech Stack:** LangGraph | LangChain | RAG | Vector DB | FastAPI | Next.js | Flutter | React

---

## Table of Contents

1. [Vision & Roadmap](#1-vision--roadmap)
2. [100+ Industry Categories Master List](#2-100-industry-categories-master-list)
3. [Enterprise Multi-Agent Architecture](#3-enterprise-multi-agent-architecture)
4. [Enterprise-Level Prompts (All Agents)](#4-enterprise-level-prompts-all-agents)
5. [LangGraph Orchestration Pipeline](#5-langgraph-orchestration-pipeline)
6. [RAG + Vector DB Implementation](#6-rag--vector-db-implementation)
7. [Data Sources & API Integration](#7-data-sources--api-integration)
8. [Web + Mobile Implementation Plan](#8-web--mobile-implementation-plan)
9. [Gartner Hype Cycle Integration](#9-gartner-hype-cycle-integration)
10. [Investment & Funding Tracking](#10-investment--funding-tracking)
11. [Complete Code Implementation](#11-complete-code-implementation)

---

## 1. Vision & Roadmap

### Current State (TechPulse Daily)
```
✅ 20 industry domains
✅ RSS + Web + Serper scraping
✅ Keyword-based curation
✅ Flask dashboard (web only)
✅ OpenAI GPT-4o-mini chat
✅ Email + WhatsApp notifications
✅ Historical archive
```

### Target State (Enterprise Platform)
```
🚀 100+ industry categories with sub-industries
🚀 Multi-agent LangGraph orchestration
🚀 RAG with Pinecone/Weaviate vector database
🚀 LangChain for agent tool use
🚀 Real-time data ingestion (6-hour cycles)
🚀 Next.js web dashboard + Flutter mobile app
🚀 Gartner Hype Cycle integration
🚀 Investment/funding tracking with Crunchbase
🚀 Push notifications (Firebase/OneSignal)
🚀 Sentiment analysis & trend detection
🚀 Executive daily brief (auto-generated)
```

### Implementation Phases

| Phase | Timeline | Deliverables |
|-------|----------|-------------|
| **P0 — Foundation** | Week 1-2 | 100+ industry config, multi-source ingestion, Vector DB setup |
| **P1 — Intelligence** | Week 3-4 | LangGraph agents, RAG pipeline, GPT-4o-mini → GPT-4o upgrade |
| **P2 — Frontend** | Week 5-6 | Next.js dashboard, Flutter mobile app, real-time updates |
| **P3 — Enterprise** | Week 7-8 | Gartner data, investment tracking, alert system, SSO auth |

---

## 2. 100+ Industry Categories Master List

### Core Categories (20 existing → expanded to 100+)

```
INDUSTRY_MASTER_CATEGORIES = {
    "technology": {
        "ai_agents": ["AI Agents", "Agentic AI", "Multi-Agent Systems", "AI Agent Frameworks",
                      "Autonomous Agents", "Agent Orchestration", "Agent Workflows"],
        "artificial_intelligence": ["Machine Learning", "Deep Learning", "Neural Networks",
                                     "Generative AI", "LLMs", "GPT", "Computer Vision", "NLP",
                                     "Speech Recognition", "Reinforcement Learning", "Transformer",
                                     "Diffusion Models", "Foundation Models", "Edge AI", "Federated Learning"],
        "quantum_computing": ["Quantum Hardware", "Quantum Software", "Quantum Algorithms",
                              "Quantum Error Correction", "Quantum Cryptography", "Quantum Sensors",
                              "Quantum Networking", "Topological Quantum", "Photonic Quantum",
                              "Trapped Ion", "Superconducting Qubits", "Quantum Annealing",
                              "Post-Quantum Cryptography", "Quantum Machine Learning"],
        "robotics": ["Humanoid Robots", "Industrial Robotics", "Collaborative Robots",
                     "Autonomous Mobile Robots", "Robotic Process Automation", "Surgical Robotics",
                     "Soft Robotics", "Swarm Robotics", "Drone Technology", "Exoskeletons",
                     "Robotic Vision", "Manipulation", "Robot Perception", "SLAM"],
        "semiconductor": ["Chip Design", "GPU", "TPU", "NPU", "Foundry", "TSMC", "ASML",
                          "Advanced Packaging", "Chiplets", "RISC-V", "ARM", "EUV Lithography",
                          "EDA Tools", "3D ICs", "HBM Memory", "Silicon Photonics"],
        "cybersecurity": ["Zero-Day", "Ransomware", "Threat Intelligence", "SOC", "SIEM",
                          "XDR", "EDR", "Cloud Security", "Network Security", "Identity Security",
                          "Zero Trust", "AI Security", "Supply Chain Security", "DevSecOps",
                          "Security Posture", "Vulnerability Management", "Penetration Testing",
                          "Bug Bounty", "Digital Forensics", "Incident Response"],
        "cloud_native": ["Cloud Computing", "Kubernetes", "Docker", "Serverless", "AWS",
                         "Azure", "GCP", "Microservices", "Service Mesh", "Istio", "Envoy",
                         "Terraform", "Helm", "ArgoCD", "GitOps", "FinOps", "Platform Engineering",
                         "eBPF", "WebAssembly", "Edge Computing"],
        "data_infrastructure": ["Data Engineering", "Data Lakes", "Data Warehouses", "Lakehouse",
                                "Apache Spark", "Kafka", "Flink", "dbt", "Airflow", "Snowflake",
                                "Databricks", "BigQuery", "Redshift", "Data Mesh", "Data Contracts",
                                "Data Observability", "Data Governance", "Data Quality"],
        "developer_tools": ["IDE", "Code Generation", "CI/CD", "Version Control", "API Management",
                            "Low-Code", "No-Code", "Open Source", "Package Management",
                            "Testing Automation", "Monitoring", "Observability", "APM"],
        "blockchain_web3": ["Blockchain", "DeFi", "NFT", "Smart Contracts", "Layer 2",
                            "zk-Rollups", "Bitcoin", "Ethereum", "Solana", "Web3", "DAOs",
                            "Tokenization", "Stablecoins", "CBDC"],
    },
    "healthcare_life_sciences": {
        "healthcare_ai": ["Medical Imaging AI", "Diagnostic AI", "Clinical Decision Support",
                          "Drug Discovery AI", "Genomics AI", "Precision Medicine", "Robotic Surgery",
                          "Hospital AI", "Health Informatics", "Telemedicine", "Remote Monitoring",
                          "EHR AI", "FDA AI Approvals", "Digital Pathology"],
        "biotech": ["Genomics", "Proteomics", "CRISPR", "Gene Therapy", "Synthetic Biology",
                    "Bioinformatics", "Computational Biology", "Personalized Medicine",
                    "Biomarkers", "Cell Therapy", "RNA Therapeutics"],
        "pharma": ["Drug Discovery", "Clinical Trials", "Pharma AI", "FDA Approvals",
                   "Regulatory Affairs", "Pharma Supply Chain", "Real World Evidence"],
        "medtech": ["Medical Devices", "Wearables", "Diagnostic Equipment", "Imaging Systems",
                    "Patient Monitoring", "Point of Care"],
        "neurotech": ["Brain-Computer Interfaces", "Neuroimaging", "Neural Implants",
                      "Neural Networks", "Cognitive Computing", "Neuromodulation"],
        "longevity": ["Anti-Aging", "Longevity Research", "Regenerative Medicine",
                      "Senolytics", "Epigenetics", "Telomere Research"],
    },
    "financial_services": {
        "fintech": ["Digital Payments", "Mobile Banking", "Neobanks", "Open Banking",
                    "Embedded Finance", "Payments Infrastructure", "Cross-Border Payments",
                    "BNPL", "Digital Wallets"],
        "insurtech": ["AI Underwriting", "Claims Automation", "Usage-Based Insurance",
                      "Parametric Insurance", "Insurance Analytics"],
        "wealthtech": ["Robo-Advisors", "Wealth Management", "Trading Platforms",
                       "Portfolio Optimization", "Alternative Investments"],
        "regtech": ["Compliance Automation", "AML/KYC", "Regulatory Reporting",
                    "Risk Management", "Fraud Detection"],
        "defi": ["Decentralized Finance", "Lending Protocols", "DEX", "Yield Farming",
                 "Liquid Staking", "Stablecoins"],
    },
    "industrial_manufacturing": {
        "industry_4_0": ["Smart Factory", "Digital Twin", "Predictive Maintenance",
                         "Industrial IoT", "SCADA", "MES", "PLC", "Industrial Automation"],
        "additive_manufacturing": ["3D Printing", "4D Printing", "Additive Manufacturing",
                                   "Metal 3D Printing", "Bioprinting"],
        "mechanical_engineering": ["CAD/CAM", "Finite Element Analysis", "Thermodynamics",
                                   "Fluid Dynamics", "Machine Design", "Robotics Mechanics"],
        "electrical_engineering": ["Power Systems", "Circuit Design", "Embedded Systems",
                                    "VLSI Design", "Power Electronics"],
        "electronic_engineering": ["PCB Design", "Electronic Components", "Sensors",
                                   "Actuators", "Signal Processing", "RF Engineering"],
        "civil_engineering": ["Structural Engineering", "Construction Tech", "BIM",
                              "Smart Infrastructure", "Geotechnical Engineering"],
        "supply_chain": ["Logistics AI", "Warehouse Automation", "Last Mile Delivery",
                         "Inventory Optimization", "Supply Chain Visibility"],
    },
    "energy_utilities": {
        "renewable_energy": ["Solar Energy", "Wind Energy", "Hydropower", "Geothermal",
                             "Wave Energy", "Tidal Energy"],
        "nuclear_energy": ["Nuclear Fission", "Nuclear Fusion", "SMR", "Nuclear Safety",
                           "Thorium Reactors"],
        "hydrogen": ["Green Hydrogen", "Blue Hydrogen", "Hydrogen Fuel Cells",
                     "Hydrogen Storage", "Hydrogen Infrastructure"],
        "battery_tech": ["Lithium-Ion", "Solid-State", "Sodium-Ion", "Flow Batteries",
                         "Battery Recycling", "Energy Storage Systems"],
        "carbon_capture": ["Direct Air Capture", "Point Source Capture", "Carbon Storage",
                           "Carbon Utilization", "CCUS"],
        "smart_grid": ["Grid Modernization", "Smart Meters", "Demand Response",
                       "Microgrids", "Grid Edge", "Energy Management"],
        "clean_tech": ["Clean Technology", "Sustainable Tech", "Green Tech",
                       "Climate Tech", "Environmental Tech"],
    },
    "automotive_transport": {
        "automotive": ["Electric Vehicles", "Autonomous Driving", "ADAS", "Vehicle AI",
                       "Connected Cars", "V2X", "LIDAR", "Radar", "Camera Systems"],
        "autonomous_vehicles": ["Self-Driving Cars", "Robotaxis", "Autonomous Trucks",
                                "Autonomous Shuttles", "Autonomous Delivery", "Waymo",
                                "Tesla FSD", "Cruise", "Zoox", "Aurora"],
        "e_mobility": ["E-Scooters", "E-Bikes", "Electric Motorcycles", "Micromobility",
                       "Charging Infrastructure", "Battery Swapping"],
        "aviation": ["Electric Aviation", "Urban Air Mobility", "eVTOL", "Drones",
                     "Air Taxis", "Sustainable Aviation Fuel", "Autonomous Flight"],
        "maritime": ["Autonomous Ships", "Smart Ports", "Maritime AI",
                     "Green Shipping", "Maritime Logistics"],
        "railway": ["High-Speed Rail", "Smart Railways", "Autonomous Trains",
                    "Railway AI", "Rail Signaling"],
    },
    "space_aerospace": {
        "space_exploration": ["SpaceX", "NASA", "Mars Mission", "Lunar Mission",
                              "Artemis", "Starship", "Deep Space", "Asteroid Mining"],
        "satellite": ["Satellite Communications", "Starlink", "Earth Observation",
                      "Remote Sensing", "Satellite IoT", "LEO Satellites"],
        "aerospace": ["Aircraft", "Avionics", "Propulsion", "Aerospace Manufacturing",
                      "Defense Aerospace"],
        "space_commerce": ["Space Tourism", "Commercial Space", "Space Stations",
                           "Space Manufacturing", "In-Space Services"],
    },
    "real_estate_construction": {
        "proptech": ["Real Estate AI", "Property Management", "Smart Buildings",
                     "Real Estate Analytics", "Property Valuation AI"],
        "construction_tech": ["Construction AI", "Building Information Modeling",
                              "Modular Construction", "Smart Construction", "Robotic Construction"],
        "smart_cities": ["Urban AI", "City IoT", "Smart Infrastructure", "Urban Mobility",
                         "Public Safety Tech", "Waste Management Tech"],
    },
    "agriculture_food": {
        "agritech": ["Precision Agriculture", "Farm AI", "Smart Farming", "Agricultural Robots",
                     "Drone Farming", "Soil Sensors", "Crop Monitoring"],
        "foodtech": ["Alternative Protein", "Cultivated Meat", "Plant-Based", "Food AI",
                     "Food Safety", "Smart Kitchen", "Food Delivery Tech"],
        "vertical_farming": ["Indoor Farming", "Hydroponics", "Aeroponics", "Aquaponics",
                             "Controlled Environment Ag"],
    },
    "education": {
        "edtech": ["AI in Education", "Learning Management", "Personalized Learning",
                   "Adaptive Learning", "EdTech AI", "Online Learning", "Learning Analytics"],
        "corporate_training": ["Enterprise Learning", "LMS", "AI Training", "Skills Tech",
                               "Microlearning", "VR Training"],
    },
    "government_public": {
        "govtech": ["Government AI", "Digital Government", "Smart Government",
                    "Public Sector Tech", "E-Governance", "Civic Tech"],
        "defense_tech": ["Defense AI", "Military Tech", "C4ISR", "Defense Cybersecurity",
                         "Autonomous Weapons", "Defense Drones"],
        "public_safety": ["Emergency Response", "Police Tech", "Fire Tech", "Disaster Tech",
                          "Predictive Policing"],
    },
    "media_entertainment": {
        "media_tech": ["AI in Media", "Content Creation AI", "News AI", "Journalism Tech"],
        "gaming": ["Game Development", "Game AI", "Cloud Gaming", "Game Engines",
                   "Unity", "Unreal Engine", "Procedural Generation"],
        "entertainment": ["Streaming AI", "Recommendation AI", "Content Moderation",
                          "Digital Media", "Music AI", "Video AI"],
        "sportstech": ["Sports Analytics", "Athlete AI", "Smart Stadiums", "Wearable Sports",
                       "Esports Tech"],
    },
    "marketing_sales": {
        "martech": ["Marketing AI", "Marketing Automation", "CRM AI", "Customer Analytics",
                    "Personalization", "Content Marketing", "SEO AI", "Ad Tech"],
        "adtech": ["Programmatic Advertising", "Ad AI", "Demand Side Platforms",
                   "Supply Side Platforms", "Ad Attribution"],
        "sales_tech": ["Sales AI", "Sales Intelligence", "Conversation AI", "Revenue Intelligence",
                       "CPQ", "Sales Engagement"],
    },
    "legal_hr": {
        "legaltech": ["Legal AI", "Contract Analysis", "Legal Research", "E-Discovery",
                      "Compliance Tech", "Legal Analytics"],
        "hrtech": ["HR AI", "Talent Analytics", "Recruitment AI", "People Analytics",
                   "Workforce Planning", "Employee Experience", "Payroll Tech"],
    },
    "telecom_connectivity": {
        "telecom": ["5G", "6G", "Telecom AI", "Network Automation", "Open RAN",
                    "Private Networks", "Network Slicing"],
        "iot": ["Internet of Things", "Industrial IoT", "Smart Home", "IoT Platforms",
                "Edge Devices", "IoT Security"],
    },
    "real_estate_property": {
        "commercial_real_estate": ["Office Tech", "Retail Real Estate", "Industrial Real Estate",
                                    "CRE Tech", "Smart Buildings"],
        "residential_real_estate": ["Smart Homes", "Home Tech", "Residential Proptech",
                                     "Property Management", "Real Estate Marketplace"],
    },
    "trading_commodities": {
        "algorithmic_trading": ["Quant Trading", "AI Trading", "High Frequency Trading",
                                "Trading Bots", "Market Making"],
        "commodities": ["Oil Trading", "Gold Trading", "Commodity AI", "Supply & Demand Analytics",
                        "Commodity Markets"],
        "crypto_trading": ["Crypto Exchanges", "Trading Bots", "Market Analysis",
                           "Token Trading", "Derivatives"],
    },
    "business_services": {
        "consulting": ["AI Consulting", "Digital Transformation", "Strategy Consulting",
                       "Tech Consulting", "Management Consulting"],
        "accounting_finance": ["Accounting AI", "Audit AI", "Financial Planning",
                                "Tax Tech", "CFO Tech"],
        "legal_services": ["Law Firm Tech", "Legal Practice", "IP Tech", "Litigation Tech"],
    },
}
```

### Total Coverage: **130+ Categories** | **1,000+ Keywords**

---

## 3. Enterprise Multi-Agent Architecture

```
┌──────────────────────────────────────────────────────────────────────────┐
│                     ENTERPRISE AI INTELLIGENCE PLATFORM                    │
│                                                                            │
│  ┌───────────────────── LangGraph Orchestrator ───────────────────────┐   │
│  │                                                                      │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────┐  │   │
│  │  │  News    │  │  Curator │  │  Insight │  │  Alert   │  │Report│  │   │
│  │  │ Aggregat │──►│ Agent    │──►│Extract   │──►│Agent     │──►│Gen   │  │   │
│  │  │ ion Agent│  │ (RAG)    │  │ Agent     │  │(Real-    │  │Agent │  │   │
│  │  └──────────┘  └──────────┘  └──────────┘  │ time)    │  └──────┘  │   │
│  │                                              └──────────┘           │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                            │
│  ┌─────────────────── Data Layer ──────────────────────────────────┐      │
│  │                                                                  │      │
│  │  ┌────────┐  ┌──────────┐  ┌──────────┐  ┌─────────────────┐   │      │
│  │  │Postgre │  │Pinecone  │  │Elastic-  │  │Redis (Cache)    │   │      │
│  │  │SQL     │  │Vector DB │  │search    │  │+ Pub/Sub        │   │      │
│  │  └────────┘  └──────────┘  └──────────┘  └─────────────────┘   │      │
│  └──────────────────────────────────────────────────────────────────┘      │
│                                                                            │
│  ┌─────────────────── Source Ingestion ─────────────────────────────┐     │
│  │                                                                   │     │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────┐   │     │
│  │  │Google    │ │Bing News │ │Gartner   │ │Crunchbase│ │arXiv │   │     │
│  │  │News API  │ │API       │ │RSS/API   │ │API       │ │RSS   │   │     │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────┘   │     │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────┐   │     │
│  │  │TechCrunch│ │Reddit RSS│ │IEEE      │ │GitHub    │ │SEC   │   │     │
│  │  │RSS       │ │          │ │Spectrum  │ │Trending  │ │Filings│   │     │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────┘   │     │
│  └───────────────────────────────────────────────────────────────────┘     │
│                                                                            │
│  ┌─────────────────── Delivery Layer ───────────────────────────────┐     │
│  │                                                                   │     │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌─────────────────┐  │     │
│  │  │ Next.js  │  │ Flutter  │  │PWA (Web) │  │Push Notifications│  │     │
│  │  │ Dashboard│  │ Mobile   │  │          │  │(Firebase)        │  │     │
│  │  └──────────┘  └──────────┘  └──────────┘  └─────────────────┘  │     │
│  └───────────────────────────────────────────────────────────────────┘     │
└──────────────────────────────────────────────────────────────────────────┘
```

### Agent State Graph (LangGraph)

```
from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Optional

class AgentState(TypedDict):
    raw_articles: List[dict]
    curated_articles: List[dict]
    insights: dict
    alerts: List[dict]
    report: str
    industries: List[str]
    regions: List[str]
    errors: List[str]

workflow = StateGraph(AgentState)

# Define nodes
workflow.add_node("news_aggregation", NewsAggregationAgent)
workflow.add_node("curation_rag", CuratorRAGAgent)
workflow.add_node("insight_extraction", InsightExtractionAgent)
workflow.add_node("alert_generation", AlertAgent)
workflow.add_node("report_generation", ReportGenerationAgent)

# Define edges
workflow.set_entry_point("news_aggregation")
workflow.add_edge("news_aggregation", "curation_rag")
workflow.add_edge("curation_rag", "insight_extraction")
workflow.add_conditional_edges(
    "insight_extraction",
    should_trigger_alerts,
    {"alert": "alert_generation", "skip": "report_generation"}
)
workflow.add_edge("alert_generation", "report_generation")
workflow.add_edge("report_generation", END)
```

---

## 4. Enterprise-Level Prompts (All Agents)

### 4.1 Master Orchestration Prompt

```python
ORCHESTRATOR_SYSTEM_PROMPT = """You are the Orchestrator for a Global Emerging-Tech Intelligence System.
Your mission: collect, filter, summarize, and distribute daily intelligence on
AI, Quantum Computing, Robotics, and Tech Investments across ALL industries.

INDUSTRIES (130+ categories across 18 sectors):
Technology: AI Agents, Artificial Intelligence, Quantum Computing, Robotics,
  Semiconductor, Cybersecurity, Cloud Native, Data Infrastructure,
  Developer Tools, Blockchain/Web3
Healthcare: Healthcare AI, Biotech, Pharma, MedTech, NeuroTech, Longevity
Financial: Fintech, InsurTech, WealthTech, RegTech, DeFi
Industrial: Industry 4.0, Additive Manufacturing, Mechanical Eng,
  Electrical Eng, Electronic Eng, Civil Eng, Supply Chain
Energy: Renewable Energy, Nuclear, Hydrogen, Battery Tech, Carbon Capture,
  Smart Grid, Clean Tech
Transport: Automotive, Autonomous Vehicles, E-Mobility, Aviation, Maritime, Railway
Space: Space Exploration, Satellite, Aerospace, Space Commerce
Real Estate: PropTech, Construction Tech, Smart Cities
Agriculture: AgriTech, FoodTech, Vertical Farming
Education: EdTech, Corporate Training
Government: GovTech, Defense Tech, Public Safety
Media: Media Tech, Gaming, Entertainment, SportsTech
Marketing: MarTech, AdTech, Sales Tech
Legal/HR: LegalTech, HRTech
Telecom: 5G/6G, IoT
Trading: Algorithmic Trading, Commodities, Crypto Trading
Business: Consulting, Accounting, Legal Services

REQUIRED DAILY OUTPUT:
1. Top 10 Global Emerging-Tech Headlines (with severity 1-10)
2. Investment Radar — funding >$50M, M&A, IPOs (with amounts in USD)
3. Industry-by-Industry Impact Matrix (disruption level per sector)
4. Regional Breakdown (NA, EU, APAC, ME, Africa, LATAM)
5. Gartner Hype Cycle positioning for each technology
6. Regulatory & Policy Watch
7. Competitive Moves — who is leading in each segment
8. 2-Minute Executive Brief (mobile-optimized)

SOURCES: Gartner, McKinsey, BCG, Deloitte, PwC, IEEE Spectrum,
MIT Technology Review, Nature, Science, arXiv, Crunchbase, TechCrunch,
Reuters, Bloomberg, Financial Times, Nikkei, Caixin, YourStory,
TechInAsia, Menabytes, GitHub Trending, Hugging Face Papers,
Google AI Blog, OpenAI Blog, DeepMind Blog, Quantum Insider,
The Quantum Daily, Robot Report, The Verge, Wired, SEC Filings.

OUTPUT: Structured JSON with severity score, industry tags, region tags,
source credibility score, and suggested push notification message."""
```

### 4.2 News Aggregation Agent Prompt

```python
NEWS_AGGREGATION_PROMPT = """You are a News Aggregation Agent running every 4 hours.

TASK: Fetch the latest 500+ articles about AI, Quantum Computing, Robotics,
Emerging Tech, and Investments across ALL 130+ industries.

REQUIRED SOURCES (parallel fetch):
- Google News API: query per industry group (20 queries)
- Bing News API: trending tech topics
- Gartner RSS: emerging tech research
- Crunchbase API: funding rounds
- arXiv: latest papers (cs.AI, quant-ph, cs.RO, cs.LG)
- TechCrunch RSS + VentureBeat RSS + Wired RSS
- Reddit RSS: r/artificial, r/MachineLearning, r/quantum, r/robotics
- SEC EDGAR API: 8-K filings mentioning AI/quantum/robotics
- GitHub Trending: repositories

For EACH article, extract:
{{
  "article_id": "hash(unique)",
  "title": "string",
  "source": "string",
  "source_type": "rss|api|web_scrape",
  "url": "string",
  "published": "ISO8601",
  "full_text": "string (cleaned via Firecrawl/Newspaper3k)",
  "summary": "string (first 500 chars)",
  "industry_tags": ["list", "of", "matched", "categories"],
  "region_tags": ["North America", "APAC", "EU", "ME", "Africa", "LATAM"],
  "category": "AI|Quantum|Robotics|Investment|Cross-cutting",
  "sentiment": "positive|negative|neutral",
  "relevance_score": 0-100 (initial estimate),
  "has_funding_data": bool,
  "has_regulatory_impact": bool,
  "key_entities": ["company_names", "people", "countries"],
  "source_credibility": 1-30 (Gartner/McKinsey=30, IEEE/Nature=25,
    Reuters/Bloomberg=20, TechCrunch/Wired=15, blog=5),
}}

FUNDING EXTRACTION (if applicable):
{{
  "funding_amount_usd": float,
  "funding_round": "Seed|Series_A|Series_B|Series_C|Series_D|Series_E|Series_F|IPO|Grant|Debt|M&A",
  "lead_investors": ["list"],
  "valuation_usd": float (if disclosed),
  "funding_date": "ISO8601",
}}

OUTPUT: JSON array of articles sorted by initial relevance_score.
LIMIT: Top 500 articles per cycle."""
```

### 4.3 RAG Curation Agent Prompt

```python
RAG_CURATION_PROMPT = """You are a Relevance Curation Agent using RAG.

TASK: Score, deduplicate, and semantically rank the raw article feed.

STEP 1 — SEMANTIC DEDUPLICATION:
For each incoming article:
1. Generate embedding via OpenAI text-embedding-3-large
2. Query Pinecone vector DB for cosine similarity > 0.85
3. If duplicate found: keep higher-scored, drop lower

STEP 2 — MULTI-DIMENSIONAL SCORING:
SCORE = sum of:
- Keyword Score (max 30): Matches in 1000+ keyword list
  +5 per keyword in title, +2 per keyword in summary
- Source Credibility (max 25): Based on source tier
- Freshness (max 15):
  +15 for <6 hours, +10 for <12h, +5 for <24h, +0 for >24h
- Entity Prominence (max 10):
  +5 per Fortune 500 company mentioned
  +2 per notable person/executive
- Numerical Content (max 10):
  +10 if contains $ amounts, performance metrics, dates
  +5 if mentions percentages or statistics
- Cross-Industry Impact (max 10):
  +10 if affects 3+ industries
  +5 if affects 2 industries
  +0 if single industry

STEP 3 — THRESHOLD:
Keep articles with final_score >= 40
For "Alert-worthy": score >= 75

OUTPUT: Filtered, scored, deduplicated article list with:
  - final_score (0-100)
  - curation_reason: "string explaining top scoring factors"
  - industry_impact_level: "None|Low|Medium|High|Transformative"
  - alert_worthy: bool (true if score >= 75)

Store in PostgreSQL + embed + store vector in Pinecone."""
```

### 4.4 Insight Extraction Agent Prompt

```python
INSIGHT_EXTRACTION_PROMPT = """You are an Insight Extraction Agent.
From today's curated feed (500+ → 200+ curated articles), produce an
executive intelligence brief with these sections:

1. 🔥 BREAKING TODAY (Top 3, severity 8-10):
   For each: What happened, why it matters, which industries affected,
   recommended action for C-suite.

2. 📊 INVESTMENT HEATMAP:
   - Total disclosed funding today: $X.XXB
   - Top 5 rounds by size (company, amount, round type, investors)
   - Emerging patterns: "Capital flowing from X to Y"
   - 7-day trend: funding volume compared to previous week
   - IPOs in pipeline

3. 🏭 INDUSTRY IMPACT MATRIX (all 18 sectors):
   Per sector:
   {{
     "sector": "Technology",
     "disruption_level": "None|Low|Medium|High|Transformative",
     "key_development": "string",
     "affected_sub_industries": ["list"],
     "c_suite_recommendation": "string",
     "urgency": 1-10,
   }}

4. 🌍 REGIONAL PULSE:
   - North America: Regulation, Big Tech moves, VC activity
   - Europe: EU AI Act, GDPR, Horizon Europe
   - APAC: China/US tech war, Japan/India startup ecosystem
   - Middle East: Sovereign wealth funds, NEOM, AI cities
   - Africa: Leapfrog tech, fintech boom
   - LATAM: Digital transformation, crypto adoption

5. 🧬 TECHNOLOGY MATURITY (Gartner Hype Cycle):
   Per technology category:
   {{
     "tech": "Quantum Computing",
     "phase": "Innovation Trigger|Peak of Inflated Expectations|
        Trough of Disillusionment|Slope of Enlightenment|
        Plateau of Productivity",
     "years_to_plateau": "2-5|5-10|10+",
     "key_evidence": ["quotes", "metrics", "citations"],
   }}

6. ⚠️ REGULATORY & RISK WATCH:
   - New laws/regulations passed or proposed
   - Enforcement actions (SEC, FTC, EU Commission)
   - Export controls (CHIPS Act, China restrictions)
   - Cybersecurity threats to AI infrastructure
   - IP litigation and patent disputes

7. 🏆 INNOVATION LEADERBOARD:
   - Companies gaining AI talent share
   - Universities leading in quantum publications
   - Countries with largest AI compute investment
   - Most active corporate VC arms

OUTPUT: Structured JSON with markdown-ready summary strings."""
```

### 4.5 Alert Agent Prompt (Real-Time)

```python
ALERT_AGENT_PROMPT = """You are a Real-Time Alert Agent monitoring the article stream.

FIRE IMMEDIATE ALERT WHEN any condition is met:

🚨 BREAKING INVESTMENT (Severity 8-10):
  - Funding round > $100M in AI/Quantum/Robotics
  - Mega-round > $500M in any emerging tech
  - IPO filing by AI/quantum/robotics company
  - SPAC merger with tech company

🚨 REGULATORY ALERT (Severity 7-10):
  - Government policy change affecting tech
  - Export control expansion (CHIPS Act, entity list)
  - AI safety/compliance law passed
  - Data privacy regulation change

🚨 MODEL RELEASE (Severity 7-10):
  - Frontier model release (GPT-5, Gemini Ultra, Claude 4, Llama 4, etc.)
  - Open-source model matching proprietary performance
  - Model with new capability (multimodal, reasoning, agentic)

🚨 QUANTUM BREAKTHROUGH (Severity 8-10):
  - Verified quantum advantage/supremacy claim
  - Error correction milestone (below threshold)
  - New qubit record (1000+ logical qubits)

🚨 ROBOTICS SCALE (Severity 7-9):
  - 1,000+ robot deployment at single site
  - Humanoid robot entering commercial production
  - Autonomous vehicle regulatory approval in new region

🚨 SECURITY ALERT (Severity 8-10):
  - Major vulnerability in AI infrastructure
  - Supply chain attack on ML libraries
  - Critical infrastructure AI breach

🚨 STRATEGIC MOVE (Severity 6-8):
  - Big Tech + Government partnership
  - Major acquisition ( > $1B )
  - Key executive move (hiring at competitor)

ALERT FORMAT:
{{
  "type": "BREAKING_INVESTMENT|REGULATORY_ALERT|MODEL_RELEASE|
           QUANTUM_BREAKTHROUGH|ROBOTICS_SCALE|SECURITY_ALERT|
           STRATEGIC_MOVE",
  "severity": 1-10,
  "headline": "string (max 100 chars)",
  "body": "string (2-sentence summary)",
  "industry_tags": ["list"],
  "region": "string",
  "action_url": "link to full article",
  "suggested_push_text": "string (max 120 chars for mobile)",
  "ttl_hours": 24,
  "requires_immediate_notification": bool,
  "notification_channels": ["push|email|sms|slack|teams"],
}}"""
```

### 4.6 Report Generation Agent Prompt

```python
REPORT_GENERATION_PROMPT = """You are a Report Generation Agent.
Convert today's full intelligence into multiple output formats.

FORMAT 1 — Full Daily Brief (Markdown):
# 🧠 Global AI Intelligence Brief — {date}

## 🔥 Breaking Today
...

## 📊 Investment Heatmap
...

## 🏭 Industry Impact Matrix
...

## 🌍 Regional Pulse
...

## 🧬 Technology Maturity
...

## ⚠️ Regulatory Watch
...

## 🏆 Innovation Leaderboard
...

---

FORMAT 2 — Executive Summary (2-min read):
📡 Daily Tech Pulse — {date}
⚡ [Severity N] Headline → Impact → Action
...

FORMAT 3 — Mobile Push Brief:
5 bullet points, emoji per category, max 500 chars total

FORMAT 4 — JSON API Response:
Full structured data for dashboard consumption

FORMAT 5 — Audio Script (90 seconds):
For text-to-speech / podcast generation"""
```

### 4.7 Visualization Agent Prompt

```python
VISUALIZATION_PROMPT = """You are a Visualization Agent. Generate dashboard charts.

REQUIRED CHARTS (as Plotly JSON):

1. AI Investment by Industry (Treemap)
   - Hierarchy: Sector → Industry → Company
   - Value: Total funding USD
   - Color: Funding growth % (green=high, red=declining)

2. Quantum Readiness by Country (Choropleth)
   - Metrics: Patents + Funding + Publications (normalized)
   - Color scale: Dark blue=high readiness

3. Robotics Deployment by Sector (Horizontal Bar)
   - Y-axis: Industry sectors
   - X-axis: Number of deployed units
   - Color: Year-over-year growth

4. News Volume Trend (30-day Line Chart)
   - Lines: AI, Quantum, Robotics, Investments
   - Y-axis: Article count
   - Annotations: Major events

5. Technology Maturity Radar (Radar/Spider)
   - Axes: Each major tech category
   - Value: Maturity score 0-100
   - Overlay: Current position vs 6 months ago

6. Entity Network Graph (Force-Directed)
   - Nodes: Companies, Investors, Industries
   - Edges: Funding, Partnership, Acquisition
   - Size: Market cap / funding amount

7. Sentiment Timeline (Stacked Area)
   - Positive / Neutral / Negative
   - Per industry category
   - Time range: 30 days

8. Regulatory Activity Map (World Heatmap)
   - Countries colored by number of regulatory actions
   - Annotations: Key regulations

9. Funding Round Distribution (Sunburst)
   - Inner: Round type (Seed → Series A → ... → IPO)
   - Middle: Industry sector
   - Outer: Region

10. Top Movers (Table + Bar)
    - Companies with largest valuation changes
    - Biggest funding rounds
    - Most mentioned companies

OUTPUT: JSON with Plotly traces, layout, and insight_text per chart."""
```

---

## 5. LangGraph Orchestration Pipeline

### Complete Python Implementation

```python
# enterprise_engine/orchestrator.py
import os
import json
import logging
from datetime import datetime, timedelta
from typing import TypedDict, List, Optional, Dict, Any
from zoneinfo import ZoneInfo

from langgraph.graph import StateGraph, END
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Pinecone
from langchain_community.document_loaders import RSSFeedLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.tools import Tool
from langchain.agents import AgentExecutor, create_openai_tools_agent

import pinecone
import requests
from bs4 import BeautifulSoup
import feedparser

from sqlalchemy import create_engine, Column, String, Float, DateTime, JSON, Boolean, Text
from sqlalchemy.orm import declarative_base, sessionmaker

# ============================================================
# CONFIGURATION
# ============================================================

SGT = ZoneInfo("Asia/Singapore")
logger = logging.getLogger("EnterpriseOrchestrator")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY", "")
PINECONE_INDEX = os.getenv("PINECONE_INDEX", "tech-intel")
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost/techintel")
SERPER_API_KEY = os.getenv("SERPER_API_KEY", "")
BING_API_KEY = os.getenv("BING_API_KEY", "")
CRUNCHBASE_API_KEY = os.getenv("CRUNCHBASE_API_KEY", "")

# ============================================================
# DATA MODELS
# ============================================================

Base = declarative_base()

class Article(Base):
    __tablename__ = "articles"

    id = Column(String, primary_key=True)
    title = Column(String(500))
    url = Column(Text, unique=True)
    source = Column(String(200))
    source_type = Column(String(50))
    published = Column(DateTime)
    summary = Column(Text)
    full_text = Column(Text, nullable=True)
    industry_tags = Column(JSON)
    region_tags = Column(JSON)
    category = Column(String(100))
    sentiment = Column(String(20))
    relevance_score = Column(Float)
    final_score = Column(Float, nullable=True)
    curation_reason = Column(Text, nullable=True)
    funding_amount_usd = Column(Float, nullable=True)
    funding_round = Column(String(50), nullable=True)
    has_regulatory_impact = Column(Boolean, default=False)
    key_entities = Column(JSON)
    source_credibility = Column(Float)
    embedding_id = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(String, primary_key=True)
    type = Column(String(100))
    severity = Column(Integer)
    headline = Column(String(200))
    body = Column(Text)
    industry_tags = Column(JSON)
    region = Column(String(100))
    action_url = Column(Text)
    suggested_push_text = Column(String(200))
    ttl_hours = Column(Integer, default=24)
    sent = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

# ============================================================
# LANGGRAPH STATE
# ============================================================

class EnterpriseState(TypedDict):
    run_id: str
    started_at: str
    completed_at: Optional[str]
    raw_articles: List[Dict[str, Any]]
    curated_articles: List[Dict[str, Any]]
    insights: Dict[str, Any]
    alerts: List[Dict[str, Any]]
    report: Dict[str, Any]
    industries: List[str]
    regions: List[str]
    sources_used: List[str]
    errors: List[str]

# ============================================================
# AGENT 1: NEWS AGGREGATION
# ============================================================

class NewsAggregationAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4o",
            temperature=0.1,
            api_key=OPENAI_API_KEY
        )
        self.sources = [
            self.fetch_google_news,
            self.fetch_bing_news,
            self.fetch_rss_feeds,
            self.fetch_crunchbase,
            self.fetch_arxiv,
            self.fetch_sec_filings,
        ]

    def __call__(self, state: EnterpriseState) -> EnterpriseState:
        all_articles = []
        errors = []

        for source_fn in self.sources:
            try:
                articles = source_fn()
                all_articles.extend(articles)
                logger.info(f"Fetched {len(articles)} from {source_fn.__name__}")
            except Exception as e:
                errors.append(f"{source_fn.__name__}: {str(e)}")
                logger.error(f"Source failed: {source_fn.__name__}: {e}")

        # Deduplicate by URL
        seen_urls = set()
        unique_articles = []
        for a in all_articles:
            if a["url"] not in seen_urls:
                seen_urls.add(a["url"])
                unique_articles.append(a)

        # Initial relevance scoring
        scored = self.initial_score(unique_articles)
        scored.sort(key=lambda x: x["relevance_score"], reverse=True)

        state["raw_articles"] = scored[:500]
        state["errors"] = errors
        return state

    def initial_score(self, articles: List[Dict]) -> List[Dict]:
        """Quick keyword-based pre-filter before expensive RAG"""
        MASTER_KEYWORDS = [
            "ai", "artificial intelligence", "machine learning", "deep learning",
            "quantum", "robot", "automation", "autonomous",
            "investment", "funding", "series", "ipo", "valuation",
            "breakthrough", "innovation", "startup", "technology",
            "gartner", "mckinsey", "forrester",
            "llm", "gpt", "generative", "neural",
            "chip", "semiconductor", "processor", "gpu",
            "cloud", "kubernetes", "serverless",
            "cyber", "security", "ransomware", "breach",
            "blockchain", "defi", "crypto", "web3",
        ]

        HIGH_VALUE_SOURCES = {
            "gartner": 30, "mckinsey": 30, "bcg": 25, "deloitte": 25,
            "ieee": 25, "nature": 25, "science": 25,
            "reuters": 20, "bloomberg": 20, "ft": 20,
            "techcrunch": 15, "wired": 15, "venturebeat": 15,
            "mit": 20, "stanford": 20,
        }

        for article in articles:
            score = 0
            text = (article.get("title", "") + " " + article.get("summary", "")).lower()

            # Keyword matches
            for kw in MASTER_KEYWORDS:
                if kw in text:
                    score += 5
                    if kw in article.get("title", "").lower():
                        score += 10

            # Source credibility
            source_lower = article.get("source", "").lower()
            for src_key, cred in HIGH_VALUE_SOURCES.items():
                if src_key in source_lower:
                    score += cred
                    break

            # Freshness bonus
            published = article.get("published")
            if published:
                try:
                    age = datetime.now(SGT) - datetime.fromisoformat(published.replace("Z", "+00:00"))
                    if age < timedelta(hours=6): score += 15
                    elif age < timedelta(hours=12): score += 10
                    elif age < timedelta(hours=24): score += 5
                except:
                    pass

            # Numbers in content = +10
            if any(c.isdigit() for c in text):
                if "$" in text or "million" in text or "billion" in text:
                    score += 15
                else:
                    score += 5

            article["relevance_score"] = min(score, 100)

        return articles

    def fetch_google_news(self) -> List[Dict]:
        """Fetch from Google News API via Serper"""
        INDUSTRY_QUERIES = [
            "AI artificial intelligence",
            "quantum computing",
            "robotics automation",
            "tech investment funding",
            "AI startups",
            "cybersecurity technology",
            "cloud computing",
            "semiconductor chip",
            "autonomous vehicles",
            "healthcare AI",
            "fintech digital payments",
            "blockchain crypto",
            "space technology",
            "clean energy tech",
            "machine learning research",
            "AI regulation policy",
            "robotics humanoid",
            "quantum breakthrough",
        ]

        headers = {"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"}
        all_results = []

        for query in INDUSTRY_QUERIES:
            try:
                resp = requests.post(
                    "https://google.serper.dev/news",
                    headers=headers,
                    json={"q": query, "num": 20},
                    timeout=15
                )
                data = resp.json()
                for item in data.get("news", []):
                    all_results.append({
                        "title": item.get("title", ""),
                        "url": item.get("link", ""),
                        "source": f"GoogleNews:{item.get('source', '')}",
                        "source_type": "api",
                        "published": datetime.now(SGT).isoformat(),
                        "summary": item.get("snippet", ""),
                        "industry_tags": self._tag_industry(query + " " + item.get("title", "")),
                        "region_tags": [],
                        "category": self._categorize(query),
                        "sentiment": "neutral",
                        "source_credibility": 10,
                    })
            except Exception as e:
                logger.warning(f"Google News query failed: {query}: {e}")

        return all_results

    def fetch_bing_news(self) -> List[Dict]:
        """Fetch from Bing News API"""
        if not BING_API_KEY:
            return []

        headers = {"Ocp-Apim-Subscription-Key": BING_API_KEY}
        all_results = []

        TOPICS = [
            "AI+artificial+intelligence", "quantum+computing",
            "robotics", "tech+investment+funding",
            "cybersecurity", "semiconductor",
            "autonomous+vehicles", "AI+startup"
        ]

        for topic in TOPICS:
            try:
                resp = requests.get(
                    f"https://api.bing.microsoft.com/v7.0/news/search?q={topic}&count=30&freshness=Day",
                    headers=headers,
                    timeout=15
                )
                data = resp.json()
                for item in data.get("value", []):
                    all_results.append({
                        "title": item.get("name", ""),
                        "url": item.get("url", ""),
                        "source": f"BingNews:{item.get('provider', [{}])[0].get('name', '')}",
                        "source_type": "api",
                        "published": item.get("datePublished", datetime.now(SGT).isoformat()),
                        "summary": item.get("description", ""),
                        "industry_tags": [],
                        "region_tags": [],
                        "category": "Cross-cutting",
                        "sentiment": "neutral",
                        "source_credibility": 15,
                    })
            except Exception as e:
                logger.warning(f"Bing News query failed: {topic}: {e}")

        return all_results

    def fetch_rss_feeds(self) -> List[Dict]:
        """Fetch from RSS feeds"""
        RSS_FEEDS = [
            "https://techcrunch.com/feed/",
            "https://venturebeat.com/feed/",
            "https://www.wired.com/feed/rss",
            "https://www.theverge.com/rss/index.xml",
            "https://arstechnica.com/feed/",
            "https://krebsonsecurity.com/feed/",
            "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml",
            "https://feeds.bloomberg.com/markets/news.rss",
            "https://www.ft.com/?format=rss",
            "https://www.newscientist.com/feed/home",
            "https://www.quantamagazine.org/feed/",
            "https://www.nasa.gov/feed/",
            "https://www.space.com/feeds/all",
            "https://www.sciencedaily.com/rss/computers_math/artificial_intelligence.xml",
            "https://www.sciencedaily.com/rss/computers_math/quantum_computers.xml",
            "https://www.reddit.com/r/artificial/.rss",
            "https://www.reddit.com/r/MachineLearning/.rss",
            "https://www.reddit.com/r/quantum/.rss",
            "https://www.reddit.com/r/robotics/.rss",
            "https://www.reddit.com/r/Futurology/.rss",
        ]

        all_results = []
        for feed_url in RSS_FEEDS:
            try:
                parsed = feedparser.parse(feed_url)
                for entry in parsed.entries[:10]:
                    summary = entry.get("summary", entry.get("description", ""))
                    if summary:
                        soup = BeautifulSoup(summary, "html.parser")
                        summary = soup.get_text(strip=True)[:500]

                    all_results.append({
                        "title": entry.get("title", ""),
                        "url": entry.get("link", ""),
                        "source": f"RSS:{feed_url.split('/')[2]}",
                        "source_type": "rss",
                        "published": entry.get("published", datetime.now(SGT).isoformat()),
                        "summary": summary,
                        "industry_tags": [],
                        "region_tags": [],
                        "category": "Cross-cutting",
                        "sentiment": "neutral",
                        "source_credibility": 15,
                    })
            except Exception as e:
                logger.warning(f"RSS failed: {feed_url}: {e}")

        return all_results

    def fetch_crunchbase(self) -> List[Dict]:
        """Fetch funding data from Crunchbase"""
        if not CRUNCHBASE_API_KEY:
            return []

        headers = {"X-API-KEY": CRUNCHBASE_API_KEY, "Content-Type": "application/json"}
        all_results = []

        CATEGORIES = ["artificial_intelligence", "quantum_computing", "robotics",
                      "machine_learning", "autonomous_vehicles", "cybersecurity",
                      "semiconductor", "cloud_computing", "biotechnology",
                      "clean_technology", "space_technology", "fintech"]

        for category in CATEGORIES:
            try:
                resp = requests.post(
                    "https://api.crunchbase.com/api/v4/searches/funding_rounds",
                    headers=headers,
                    json={
                        "field_ids": ["funding_round_id", "funding_round_name",
                                      "funding_round_amount", "funding_round_type",
                                      "funding_round_post_money_valuation",
                                      "organization_name", "funding_round_announced_on",
                                      "investor_names"],
                        "query": [
                            {"type": "predicate", "field_id": "categories",
                             "operator_id": "includes", "values": [category]},
                            {"type": "predicate", "field_id": "funding_round_announced_on",
                             "operator_id": "gte", "values": [(datetime.now(SGT) - timedelta(days=1)).strftime("%Y-%m-%d")]}
                        ],
                        "limit": 20
                    },
                    timeout=15
                )
                data = resp.json()
                for item in data.get("entities", []):
                    props = item.get("properties", {})
                    name = props.get("organization_name", {}).get("value", "")
                    amount = props.get("funding_round_amount", {}).get("value_usd", 0)
                    round_type = props.get("funding_round_type", {}).get("value", "")
                    valuation = props.get("funding_round_post_money_valuation", {}).get("value_usd", 0)
                    investors = props.get("investor_names", {}).get("value", [])

                    if amount and amount > 0:
                        all_results.append({
                            "title": f"{name} raises ${amount/1000000:.0f}M in {round_type} funding",
                            "url": f"https://www.crunchbase.com/organization/{item.get('uuid', '')}",
                            "source": "Crunchbase",
                            "source_type": "api",
                            "published": props.get("funding_round_announced_on", {}).get("value", ""),
                            "summary": f"{name} raised ${amount/1000000:.0f}M in {round_type} funding. "
                                       f"Valuation: ${valuation/1000000000:.1f}B. Investors: {', '.join(investors) if investors else 'Not disclosed'}",
                            "industry_tags": [category],
                            "region_tags": [],
                            "category": "Investment",
                            "sentiment": "positive",
                            "funding_amount_usd": amount,
                            "funding_round": round_type,
                            "has_funding_data": True,
                            "source_credibility": 20,
                        })
            except Exception as e:
                logger.warning(f"Crunchbase query failed: {category}: {e}")

        return all_results

    def fetch_arxiv(self) -> List[Dict]:
        """Fetch latest papers from arXiv"""
        CATEGORIES = [
            ("cs.AI", "AI"),
            ("quant-ph", "Quantum"),
            ("cs.RO", "Robotics"),
            ("cs.LG", "AI"),
            ("cs.CL", "AI"),
            ("cs.CV", "AI"),
            ("cs.CR", "Cybersecurity"),
        ]

        all_results = []
        for category, tech_label in CATEGORIES:
            try:
                resp = requests.get(
                    f"http://export.arxiv.org/api/query?search_query=cat:{category}"
                    f"&sortBy=submittedDate&sortOrder=descending&max_results=20",
                    timeout=15
                )
                import xml.etree.ElementTree as ET
                root = ET.fromstring(resp.content)
                ns = {"a": "http://www.w3.org/2005/Atom"}

                for entry in root.findall("a:entry", ns):
                    title = entry.find("a:title", ns)
                    summary = entry.find("a:summary", ns)
                    published = entry.find("a:published", ns)
                    link = entry.find("a:id", ns)

                    all_results.append({
                        "title": (title.text or "").replace("\n", " ").strip() if title is not None else "",
                        "url": link.text.strip() if link is not None else "",
                        "source": f"arXiv:{category}",
                        "source_type": "rss",
                        "published": published.text if published is not None else "",
                        "summary": (summary.text or "").replace("\n", " ").strip()[:500] if summary is not None else "",
                        "industry_tags": [category],
                        "region_tags": [],
                        "category": tech_label,
                        "sentiment": "neutral",
                        "has_funding_data": False,
                        "source_credibility": 25,
                    })
            except Exception as e:
                logger.warning(f"arXiv query failed: {category}: {e}")

        return all_results

    def fetch_sec_filings(self) -> List[Dict]:
        """Fetch SEC 8-K filings mentioning key terms"""
        try:
            resp = requests.get(
                "https://efts.sec.gov/LATEST/search-index?q=artificial+intelligence+OR+quantum+OR+robotics"
                "&dateRange=today&start=0&count=50",
                timeout=15
            )
            data = resp.json()
            results = []
            for hit in data.get("hits", {}).get("hits", []):
                source = hit.get("_source", {})
                results.append({
                    "title": f"SEC Filing: {source.get('display_name', '')} - {source.get('file_description', 'AI Disclosure')}",
                    "url": f"https://www.sec.gov{source.get('file_num', '')}",
                    "source": "SEC EDGAR",
                    "source_type": "api",
                    "published": source.get("filed_at", ""),
                    "summary": f"SEC 8-K filing mentioning AI/quantum/robotics by {source.get('display_name', 'Unknown')}",
                    "industry_tags": [],
                    "region_tags": ["North America"],
                    "category": "Investment",
                    "sentiment": "neutral",
                    "has_regulatory_impact": True,
                    "source_credibility": 20,
                })
            return results
        except Exception as e:
            logger.warning(f"SEC filings failed: {e}")
            return []

    def _tag_industry(self, text: str) -> List[str]:
        """Simple industry tagging from text"""
        text_lower = text.lower()
        tags = []

        industry_map = {
            "ai|artificial intelligence|machine learning|llm|gpt|neural": "AI",
            "quantum|qubit|superposition|entanglement": "Quantum Computing",
            "robot|humanoid|drone|autonomous": "Robotics",
            "cyber|security|ransomware|breach|zero-day": "Cybersecurity",
            "cloud|kubernetes|aws|azure|gcp|serverless": "Cloud Computing",
            "chip|semiconductor|gpu|foundry|tsmc": "Semiconductor",
            "fintech|payment|banking|blockchain|crypto|defi": "Fintech/Blockchain",
            "health|medical|drug|clinical|hospital|biotech": "Healthcare/Biotech",
            "auto|vehicle|ev|electric car|self-driving": "Automotive/AV",
            "space|nasa|spacex|satellite|launch|rocket": "Space/Satellite",
            "energy|solar|wind|nuclear|hydrogen|battery|renewable": "Energy/Cleantech",
            "education|learning|edtech|online course": "Education",
            "defense|military|national security|government": "Defense/GovTech",
            "real estate|property|smart building|construction": "Real Estate/Construction",
            "food|agriculture|farming|agritech": "Agriculture/Food",
            "media|entertainment|gaming|streaming": "Media/Entertainment",
            "market|advertising|marketing|martech": "Marketing/AdTech",
            "hr|talent|recruitment|workforce": "HR/Legal",
        }

        for pattern, tag in industry_map.items():
            if any(kw in text_lower for kw in pattern.split("|")):
                tags.append(tag)

        return tags if tags else ["General Technology"]

    def _categorize(self, query: str) -> str:
        query_lower = query.lower()
        if "quantum" in query_lower:
            return "Quantum"
        elif "robot" in query_lower or "autonom" in query_lower:
            return "Robotics"
        elif "investment" in query_lower or "funding" in query_lower:
            return "Investment"
        else:
            return "AI"


# ============================================================
# AGENT 2: RAG CURATION
# ============================================================

class CuratorRAGAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.0,
            api_key=OPENAI_API_KEY
        )
        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-3-large",
            api_key=OPENAI_API_KEY
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )

        # Initialize Pinecone
        pinecone.init(api_key=PINECONE_API_KEY, environment="us-west1-gcp")
        self.index = pinecone.Index(PINECONE_INDEX)
        self.vectorstore = Pinecone(
            index=self.index,
            embedding=self.embeddings,
            text_key="text"
        )

    def __call__(self, state: EnterpriseState) -> EnterpriseState:
        curated = []
        for article in state["raw_articles"]:
            score = self.compute_final_score(article)
            article["final_score"] = score

            if score >= 40:
                # Generate embedding and store in Pinecone
                self.store_in_vector_db(article)
                curated.append(article)

        curated.sort(key=lambda x: x["final_score"], reverse=True)

        # Flag alert-worthy articles
        for article in curated:
            article["alert_worthy"] = article["final_score"] >= 75
            article["industry_impact_level"] = self.compute_impact_level(article)

        state["curated_articles"] = curated[:200]
        return state

    def compute_final_score(self, article: Dict) -> float:
        score = article.get("relevance_score", 0)
        source_cred = article.get("source_credibility", 0)

        # Funding bonus
        if article.get("has_funding_data") or article.get("funding_amount_usd", 0) > 0:
            score += 15

        # Regulatory impact bonus
        if article.get("has_regulatory_impact"):
            score += 10

        # Cross-industry impact (inferred from industry_tags)
        tags = article.get("industry_tags", [])
        if len(tags) >= 3:
            score += 10
        elif len(tags) >= 2:
            score += 5

        # Source credibility weighted
        score += source_cred * 0.2

        return min(score, 100)

    def compute_impact_level(self, article: Dict) -> str:
        score = article.get("final_score", 0)
        if score >= 85: return "Transformative"
        elif score >= 70: return "High"
        elif score >= 55: return "Medium"
        elif score >= 40: return "Low"
        return "None"

    def store_in_vector_db(self, article: Dict):
        """Chunk, embed, and store article in Pinecone"""
        try:
            text = f"{article['title']}\n\n{article['summary']}"
            if article.get("full_text"):
                text += f"\n\n{article['full_text']}"

            chunks = self.text_splitter.split_text(text)
            embeddings = self.embeddings.embed_documents(chunks)

            vectors = []
            for i, (chunk, emb) in enumerate(zip(chunks, embeddings)):
                vectors.append({
                    "id": f"{article['url']}_{i}",
                    "values": emb,
                    "metadata": {
                        "title": article["title"],
                        "url": article["url"],
                        "source": article["source"],
                        "chunk_index": i,
                        "industry_tags": json.dumps(article.get("industry_tags", [])),
                        "category": article.get("category", ""),
                        "published": article.get("published", ""),
                    }
                })

            self.index.upsert(vectors=vectors)
        except Exception as e:
            logger.error(f"Vector store failed for {article.get('title', '')}: {e}")


# ============================================================
# AGENT 3: INSIGHT EXTRACTION
# ============================================================

class InsightExtractionAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4o",
            temperature=0.2,
            api_key=OPENAI_API_KEY
        )

    def __call__(self, state: EnterpriseState) -> EnterpriseState:
        articles_json = json.dumps(state["curated_articles"][:100], indent=2)

        prompt = f"""Extract structured intelligence from today's curated articles.

Today's date: {datetime.now(SGT).strftime('%Y-%m-%d')}
Total articles: {len(state['curated_articles'])}
Industries covered: {', '.join(sorted(set(
    t for a in state['curated_articles'] for t in a.get('industry_tags', [])
)))}

Articles:
{articles_json[:8000]}

Generate the following EXECUTIVE INTELLIGENCE BRIEF as JSON:
1. breaking_today: top 3 stories with severity (8-10), impact, action needed
2. investment_heatmap: total funding, top 5 rounds, emerging patterns
3. industry_impact_matrix: disruption level per sector
4. regional_pulse: key developments per region
5. technology_maturity: Gartner Hype Cycle phase per tech
6. regulatory_watch: policy changes and enforcement
7. innovation_leaderboard: leading companies, universities, countries
8. executive_summary: 2-minute brief (5 bullets)

Return ONLY valid JSON, no other text."""

        try:
            resp = self.llm.invoke(prompt)
            insights = json.loads(resp.content.strip())
            state["insights"] = insights
        except Exception as e:
            logger.error(f"Insight extraction failed: {e}")
            state["insights"] = {"error": str(e), "breaking_today": []}

        return state


# ============================================================
# AGENT 4: ALERT GENERATION
# ============================================================

class AlertAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.1,
            api_key=OPENAI_API_KEY
        )

    def __call__(self, state: EnterpriseState) -> EnterpriseState:
        alert_worthy = [a for a in state["curated_articles"]
                       if a.get("alert_worthy") or a.get("final_score", 0) >= 75]

        if not alert_worthy:
            state["alerts"] = []
            return state

        articles_json = json.dumps(alert_worthy, indent=2)

        prompt = f"""Analyze these alert-worthy articles and generate push notifications.

ARTICLES:
{articles_json}

For each article, determine if it matches these alert types:
- BREAKING_INVESTMENT: Funding >$100M, IPO, M&A
- REGULATORY_ALERT: Government policy, export controls, compliance
- MODEL_RELEASE: New AI model, breakthrough
- QUANTUM_BREAKTHROUGH: Quantum computing milestone
- ROBOTICS_SCALE: Large-scale robot deployment
- SECURITY_ALERT: Critical vulnerability, breach
- STRATEGIC_MOVE: Major partnership, acquisition, executive move

OUTPUT JSON array:
[
  {{
    "type": "ALERT_TYPE",
    "severity": 1-10,
    "headline": "string",
    "body": "2-sentence summary",
    "industry_tags": [],
    "region": "string",
    "action_url": "url",
    "suggested_push_text": "max 120 chars",
    "notification_channels": ["push", "email", "sms"],
    "ttl_hours": 24
  }}
]"""

        try:
            resp = self.llm.invoke(prompt)
            alerts = json.loads(resp.content.strip())
            state["alerts"] = alerts
        except Exception as e:
            logger.error(f"Alert generation failed: {e}")
            state["alerts"] = []

        return state


# ============================================================
# AGENT 5: REPORT GENERATION
# ============================================================

class ReportGenerationAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4o",
            temperature=0.3,
            api_key=OPENAI_API_KEY
        )

    def __call__(self, state: EnterpriseState) -> EnterpriseState:
        insights = state.get("insights", {})
        alerts = state.get("alerts", [])
        article_count = len(state.get("curated_articles", []))

        # Build from insights
        report = {
            "generated_at": datetime.now(SGT).isoformat(),
            "total_articles_processed": article_count,
            "total_alerts": len(alerts),
            "industries_covered": sorted(set(
                t for a in state["curated_articles"] for t in a.get("industry_tags", [])
            )),
            "regions_covered": sorted(set(
                r for a in state["curated_articles"] for r in a.get("region_tags", [])
            )),
            "sources_used": list(set(a.get("source", "").split(":")[0]
                                    for a in state["curated_articles"])),
            "insights": insights,
            "alerts": alerts,
            "markdown_brief": self.generate_markdown(insights, alerts, article_count),
            "mobile_brief": self.generate_mobile_brief(insights, alerts),
            "audio_script": self.generate_audio_script(insights),
        }

        state["report"] = report
        return state

    def generate_markdown(self, insights: dict, alerts: list, count: int) -> str:
        date_str = datetime.now(SGT).strftime("%d %B %Y")
        lines = [
            f"# 🧠 Global AI Intelligence Brief — {date_str}",
            "",
            f"> **Articles Processed:** {count} | **Alerts:** {len(alerts)}",
            f"> **Generated:** {datetime.now(SGT).strftime('%Y-%m-%d %H:%M SGT')}",
            "",
        ]

        # Breaking Today
        lines.append("## 🔥 Breaking Today")
        for item in insights.get("breaking_today", []):
            lines.append(f"- ⚡ [{item.get('severity', 'N/A')}/10] {item.get('headline', '')}")
            lines.append(f"  - {item.get('impact', '')}")
        lines.append("")

        # Investment Heatmap
        lines.append("## 📊 Investment Heatmap")
        hm = insights.get("investment_heatmap", {})
        lines.append(f"**Total Disclosed Funding:** {hm.get('total_funding', 'N/A')}")
        lines.append("**Top Rounds:**")
        for r in hm.get("top_rounds", []):
            lines.append(f"- {r}")
        lines.append("")

        # Industry Impact
        lines.append("## 🏭 Industry Impact Matrix")
        for sector in insights.get("industry_impact_matrix", []):
            dl = sector.get("disruption_level", "None")
            emoji = {"Transformative": "🚀", "High": "📈", "Medium": "📊", "Low": "📉", "None": "⚪"}
            lines.append(f"{emoji.get(dl, '⚪')} **{sector.get('sector', '')}** — {dl}")
            lines.append(f"  - {sector.get('key_development', '')}")
        lines.append("")

        # Regional Pulse
        lines.append("## 🌍 Regional Pulse")
        for region, dev in insights.get("regional_pulse", {}).items():
            lines.append(f"- **{region}:** {dev}")
        lines.append("")

        # Alerts
        if alerts:
            lines.append("## 🚨 Active Alerts")
            for alert in alerts:
                lines.append(f"- [{alert.get('type', '')}] Severity {alert.get('severity', '')}: {alert.get('headline', '')}")
            lines.append("")

        lines.append("---")
        lines.append(f"*End of Brief — TechPulse Global Intelligence*")

        return "\n".join(lines)

    def generate_mobile_brief(self, insights: dict, alerts: list) -> str:
        """5-bullet mobile-optimized brief"""
        bullets = []
        for item in insights.get("breaking_today", [])[:5]:
            sev = item.get("severity", 0)
            icon = "🔴" if sev >= 8 else "🟡" if sev >= 6 else "🔵"
            bullets.append(f"{icon} {item.get('headline', '')[:80]}")

        while len(bullets) < 5:
            bullets.append("📡 Check dashboard for full briefing")

        return "\n".join(bullets[:5])

    def generate_audio_script(self, insights: dict) -> str:
        lines = ["Welcome to today's Global AI Intelligence Brief.", ""]
        for item in insights.get("breaking_today", [])[:3]:
            lines.append(f"Top story: {item.get('headline', '')}.")
            lines.append(f"{item.get('impact', '')}")
            lines.append("")
        lines.append("Check the TechPulse dashboard for the full report.")
        return "\n".join(lines)


# ============================================================
# CONDITIONAL EDGES
# ============================================================

def should_trigger_alerts(state: EnterpriseState) -> str:
    """Decide if alerts should be generated"""
    # Check if any articles are alert-worthy
    alert_worthy = [a for a in state.get("curated_articles", [])
                   if a.get("alert_worthy") or a.get("final_score", 0) >= 75]
    return "alert" if alert_worthy else "skip"

def should_continue(state: EnterpriseState) -> str:
    """Check if pipeline should continue"""
    if state.get("errors") and len(state["errors"]) > 5:
        return "end"
    if not state.get("raw_articles"):
        return "end"
    return "continue"


# ============================================================
# BUILD LANGGRAPH
# ============================================================

def build_pipeline() -> StateGraph:
    workflow = StateGraph(EnterpriseState)

    # Add nodes
    workflow.add_node("news_aggregation", NewsAggregationAgent())
    workflow.add_node("curation_rag", CuratorRAGAgent())
    workflow.add_node("insight_extraction", InsightExtractionAgent())
    workflow.add_node("alert_generation", AlertAgent())
    workflow.add_node("report_generation", ReportGenerationAgent())

    # Add edges
    workflow.set_entry_point("news_aggregation")
    workflow.add_edge("news_aggregation", "curation_rag")
    workflow.add_edge("curation_rag", "insight_extraction")
    workflow.add_conditional_edges(
        "insight_extraction",
        should_trigger_alerts,
        {
            "alert": "alert_generation",
            "skip": "report_generation",
        }
    )
    workflow.add_edge("alert_generation", "report_generation")
    workflow.add_edge("report_generation", END)

    # Compile with checkpointing
    memory = SqliteSaver.from_conn_string("checkpoints.db")
    return workflow.compile(checkpointer=memory)


# ============================================================
# PIPELINE EXECUTOR
# ============================================================

class EnterprisePipeline:
    def __init__(self):
        self.graph = build_pipeline()

    async def run_daily(self) -> Dict[str, Any]:
        """Execute the full daily intelligence pipeline"""
        run_id = datetime.now(SGT).strftime("run_%Y%m%d_%H%M%S")

        initial_state: EnterpriseState = {
            "run_id": run_id,
            "started_at": datetime.now(SGT).isoformat(),
            "completed_at": None,
            "raw_articles": [],
            "curated_articles": [],
            "insights": {},
            "alerts": [],
            "report": {},
            "industries": list(INDUSTRY_MASTER_CATEGORIES.keys()),
            "regions": ["North America", "Europe", "APAC", "Middle East", "Africa", "LATAM"],
            "sources_used": [],
            "errors": [],
        }

        config = {"configurable": {"thread_id": run_id}}
        final_state = await self.graph.ainvoke(initial_state, config)
        final_state["completed_at"] = datetime.now(SGT).isoformat()

        # Store to database
        self.persist_results(final_state)

        return final_state

    def persist_results(self, state: EnterpriseState):
        """Save articles and alerts to PostgreSQL"""
        try:
            engine = create_engine(DATABASE_URL)
            Session = sessionmaker(bind=engine)
            session = Session()

            for article in state.get("curated_articles", []):
                existing = session.query(Article).filter_by(url=article.get("url")).first()
                if not existing:
                    db_article = Article(
                        id=article.get("url", ""),
                        title=article.get("title", ""),
                        url=article.get("url", ""),
                        source=article.get("source", ""),
                        source_type=article.get("source_type", ""),
                        published=article.get("published"),
                        summary=article.get("summary", ""),
                        industry_tags=article.get("industry_tags", []),
                        region_tags=article.get("region_tags", []),
                        category=article.get("category", ""),
                        sentiment=article.get("sentiment", ""),
                        relevance_score=article.get("relevance_score", 0),
                        final_score=article.get("final_score", 0),
                        funding_amount_usd=article.get("funding_amount_usd"),
                        funding_round=article.get("funding_round"),
                        has_regulatory_impact=article.get("has_regulatory_impact", False),
                        key_entities=article.get("key_entities", []),
                        source_credibility=article.get("source_credibility", 0),
                    )
                    session.add(db_article)

            for alert in state.get("alerts", []):
                db_alert = Alert(
                    id=f"alert_{alert.get('type')}_{datetime.now(SGT).timestamp()}",
                    type=alert.get("type", ""),
                    severity=alert.get("severity", 0),
                    headline=alert.get("headline", ""),
                    body=alert.get("body", ""),
                    industry_tags=alert.get("industry_tags", []),
                    region=alert.get("region", ""),
                    action_url=alert.get("action_url", ""),
                    suggested_push_text=alert.get("suggested_push_text", ""),
                    ttl_hours=alert.get("ttl_hours", 24),
                )
                session.add(db_alert)

            session.commit()
            session.close()
        except Exception as e:
            logger.error(f"Database persist failed: {e}")


# ============================================================
# FASTAPI SERVER
# ============================================================

from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Enterprise Tech Intelligence API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pipeline = EnterprisePipeline()

@app.get("/health")
async def health():
    return {"status": "ok", "version": "2.0.0", "timestamp": datetime.now(SGT).isoformat()}

@app.post("/api/pipeline/run")
async def run_pipeline(background_tasks: BackgroundTasks):
    """Trigger full intelligence pipeline"""
    background_tasks.add_task(pipeline.run_daily)
    return {"status": "started", "message": "Daily intelligence pipeline initiated"}

@app.get("/api/pipeline/latest")
async def get_latest_report():
    """Get latest generated report"""
    try:
        engine = create_engine(DATABASE_URL)
        Session = sessionmaker(bind=engine)
        session = Session()
        articles = session.query(Article).order_by(Article.created_at.desc()).limit(50).all()
        alerts = session.query(Alert).filter(Alert.sent == False).order_by(Alert.created_at.desc()).limit(10).all()
        session.close()

        return {
            "articles": [
                {
                    "title": a.title,
                    "url": a.url,
                    "source": a.source,
                    "industry_tags": a.industry_tags,
                    "final_score": a.final_score,
                    "funding_amount_usd": a.funding_amount_usd,
                }
                for a in articles
            ],
            "alerts": [
                {
                    "type": al.type,
                    "severity": al.severity,
                    "headline": al.headline,
                    "suggested_push_text": al.suggested_push_text,
                }
                for al in alerts
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/insights/{industry}")
async def get_industry_insights(industry: str):
    """Get RAG-powered insights for a specific industry"""
    try:
        # Query Pinecone for industry-specific articles
        vectorstore = Pinecone(
            index=pinecone.Index(PINECONE_INDEX),
            embedding=OpenAIEmbeddings(model="text-embedding-3-large"),
            text_key="text"
        )
        results = vectorstore.similarity_search(
            f"Latest developments in {industry} technology",
            k=10,
            filter={"industry_tags": {"$contains": industry}}
        )

        return {
            "industry": industry,
            "articles": [
                {
                    "title": r.metadata.get("title", ""),
                    "url": r.metadata.get("url", ""),
                    "source": r.metadata.get("source", ""),
                    "score": r.metadata.get("score", 0),
                    "content": r.page_content[:300],
                }
                for r in results
            ],
            "total": len(results),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

---

## 6. RAG + Vector DB Implementation

### Current vs. Enhanced RAG

```
CURRENT (TechPulse Daily):
  No RAG → Passes full report text to GPT-4o-mini (truncated at 120K chars)

ENHANCED (Enterprise):
  ┌─────────────────────────────────────────────────────┐
  │                    RAG PIPELINE                       │
  │                                                       │
  │  1. INGEST: Chunk each article (1000 chars, 200 overlap) │
  │  2. EMBED: text-embedding-3-large (3072 dimensions)  │
  │  3. STORE: Pinecone vector DB (cosine similarity)    │
  │  4. RETRIEVE: Top-K (k=5-20) relevant chunks per query │
  │  5. RERANK: Cross-encoder for precision              │
  │  6. GENERATE: GPT-4o with retrieved context          │
  └─────────────────────────────────────────────────────┘
```

### Pinecone Setup

```python
# enterprise_engine/vector_store.py
import pinecone
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Pinecone as PineconeStore
from langchain.text_splitter import RecursiveCharacterTextSplitter

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY", "")
PINECONE_ENVIRONMENT = "us-west1-gcp"
PINECONE_INDEX = "tech-intel"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Initialize
pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENVIRONMENT)

# Create index if not exists
if PINECONE_INDEX not in pinecone.list_indexes():
    pinecone.create_index(
        name=PINECONE_INDEX,
        dimension=3072,  # text-embedding-3-large
        metric="cosine",
        pod_type="p1.x1"
    )

embeddings = OpenAIEmbeddings(model="text-embedding-3-large", api_key=OPENAI_API_KEY)
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

def index_article(article: dict):
    """Chunk, embed, and store article"""
    text = f"{article['title']}\n\n{article.get('summary', '')}"
    if article.get("full_text"):
        text += f"\n\n{article['full_text']}"

    chunks = text_splitter.split_text(text)
    chunk_embeddings = embeddings.embed_documents(chunks)

    vectors = []
    for i, (chunk, emb) in enumerate(zip(chunks, chunk_embeddings)):
        vectors.append({
            "id": f"{article['url']}_{i}",
            "values": emb,
            "metadata": {
                "title": article["title"],
                "url": article["url"],
                "source": article["source"],
                "chunk_index": i,
                "industry_tags": article.get("industry_tags", []),
                "category": article.get("category", ""),
                "published": article.get("published", ""),
                "funding_amount": article.get("funding_amount_usd", 0),
                "has_regulatory": article.get("has_regulatory_impact", False),
            }
        })

    index = pinecone.Index(PINECONE_INDEX)
    index.upsert(vectors=vectors)

def query_industry(industry: str, question: str, k: int = 10) -> list:
    """Query Pinecone for industry-specific intelligence"""
    vectorstore = PineconeStore(
        index=pinecone.Index(PINECONE_INDEX),
        embedding=embeddings,
        text_key="text"
    )

    # Hybrid: combine industry filter with semantic search
    results = vectorstore.similarity_search(
        question,
        k=k,
        filter={"industry_tags": {"$contains": industry}}
    )

    return [
        {
            "title": r.metadata.get("title", ""),
            "url": r.metadata.get("url", ""),
            "content": r.page_content[:500],
            "score": r.metadata.get("score", 0),
            "published": r.metadata.get("published", ""),
        }
        for r in results
    ]

def query_funding(min_amount: float = 100_000_000) -> list:
    """Query for funding events above threshold"""
    vectorstore = PineconeStore(
        index=pinecone.Index(PINECONE_INDEX),
        embedding=embeddings,
        text_key="text"
    )

    results = vectorstore.similarity_search(
        "technology company funding investment round",
        k=50,
        filter={"funding_amount": {"$gte": min_amount}}
    )

    return results
```

---

## 7. Data Sources & API Integration

### Complete Source Matrix

| Source | Type | API Key Required | Rate Limit | Data Points |
|--------|------|-----------------|------------|-------------|
| **Google News (via Serper)** | REST API | `SERPER_API_KEY` | 2500/month free | Title, snippet, source, link |
| **Bing News** | REST API | `BING_API_KEY` | 1000/month free | Title, description, provider, date |
| **Gartner RSS** | RSS | No | Unlimited | Research summaries |
| **Crunchbase** | REST API | `CRUNCHBASE_API_KEY` | 500/day free | Funding, investors, valuation |
| **arXiv** | RSS/API | No | Unlimited | Research papers, abstracts |
| **SEC EDGAR** | REST API | No | 10/sec | 8-K filings, AI disclosures |
| **TechCrunch** | RSS | No | Unlimited | Startup news |
| **VentureBeat** | RSS | No | Unlimited | AI/tech news |
| **Wired** | RSS | No | Unlimited | Tech culture |
| **Reddit** | RSS | No | Unlimited | Community discussions |
| **GitHub Trending** | REST API | No | 60/hour | Trending repos |
| **Hugging Face** | REST API | No | Unlimited | Model releases, papers |
| **Reuters** | RSS | No | Unlimited | Business news |
| **Bloomberg** | RSS | No | Unlimited | Financial news |
| **IEEE Spectrum** | RSS | No | Unlimited | Engineering research |
| **MIT Tech Review** | RSS | No | Unlimited | Emerging tech |
| **Nature** | RSS | No | Unlimited | Scientific research |
| **LinkedIn News** | RSS | No | Unlimited | Professional news |

### API Configuration (.env)

```ini
# === NEWS APIs ===
SERPER_API_KEY=your_serper_key_here
BING_API_KEY=your_bing_key_here
CRUNCHBASE_API_KEY=your_crunchbase_key_here

# === AI / LLM ===
OPENAI_API_KEY=sk-proj-your-key-here
ANTHROPIC_API_KEY=sk-ant-your-key-here

# === VECTOR DATABASE ===
PINECONE_API_KEY=your_pinecone_key
PINECONE_INDEX=tech-intel

# === DATABASE ===
DATABASE_URL=postgresql://user:pass@localhost:5432/techintel
REDIS_URL=redis://localhost:6379/0
ELASTICSEARCH_URL=http://localhost:9200

# === NOTIFICATIONS ===
FIREBASE_SERVER_KEY=your_fcm_key
ONESIGNAL_APP_ID=your_onesignal_id
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/...
TEAMS_WEBHOOK_URL=https://outlook.office.com/webhook/...

# === SCHEDULE ===
PIPELINE_INTERVAL_HOURS=4  # Run every 4 hours
ALERT_REALTIME=true

# === AUTH ===
AUTH0_DOMAIN=your-domain.auth0.com
AUTH0_AUDIENCE=https://api.techpulse.com
```

---

## 8. Web + Mobile Implementation Plan

### 8.1 Next.js Web Dashboard

```
enterprise-dashboard/
├── src/
│   ├── app/
│   │   ├── layout.tsx              # Root layout with auth
│   │   ├── page.tsx                # Main dashboard
│   │   ├── insights/
│   │   │   ├── page.tsx            # Industry insights
│   │   │   └── [industry]/
│   │   │       └── page.tsx        # Per-industry deep dive
│   │   ├── investments/
│   │   │   └── page.tsx            # Funding tracker
│   │   ├── alerts/
│   │   │   └── page.tsx            # Real-time alerts
│   │   ├── reports/
│   │   │   └── page.tsx            # Report archive
│   │   └── settings/
│   │       └── page.tsx            # User preferences
│   │
│   ├── components/
│   │   ├── dashboard/
│   │   │   ├── StatusBar.tsx       # Pipeline status
│   │   │   ├── IndustryPills.tsx   # Industry filter
│   │   │   ├── ArticleCard.tsx     # Article display
│   │   │   ├── AlertBanner.tsx     # Push alerts
│   │   │   └── FundingTable.tsx    # Funding rounds
│   │   ├── charts/
│   │   │   ├── InvestmentTreemap.tsx
│   │   │   ├── QuantumHeatmap.tsx
│   │   │   ├── RoboticsBar.tsx
│   │   │   ├── SentimentTimeline.tsx
│   │   │   └── EntityGraph.tsx
│   │   ├── chat/
│   │   │   └── AIChatPanel.tsx     # RAG chat assistant
│   │   └── layout/
│   │       ├── Header.tsx
│   │       ├── Sidebar.tsx
│   │       └── MobileNav.tsx
│   │
│   ├── lib/
│   │   ├── api.ts                  # API client
│   │   ├── auth.ts                 # Auth0 integration
│   │   ├── websocket.ts            # Real-time updates
│   │   └── utils.ts
│   │
│   └── types/
│       └── index.ts                # TypeScript types
│
├── public/                         # Static assets
├── tailwind.config.js
├── next.config.js
└── package.json
```

### 8.2 Flutter Mobile App

```
enterprise_mobile/
├── lib/
│   ├── main.dart                   # App entry point
│   │
│   ├── app/
│   │   ├── app.dart                # MaterialApp config
│   │   └── router.dart             # GoRouter config
│   │
│   ├── models/
│   │   ├── article.dart            # Article model
│   │   ├── alert.dart              # Alert model
│   │   ├── insight.dart            # Insight model
│   │   └── funding_round.dart       # Funding model
│   │
│   ├── services/
│   │   ├── api_service.dart        # HTTP client
│   │   ├── auth_service.dart       # Auth0
│   │   ├── notification_service.dart  # Firebase
│   │   └── websocket_service.dart  # Real-time
│   │
│   ├── providers/
│   │   ├── articles_provider.dart  # Riverpod state
│   │   ├── alerts_provider.dart
│   │   ├── insights_provider.dart
│   │   └── settings_provider.dart
│   │
│   ├── screens/
│   │   ├── home/
│   │   │   └── home_screen.dart    # Main feed
│   │   ├── insights/
│   │   │   ├── insights_screen.dart
│   │   │   └── industry_detail.dart
│   │   ├── investments/
│   │   │   └── investments_screen.dart
│   │   ├── alerts/
│   │   │   └── alerts_screen.dart
│   │   ├── search/
│   │   │   └── search_screen.dart  # RAG search
│   │   └── settings/
│   │       └── settings_screen.dart
│   │
│   └── widgets/
│       ├── article_card.dart
│       ├── alert_banner.dart
│       ├── industry_chip.dart
│       ├── funding_tile.dart
│       ├── chart_widget.dart
│       └── chat_bubble.dart
│
├── android/
├── ios/
├── pubspec.yaml
└── firebase_options.dart
```

### 8.3 Push Notification Integration

```dart
// Firebase Cloud Messaging
class NotificationService {
  final FirebaseMessaging _fcm = FirebaseMessaging.instance;

  Future<void> initialize() async {
    NotificationSettings settings = await _fcm.requestPermission();
    String? token = await _fcm.getToken();

    // Send token to backend
    await ApiService.registerDeviceToken(token);

    // Handle foreground messages
    FirebaseMessaging.onMessage.listen((RemoteMessage message) {
      _showLocalNotification(message);
    });

    // Handle background taps
    FirebaseMessaging.onMessageOpenedApp.listen((RemoteMessage message) {
      _navigateToAlert(message.data);
    });
  }

  void _showLocalNotification(RemoteMessage message) {
    flutterLocalNotificationsPlugin.show(
      message.hashCode,
      message.notification?.title,
      message.notification?.body,
      const NotificationDetails(
        android: AndroidNotificationDetails(
          'tech_alerts',
          'Tech Intelligence Alerts',
          importance: Importance.max,
          priority: Priority.high,
        ),
        iOS: DarwinNotificationDetails(
          presentAlert: true,
          presentBadge: true,
          presentSound: true,
        ),
      ),
      payload: jsonEncode(message.data),
    );
  }
}
```

### 8.4 Real-Time WebSocket Integration

```python
# enterprise_engine/websocket.py
import asyncio
import json
from datetime import datetime
from zoneinfo import ZoneInfo
from fastapi import WebSocket, WebSocketDisconnect
from typing import Set

SGT = ZoneInfo("Asia/Singapore")

class ConnectionManager:
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.add(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.discard(websocket)

    async def broadcast(self, message: dict):
        dead = set()
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                dead.add(connection)
        self.active_connections -= dead

manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Handle client messages (subscribe to industries, etc.)
            msg = json.loads(data)
            if msg.get("type") == "subscribe":
                industry = msg.get("industry")
                await websocket.send_json({
                    "type": "subscribed",
                    "industry": industry,
                    "message": f"Subscribed to {industry} updates"
                })
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# Background task to push alerts
async def push_alerts_loop():
    while True:
        # Check for new alerts in DB
        # Broadcast to all connected clients
        alert = {
            "type": "alert",
            "severity": 9,
            "headline": "Example breaking alert",
            "timestamp": datetime.now(SGT).isoformat()
        }
        await manager.broadcast(alert)
        await asyncio.sleep(60)  # Check every minute
```

---

## 9. Gartner Hype Cycle Integration

### Gartner Hype Cycle Data Structure

```python
GARTNER_HYPE_CYCLE_2026 = {
    "ai": {
    "label": "Artificial Intelligence",
    "phase": "Peak of Inflated Expectations",
    "years_to_plateau": "2-5 years",
    "sub_technologies": {
        "generative_ai": {"phase": "Peak of Inflated Expectations", "years": "2-5"},
        "ai_agents": {"phase": "Innovation Trigger", "years": "5-10"},
        "autonomous_ai": {"phase": "Innovation Trigger", "years": "10+"},
        "computer_vision": {"phase": "Slope of Enlightenment", "years": "2-5"},
        "nlp": {"phase": "Plateau of Productivity", "years": "<2"},
        "edge_ai": {"phase": "Slope of Enlightenment", "years": "2-5"},
    }
    },
    "quantum_computing": {
        "label": "Quantum Computing",
        "phase": "Trough of Disillusionment",
        "years_to_plateau": "5-10 years",
        "sub_technologies": {
            "quantum_sensing": {"phase": "Slope of Enlightenment", "years": "2-5"},
            "quantum_cryptography": {"phase": "Slope of Enlightenment", "years": "5-10"},
            "quantum_machine_learning": {"phase": "Innovation Trigger", "years": "10+"},
            "quantum_error_correction": {"phase": "Trough of Disillusionment", "years": "5-10"},
        }
    },
    "robotics": {
        "label": "Robotics",
        "phase": "Slope of Enlightenment",
        "years_to_plateau": "2-5 years",
        "sub_technologies": {
            "humanoid_robots": {"phase": "Innovation Trigger", "years": "10+"},
            "autonomous_mobile_robots": {"phase": "Slope of Enlightenment", "years": "2-5"},
            "collaborative_robots": {"phase": "Plateau of Productivity", "years": "<2"},
            "robotic_process_automation": {"phase": "Plateau of Productivity", "years": "<2"},
            "surgical_robotics": {"phase": "Slope of Enlightenment", "years": "2-5"},
        }
    },
    "cybersecurity": {
        "label": "Cybersecurity",
        "phase": "Plateau of Productivity",
        "years_to_plateau": "<2 years",
        "sub_technologies": {
            "ai_security": {"phase": "Peak of Inflated Expectations", "years": "2-5"},
            "zero_trust": {"phase": "Slope of Enlightenment", "years": "2-5"},
            "post_quantum_crypto": {"phase": "Innovation Trigger", "years": "5-10"},
            "xdr": {"phase": "Plateau of Productivity", "years": "<2"},
        }
    },
    "blockchain_web3": {
        "label": "Blockchain/Web3",
        "phase": "Trough of Disillusionment",
        "years_to_plateau": "5-10 years",
        "sub_technologies": {
            "defi": {"phase": "Trough of Disillusionment", "years": "5-10"},
            "tokenization": {"phase": "Innovation Trigger", "years": "5-10"},
            "digital_identity": {"phase": "Slope of Enlightenment", "years": "2-5"},
        }
    },
    "climate_tech": {
        "label": "Climate Technology",
        "phase": "Slope of Enlightenment",
        "years_to_plateau": "5-10 years",
        "sub_technologies": {
            "carbon_capture": {"phase": "Innovation Trigger", "years": "10+"},
            "green_hydrogen": {"phase": "Innovation Trigger", "years": "5-10"},
            "solar_energy": {"phase": "Plateau of Productivity", "years": "<2"},
            "battery_storage": {"phase": "Slope of Enlightenment", "years": "2-5"},
            "fusion_energy": {"phase": "Innovation Trigger", "years": "10+"},
        }
    },
    "semiconductor": {
        "label": "Semiconductor",
        "phase": "Slope of Enlightenment",
        "years_to_plateau": "2-5 years",
        "sub_technologies": {
            "advanced_packaging": {"phase": "Slope of Enlightenment", "years": "2-5"},
            "chiplet_design": {"phase": "Slope of Enlightenment", "years": "2-5"},
            "silicon_photonics": {"phase": "Innovation Trigger", "years": "5-10"},
            "neuromorphic_chips": {"phase": "Innovation Trigger", "years": "5-10"},
        }
    },
    "biotech_health": {
        "label": "Biotech/Healthcare",
        "phase": "Slope of Enlightenment",
        "years_to_plateau": "2-5 years",
        "sub_technologies": {
            "genomic_ai": {"phase": "Slope of Enlightenment", "years": "2-5"},
            "drug_discovery_ai": {"phase": "Peak of Inflated Expectations", "years": "5-10"},
            "telemedicine": {"phase": "Plateau of Productivity", "years": "<2"},
            "wearable_health": {"phase": "Slope of Enlightenment", "years": "2-5"},
        }
    },
    "space_tech": {
        "label": "Space Technology",
        "phase": "Slope of Enlightenment",
        "years_to_plateau": "5-10 years",
        "sub_technologies": {
            "satellite_internet": {"phase": "Slope of Enlightenment", "years": "2-5"},
            "space_tourism": {"phase": "Innovation Trigger", "years": "5-10"},
            "reusable_launch": {"phase": "Plateau of Productivity", "years": "<2"},
            "in_space_manufacturing": {"phase": "Innovation Trigger", "years": "10+"},
        }
    },
}
```

### Integration into Pipeline

```python
# Add Gartner phase to article metadata
def classify_technology_maturity(article: dict) -> dict:
    """Classify article's technology against Gartner Hype Cycle"""
    text = f"{article.get('title', '')} {article.get('summary', '')}".lower()

    for tech_key, tech_data in GARTNER_HYPE_CYCLE_2026.items():
        for sub_key, sub_data in tech_data.get("sub_technologies", {}).items():
            if sub_key.replace("_", " ") in text:
                return {
                    "technology": tech_data["label"],
                    "sub_technology": sub_key.replace("_", " ").title(),
                    "hype_cycle_phase": sub_data["phase"],
                    "years_to_plateau": sub_data["years"],
                }

        # Check main technology
        if tech_data["label"].lower() in text:
            return {
                "technology": tech_data["label"],
                "sub_technology": "General",
                "hype_cycle_phase": tech_data["phase"],
                "years_to_plateau": tech_data["years_to_plateau"],
            }

    return {"technology": "Unclassified", "hype_cycle_phase": "Unknown"}
```

---

## 10. Investment & Funding Tracking

### Funding Data Pipeline

```python
class FundingTracker:
    """Track investment and funding across all industries"""

    def __init__(self):
        self.sources = [
            self.crunchbase_funding,
            self.sec_filings_funding,
            self.news_funding_extraction,
        ]

    def extract_funding(self, article: dict) -> Optional[dict]:
        """Extract funding data from article using GPT-4o-mini"""
        prompt = f"""Extract funding information from this article if present.

TITLE: {article.get('title', '')}
SUMMARY: {article.get('summary', '')}

If funding data exists, return JSON:
{{
  "company": "string",
  "amount_usd": float,
  "round": "Seed|Series_A|Series_B|Series_C|Series_D|Series_E|IPO|Grant|Debt|M&A|Unknown",
  "investors": ["list"],
  "valuation_usd": float (optional),
  "date": "ISO date",
  "confidence": 0.0-1.0
}}
If no funding data, return: {{"found": false}}"""

        try:
            llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.0)
            resp = llm.invoke(prompt)
            data = json.loads(resp.content)
            if data.get("found") == False:
                return None
            return data
        except:
            return None

    def get_top_funding_rounds(self, days: int = 7, min_amount: float = 50_000_000) -> list:
        """Get top funding rounds from database"""
        engine = create_engine(DATABASE_URL)
        Session = sessionmaker(bind=engine)
        session = Session()

        cutoff = datetime.utcnow() - timedelta(days=days)
        rounds = (
            session.query(Article)
            .filter(
                Article.funding_amount_usd >= min_amount,
                Article.published >= cutoff,
                Article.funding_amount_usd.isnot(None)
            )
            .order_by(Article.funding_amount_usd.desc())
            .limit(50)
            .all()
        )
        session.close()

        return [
            {
                "company": a.title.split(" raises ")[0] if " raises " in (a.title or "") else a.title,
                "amount_usd": a.funding_amount_usd,
                "round": a.funding_round,
                "source": a.url,
                "industry_tags": a.industry_tags,
                "date": a.published.isoformat() if a.published else None,
            }
            for a in rounds
        ]

    def funding_by_industry(self, days: int = 30) -> dict:
        """Aggregate funding by industry"""
        rounds = self.get_top_funding_rounds(days=days, min_amount=0)

        industry_totals = {}
        for r in rounds:
            for tag in r.get("industry_tags", ["Uncategorized"]):
                if tag not in industry_totals:
                    industry_totals[tag] = {"total": 0, "count": 0, "rounds": []}
                industry_totals[tag]["total"] += r["amount_usd"]
                industry_totals[tag]["count"] += 1
                industry_totals[tag]["rounds"].append(r)

        # Sort by total
        sorted_industries = sorted(
            industry_totals.items(),
            key=lambda x: x[1]["total"],
            reverse=True
        )

        return {
            "total_funding_usd": sum(r["amount_usd"] for r in rounds),
            "total_rounds": len(rounds),
            "industries": [
                {
                    "name": name,
                    "total_funding_usd": data["total"],
                    "rounds_count": data["count"],
                    "top_rounds": sorted(data["rounds"], key=lambda x: x["amount_usd"], reverse=True)[:5],
                }
                for name, data in sorted_industries
            ]
        }
```

---

## 11. Complete Implementation Roadmap

### Phase 0 — Foundation (Week 1-2)

```
Day 1-2:  Database setup (PostgreSQL + Pinecone)
Day 3-4:  Config with 130+ industry categories
Day 5-6:  Multi-source ingestion engines (7 APIs)
Day 7-8:  FastAPI backend with WebSocket
Day 9-10: Basic pipeline execution
```

### Phase 1 — Intelligence (Week 3-4)

```
Day 11-12: LangGraph orchestration with state management
Day 13-14: RAG pipeline (chunk → embed → store → retrieve)
Day 15-16: GPT-4o insight extraction agent
Day 17-18: Real-time alert agent with push notifications
Day 19-20: Gartner Hype Cycle classification
```

### Phase 2 — Frontend (Week 5-6)

```
Day 21-23: Next.js dashboard (charts, articles, alerts)
Day 24-26: Flutter mobile app (iOS + Android)
Day 27-28: Real-time WebSocket updates
Day 29-30: Auth0 SSO + user preferences
```

### Phase 3 — Enterprise (Week 7-8)

```
Day 31-32: Multi-tenant organization support
Day 33-34: Custom industry watchlists per user
Day 35-36: Export to PDF/Excel/CSV
Day 37-38: Slack/Teams/Email integration
Day 39-40: Load testing, monitoring, deployment
```

### Docker Compose

```yaml
# docker-compose.yml
version: "3.9"

services:
  postgres:
    image: postgres:16
    environment:
      POSTGRES_DB: techintel
      POSTGRES_USER: techintel
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  elasticsearch:
    image: elasticsearch:8.12
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
    ports:
      - "9200:9200"

  api:
    build: ./enterprise_engine
    environment:
      - DATABASE_URL=postgresql://techintel:${DB_PASSWORD}@postgres/techintel
      - REDIS_URL=redis://redis:6379/0
      - PINECONE_API_KEY=${PINECONE_API_KEY}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - SERPER_API_KEY=${SERPER_API_KEY}
    depends_on:
      - postgres
      - redis
    ports:
      - "8000:8000"

  web:
    build: ./enterprise-dashboard
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:8000
      - AUTH0_SECRET=${AUTH0_SECRET}
    ports:
      - "3000:3000"
    depends_on:
      - api

  celery_worker:
    build: ./enterprise_engine
    command: celery -A enterprise_engine.tasks worker --loglevel=info
    environment:
      - DATABASE_URL=postgresql://techintel:${DB_PASSWORD}@postgres/techintel
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - postgres
      - redis

  celery_beat:
    build: ./enterprise_engine
    command: celery -A enterprise_engine.tasks beat --loglevel=info
    environment:
      - DATABASE_URL=postgresql://techintel:${DB_PASSWORD}@postgres/techintel
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - postgres
      - redis

volumes:
  postgres_data:
```

---

## Summary: Current vs. Enterprise

| Capability | TechPulse Daily (Current) | Enterprise Platform (Target) |
|-----------|--------------------------|------------------------------|
| **Industries** | 20 domains | 130+ categories across 18 sectors |
| **Keywords** | ~300 | 1,000+ |
| **Sources** | RSS + Web + Serper | 7 APIs + 20 RSS + Crunchbase + SEC |
| **Articles/Cycle** | ~200 | 500+ |
| **AI Model** | GPT-4o-mini | GPT-4o + GPT-4o-mini |
| **Orchestration** | Sequential (agent.py) | LangGraph state graph |
| **RAG** | None (full text pass) | Pinecone + embedding + semantic search |
| **Vector DB** | None | Pinecone (3072-dim embeddings) |
| **LangChain** | None | Full agent tools + retrievers |
| **Frontend** | Flask + Jinja2 | Next.js + Flutter |
| **Real-time** | REST polling | WebSocket + push notifications |
| **Gartner** | None | Hype Cycle classification |
| **Funding** | None | Crunchbase + SEC + AI extraction |
| **Alerts** | None | Severity-based push alerts |
| **Auth** | None | Auth0 SSO |
| **Mobile** | None | iOS + Android (Flutter) |

---

*End of Enterprise Expansion Plan — Next-gen AI Intelligence Platform*
