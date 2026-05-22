INDUSTRY_CATEGORIES = {
    "technology": {
        "label": "Technology",
        "sub_industries": {
            "ai_agents": {"keywords": ["AI agent", "agentic", "multi-agent", "agent orchestration", "autonomous agent"]},
            "artificial_intelligence": {"keywords": ["machine learning", "deep learning", "neural network", "generative AI", "LLM", "GPT", "transformer", "foundation model"]},
            "quantum_computing": {"keywords": ["quantum", "qubit", "quantum computing", "quantum error correction", "quantum cryptography", "quantum processor"]},
            "robotics": {"keywords": ["robot", "humanoid", "robotic", "drone", "autonomous robot", "cobot", "manipulator"]},
            "semiconductor": {"keywords": ["chip", "semiconductor", "GPU", "foundry", "TSMC", "processor", "ASML", "EUV", "lithography"]},
            "cybersecurity": {"keywords": ["cyber", "security", "ransomware", "breach", "zero-day", "malware", "threat intelligence", "firewall"]},
            "cloud_native": {"keywords": ["cloud", "Kubernetes", "Docker", "serverless", "microservice", "AWS", "Azure", "GCP"]},
            "data_infrastructure": {"keywords": ["data engineering", "data lake", "data warehouse", "Spark", "Kafka", "Snowflake", "Databricks"]},
            "developer_tools": {"keywords": ["IDE", "code generation", "CI/CD", "open source", "API", "developer tool", "GitHub"]},
            "blockchain_web3": {"keywords": ["blockchain", "DeFi", "crypto", "NFT", "Web3", "smart contract", "tokenization", "CBDC"]},
        }
    },
    "healthcare_life_sciences": {
        "label": "Healthcare & Life Sciences",
        "sub_industries": {
            "healthcare_ai": {"keywords": ["medical AI", "health AI", "diagnostic AI", "clinical AI", "hospital AI", "health tech", "digital health"]},
            "biotech": {"keywords": ["biotech", "genomics", "CRISPR", "gene therapy", "synthetic biology", "bioinformatics"]},
            "pharma": {"keywords": ["pharma", "drug discovery", "clinical trial", "FDA", "therapeutic", "medicine"]},
            "medtech": {"keywords": ["medical device", "wearable", "imaging", "diagnostic", "patient monitoring", "medtech"]},
            "neurotech": {"keywords": ["brain-computer", "neural implant", "neurotech", "neuroimaging", "brain interface"]},
            "longevity": {"keywords": ["longevity", "anti-aging", "regenerative medicine", "senolytic", "epigenetic"]},
        }
    },
    "financial_services": {
        "label": "Financial Services",
        "sub_industries": {
            "fintech": {"keywords": ["fintech", "digital payment", "mobile banking", "neobank", "open banking", "embedded finance", "BNPL"]},
            "insurtech": {"keywords": ["insurtech", "insurance AI", "claims automation", "underwriting AI"]},
            "wealthtech": {"keywords": ["wealthtech", "robo-advisor", "wealth management", "trading platform", "portfolio"]},
            "regtech": {"keywords": ["regtech", "compliance", "AML", "KYC", "regulatory reporting", "fraud detection"]},
            "defi": {"keywords": ["DeFi", "decentralized finance", "lending protocol", "DEX", "yield farming", "staking"]},
        }
    },
    "industrial_manufacturing": {
        "label": "Industrial & Manufacturing",
        "sub_industries": {
            "industry_4_0": {"keywords": ["smart factory", "digital twin", "predictive maintenance", "industrial IoT", "SCADA", "MES", "PLC"]},
            "additive_manufacturing": {"keywords": ["3D printing", "additive manufacturing", "metal 3D printing", "bioprinting"]},
            "mechanical_engineering": {"keywords": ["mechanical engineering", "CAD", "finite element", "thermodynamic", "machine design"]},
            "electrical_engineering": {"keywords": ["electrical engineering", "power system", "circuit design", "embedded system", "VLSI"]},
            "civil_engineering": {"keywords": ["civil engineering", "structural engineering", "construction tech", "BIM", "infrastructure"]},
            "supply_chain": {"keywords": ["supply chain", "logistics", "warehouse", "inventory", "last mile", "delivery"]},
        }
    },
    "energy_utilities": {
        "label": "Energy & Utilities",
        "sub_industries": {
            "renewable_energy": {"keywords": ["solar", "wind", "hydropower", "geothermal", "renewable energy", "clean energy"]},
            "nuclear_energy": {"keywords": ["nuclear", "fusion", "fission", "SMR", "nuclear reactor", "thorium"]},
            "hydrogen": {"keywords": ["hydrogen", "green hydrogen", "fuel cell", "hydrogen storage"]},
            "battery_tech": {"keywords": ["battery", "lithium-ion", "solid-state", "energy storage", "sodium-ion"]},
            "carbon_capture": {"keywords": ["carbon capture", "CCUS", "direct air capture", "carbon removal", "carbon storage"]},
            "smart_grid": {"keywords": ["smart grid", "grid modernization", "microgrid", "demand response", "energy management"]},
        }
    },
    "automotive_transport": {
        "label": "Automotive & Transport",
        "sub_industries": {
            "automotive": {"keywords": ["automotive", "electric vehicle", "EV", "connected car", "V2X", "LIDAR", "ADAS"]},
            "autonomous_vehicles": {"keywords": ["self-driving", "autonomous vehicle", "robotaxi", "Waymo", "Tesla FSD", "autonomous truck", "Cruise"]},
            "e_mobility": {"keywords": ["e-scooter", "e-bike", "micromobility", "charging infrastructure", "battery swap"]},
            "aviation": {"keywords": ["aviation", "eVTOL", "air taxi", "drone", "electric aviation", "sustainable aviation fuel"]},
            "maritime": {"keywords": ["maritime", "autonomous ship", "smart port", "shipping", "marine tech"]},
        }
    },
    "space_aerospace": {
        "label": "Space & Aerospace",
        "sub_industries": {
            "space_exploration": {"keywords": ["space", "NASA", "SpaceX", "Mars", "lunar", "starship", "deep space", "asteroid"]},
            "satellite": {"keywords": ["satellite", "Starlink", "earth observation", "remote sensing", "LEO", "satellite communication"]},
            "aerospace": {"keywords": ["aerospace", "aircraft", "avionics", "propulsion", "defense aerospace"]},
            "space_commerce": {"keywords": ["space tourism", "commercial space", "space station", "space manufacturing"]},
        }
    },
    "real_estate_construction": {
        "label": "Real Estate & Construction",
        "sub_industries": {
            "proptech": {"keywords": ["proptech", "real estate AI", "property tech", "smart building", "real estate analytics"]},
            "construction_tech": {"keywords": ["construction tech", "BIM", "modular construction", "smart construction", "robotic construction"]},
            "smart_cities": {"keywords": ["smart city", "urban tech", "city IoT", "urban mobility", "public safety tech"]},
        }
    },
    "agriculture_food": {
        "label": "Agriculture & Food",
        "sub_industries": {
            "agritech": {"keywords": ["agritech", "precision agriculture", "farm AI", "smart farming", "agricultural robot", "drone farming"]},
            "foodtech": {"keywords": ["foodtech", "alternative protein", "cultivated meat", "plant-based", "food AI", "smart kitchen"]},
            "vertical_farming": {"keywords": ["vertical farming", "indoor farming", "hydroponics", "aeroponics", "controlled environment"]},
        }
    },
    "education": {
        "label": "Education",
        "sub_industries": {
            "edtech": {"keywords": ["edtech", "AI education", "learning management", "personalized learning", "adaptive learning", "online learning"]},
            "corporate_training": {"keywords": ["corporate training", "enterprise learning", "LMS", "skills tech", "VR training"]},
        }
    },
    "government_public": {
        "label": "Government & Public Sector",
        "sub_industries": {
            "govtech": {"keywords": ["govtech", "government AI", "digital government", "e-governance", "public sector tech", "civic tech"]},
            "defense_tech": {"keywords": ["defense", "military tech", "C4ISR", "defense AI", "autonomous weapon"]},
            "public_safety": {"keywords": ["public safety", "emergency response", "police tech", "disaster tech"]},
        }
    },
    "media_entertainment": {
        "label": "Media & Entertainment",
        "sub_industries": {
            "media_tech": {"keywords": ["media tech", "content AI", "news AI", "journalism tech", "digital media"]},
            "gaming": {"keywords": ["gaming", "game AI", "game development", "cloud gaming", "Unity", "Unreal Engine", "esports"]},
            "sportstech": {"keywords": ["sports tech", "sports analytics", "athlete AI", "smart stadium", "wearable sport"]},
        }
    },
    "marketing_sales": {
        "label": "Marketing & Sales",
        "sub_industries": {
            "martech": {"keywords": ["martech", "marketing AI", "marketing automation", "CRM AI", "personalization", "SEO AI", "ad tech"]},
            "adtech": {"keywords": ["adtech", "programmatic advertising", "ad AI", "demand side platform", "ad attribution"]},
            "sales_tech": {"keywords": ["sales tech", "sales AI", "sales intelligence", "revenue intelligence", "CPQ"]},
        }
    },
    "legal_hr": {
        "label": "Legal & HR",
        "sub_industries": {
            "legaltech": {"keywords": ["legaltech", "legal AI", "contract analysis", "legal research", "e-discovery", "compliance tech"]},
            "hrtech": {"keywords": ["HR tech", "talent analytics", "recruitment AI", "people analytics", "workforce planning", "payroll tech"]},
        }
    },
    "telecom_connectivity": {
        "label": "Telecom & Connectivity",
        "sub_industries": {
            "telecom": {"keywords": ["5G", "6G", "telecom AI", "network automation", "Open RAN", "private network", "network slicing"]},
            "iot": {"keywords": ["IoT", "internet of things", "industrial IoT", "smart home", "edge device", "IoT platform"]},
        }
    },
    "trading_commodities": {
        "label": "Trading & Commodities",
        "sub_industries": {
            "algorithmic_trading": {"keywords": ["algorithmic trading", "quant trading", "AI trading", "high frequency trading", "trading bot"]},
            "commodities": {"keywords": ["commodity", "oil trading", "gold trading", "commodity market"]},
            "crypto_trading": {"keywords": ["crypto trading", "crypto exchange", "trading bot", "market analysis"]},
        }
    },
    "business_services": {
        "label": "Business Services",
        "sub_industries": {
            "consulting": {"keywords": ["consulting", "digital transformation", "strategy consulting", "tech consulting", "management consulting"]},
            "accounting": {"keywords": ["accounting AI", "audit AI", "financial planning", "tax tech", "CFO tech"]},
        }
    },
    "real_estate_property": {
        "label": "Real Estate & Property",
        "sub_industries": {
            "commercial_real_estate": {"keywords": ["commercial real estate", "CRE", "office tech", "retail real estate", "industrial real estate"]},
            "residential_real_estate": {"keywords": ["residential real estate", "smart home", "home tech", "property management", "real estate marketplace"]},
        }
    },
    "vibe_coding": {
        "label": "Vibe Coding & AI Development",
        "sub_industries": {
            "ai_coding_tools": {"keywords": ["vibe coding", "AI coding", "Cursor", "Windsurf", "Replit AI", "code generation AI", "AI software engineering", "aider"]},
            "ai_assisted_dev": {"keywords": ["AI assistant coding", "copilot", "code completion AI", "AI developer tools", "LLM coding"]},
        }
    },
}


def get_all_industries() -> list:
    result = []
    for sector_key, sector_data in INDUSTRY_CATEGORIES.items():
        for sub_key, sub_data in sector_data["sub_industries"].items():
            result.append({
                "sector": sector_data["label"],
                "sector_key": sector_key,
                "industry": sub_key.replace("_", " ").title(),
                "industry_key": sub_key,
                "keywords": sub_data["keywords"],
            })
    return result


def get_all_keywords() -> list:
    keywords = []
    for sector_data in INDUSTRY_CATEGORIES.values():
        for sub_data in sector_data["sub_industries"].values():
            keywords.extend(sub_data["keywords"])
    return list(set(keywords))


def tag_article(text: str) -> list:
    text_lower = text.lower()
    tags = []
    for sector_key, sector_data in INDUSTRY_CATEGORIES.items():
        for sub_key, sub_data in sector_data["sub_industries"].items():
            for kw in sub_data["keywords"]:
                if kw.lower() in text_lower:
                    tags.append({
                        "sector": sector_data["label"],
                        "industry": sub_key.replace("_", " ").title(),
                        "matched_keyword": kw,
                    })
                    break
    return tags


def tag_industries(text: str) -> list:
    return list(set(t["industry"] for t in tag_article(text)))


def tag_sectors(text: str) -> list:
    return list(set(t["sector"] for t in tag_article(text)))
