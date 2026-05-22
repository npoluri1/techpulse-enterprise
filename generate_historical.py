import os
import re
import yaml
import random
import logging
from pathlib import Path
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

SGT = ZoneInfo("Asia/Singapore")

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger("HistoricalGen")

CONFIG_PATH = Path("config.yaml")
OUTPUT_DIR = Path("output")

DOMAIN_TEMPLATES = {
    "ai_agents": {
        "label": "AI Agents",
        "articles": [
            "OpenAI announces GPT-{ver}, claims {metric} improvement over previous model",
            "Anthropic releases Claude {ver} with enhanced {feature} capabilities",
            "Google DeepMind unveils {project}, a breakthrough in {field}",
            "New benchmark shows {n}% improvement in AI reasoning tasks",
            "Meta releases open-source {model} model with {param}B parameters",
            "{company} launches AI agent platform for enterprise automation",
            "Researchers achieve {metric} on {benchmark} using novel architecture",
            "AI coding assistant {tool} reaches {n}M developers milestone",
            "Study finds AI models still struggle with {task} tasks",
            "OpenAI partners with {company} to bring AI to {industry}",
            "New technique reduces LLM inference cost by {n}%",
            "AI safety researchers propose new framework for {topic}",
            "Open-source LLM {model} matches proprietary models on key benchmarks",
            "{company} raises ${n}B for AI agent development",
            "EU AI Act enforcement begins for {category} systems",
            "Survey finds {n}% of enterprises now using generative AI",
            "New AI model can {capability}, researchers demonstrate",
            "Microsoft invests ${n}B in AI infrastructure expansion",
            "AI-powered {tool} transforms {industry} workflow",
            "Debate intensifies over open-source vs closed AI models",
        ],
    },
    "autonomous_vehicles": {
        "label": "Autonomous Vehicles",
        "articles": [
            "Waymo expands robotaxi service to {city}, covering {n} square miles",
            "Tesla delivers record {n}K vehicles in Q{q} {year}",
            "Cruise receives approval for autonomous testing in {city}",
            "LiDAR costs drop below ${n} per unit, accelerating AV adoption",
            "NVIDIA unveils next-gen {chip} for autonomous driving",
            "Zoox tests autonomous vehicle on public roads in {city}",
            "BYD announces ${n}B investment in autonomous driving tech",
            "NHTSA opens investigation into {company} autonomous system",
            "Mobileye reports {n}% revenue growth from ADAS solutions",
            "Aurora targets {year} for commercial autonomous trucking launch",
            "XPeng rolls out {feature} to all P7 vehicles via OTA update",
            "California DMV issues new regulations for autonomous vehicle testing",
            "Baidu's Apollo Go surpasses {n}M autonomous rides milestone",
            "Toyota announces partnership with {company} for autonomous tech",
            "Volvo unveils {model} with integrated autonomous driving system",
            "Samsung develops {tech} chip for autonomous vehicle processing",
            "Uber returns to autonomous vehicles with new strategy",
            "Electric vehicle sales reach {n}% of total auto market",
            "Hyundai invests ${n}B in autonomous and electric vehicles",
            "Autonomous delivery robots deployed in {n} new cities",
        ],
    },
    "business_innovation": {
        "label": "Business Innovation",
        "articles": [
            "AI adoption drives {n}% productivity gain in {industry} sector",
            "{company} launches digital transformation initiative across {n} divisions",
            "Retail giant {company} deploys AI-powered inventory management",
            "Fintech startup {company} raises ${n}M for {solution} platform",
            "Remote work technology market reaches ${n}B valuation",
            "{company} reports record revenue from cloud services",
            "Smart city project in {city} uses IoT sensors for {purpose}",
            "Education technology platform {tool} reaches {n}M students",
            "{industry} sector sees {n}% increase in technology spending",
            "{company} partners with {company2} to accelerate innovation",
            "Digital payments surpass ${n}T in annual transaction volume",
            "AI-powered customer service reduces response time by {n}%",
            "Blockchain technology finds new applications in {industry}",
            "{company} launches gig economy platform for {service}",
            "Sustainable business practices drive {n}% cost savings for {company}",
            "5G technology enables new {industry} applications in {city}",
            "Corporate venture capital investments hit record ${n}B in Q{q}",
            "Startup ecosystem in {city} produces {n} new unicorns this year",
            "{company} implements four-day work week, reports {n}% productivity increase",
            "Augmented reality transforms {industry} customer experience",
        ],
    },
    "cloud_native": {
        "label": "Cloud Native",
        "articles": [
            "AWS announces {n} new services for {category} workloads",
            "Kubernetes reaches {n}M production clusters worldwide",
            "Google Cloud launches {product} for serverless computing",
            "Azure introduces new {feature} for hybrid cloud deployments",
            "Docker introduces {tool} for container orchestration at scale",
            "CNCF graduates {project} as a stable cloud-native project",
            "Terraform adds support for {provider} cloud resources",
            "Platform engineering adoption grows {n}% among enterprises",
            "WebAssembly gains traction in cloud-native computing",
            "eBPF technology enables new {capability} for Linux systems",
            "{company} migrates {n}% of workloads to cloud, saves ${n}M",
            "Edge computing market expected to reach ${n}B by {year}",
            "Service mesh adoption reaches {n}% of Kubernetes users",
            "Serverless framework {tool} releases version {ver} with new features",
            "Multi-cloud strategy adopted by {n}% of Fortune 500 companies",
            "Chaos engineering platform {tool} helps companies improve reliability",
            "Cloud cost optimization becomes top priority for {n}% of enterprises",
            "GitOps methodology gains mainstream adoption in DevOps",
            "New {tech} standard promises better cloud interoperability",
            "FinOps practices help companies reduce cloud spend by {n}%",
        ],
    },
    "cybersecurity": {
        "label": "Cybersecurity",
        "articles": [
            "Major ransomware attack targets {industry}, affecting {n} organizations",
            "Zero-day vulnerability discovered in {software} affects millions",
            "AI-powered security platform {tool} detects {n} novel threats",
            "Data breach at {company} exposes {n}M user records",
            "CISA issues emergency directive for {vulnerability} patch",
            "Phishing attacks increase {n}% using AI-generated content",
            "New malware variant {name} targets cloud infrastructure",
            "Quantum computing threatens current encryption standards",
            "Ransomware payments exceed ${n}B in {year}",
            "Identity-based attacks account for {n}% of all breaches",
            "Security researchers discover {vulnerability} in widely-used library",
            "Zero Trust architecture adoption grows {n}% among enterprises",
            "Nation-state threat actor targets critical infrastructure in {sector}",
            "SEC announces new cybersecurity disclosure rules for public companies",
            "Bug bounty program at {company} pays record ${n}M in rewards",
            "Supply chain attack compromises {n} organizations via {vector}",
            "Cyber insurance premiums rise {n}% following surge in claims",
            "New {tech} authentication standard promises stronger security",
            "DDoS attacks reach record size, exceeding {n} Tbps",
            "SOC teams face burnout as alert volumes increase {n}%",
        ],
    },
    "data_ai_infra": {
        "label": "Data & AI Infrastructure",
        "articles": [
            "Apache Spark {ver} introduces {feature} for faster data processing",
            "Kafka adoption reaches {n}K production deployments globally",
            "Databricks launches {product} for data lakehouse optimization",
            "Snowflake reports {n}% revenue growth in Q{q}",
            "Data mesh architecture adopted by {n}% of large enterprises",
            "Real-time data streaming market hits ${n}B milestone",
            "dbt introduces new {feature} for data transformation workflows",
            "Data quality platform {tool} raises ${n}M in Series {series}",
            "MLOps platform {tool} achieves {n}% improvement in model deployment time",
            "Data catalog market grows to ${n}B as governance becomes priority",
            "{company} open-sources {tool} for feature store management",
            "Data observability platform {tool} detects {n} anomalies per day",
            "Lakehouse architecture adoption doubles in {industry} sector",
            "Flink {ver} release brings {feature} for stream processing",
            "Vector databases gain traction for AI applications",
            "Data contracts emerge as best practice for data teams",
            "Reverse ETL platform {tool} connects data warehouses to operational tools",
            "Data marketplace platforms enable {n}% more data sharing",
            "Metadata management startup {company} achieves unicorn status",
            "Data pipeline orchestration tool {tool} processes {n} workflows daily",
        ],
    },
    "developer_tools": {
        "label": "Developer Tools",
        "articles": [
            "GitHub Copilot now supports {n} programming languages",
            "VS Code reaches {n}M monthly active developers",
            "Python {ver} introduces performance improvements of {n}%",
            "Rust gains traction in {industry} development",
            "JetBrains releases {tool} for collaborative development",
            "WebAssembly support expands to {n} new platforms",
            "TypeScript adoption grows to {n}% of JavaScript developers",
            "Docker Desktop {ver} introduces {feature} for developers",
            "PostgreSQL {ver} released with major performance enhancements",
            "Kubernetes development tool {tool} simplifies local development",
            "Open-source {tool} reaches {n}K GitHub stars",
            "AI code review tool {tool} catches {n}% more bugs",
            "GraphQL adoption grows {n}% in web development",
            "New Rust-based {tool} outperforms existing solutions by {n}x",
            "Developer experience platform {tool} raises ${n}M",
            "Low-code platform {tool} enables {n}M citizen developers",
            "Serverless framework {tool} reaches version {ver} milestone",
            "API platform {tool} processes {n}B requests per month",
            "Zig programming language {ver} introduces {feature}",
            "Software supply chain security tool {tool} detects {n} vulnerabilities",
        ],
    },
    "energy_cleantech": {
        "label": "Energy & Cleantech",
        "articles": [
            "Solar energy capacity reaches {n} GW globally",
            "Battery storage costs drop {n}%, making renewable energy more viable",
            "Nuclear fusion startup {company} achieves {milestone}",
            "Wind energy generates {n}% of electricity in {country}",
            "Electric vehicle battery range exceeds {n} miles",
            "Hydrogen fuel cell technology achieves {milestone} breakthrough",
            "Carbon capture startup {company} removes {n}K tons of CO2",
            "{country} pledges {n}% reduction in emissions by {year}",
            "Grid-scale battery storage deployment grows {n}%",
            "Solar panel efficiency reaches new record of {n}%",
            "Green hydrogen production costs fall below ${n}/kg",
            "Climate tech investments reach ${n}B in Q{q}",
            "Energy grid modernization project in {city} reduces outages by {n}%",
            "Sustainable aviation fuel achieves {milestone} in commercial flights",
            "Nuclear power plant {name} receives approval for {n}-year extension",
            "Smart meter deployment reaches {n}M households in {country}",
            "Electric heat pump adoption grows {n}% in residential buildings",
            "Wave energy technology achieves {milestone} in ocean trials",
            "Building-integrated solar panels gain traction in urban areas",
            "Circular economy initiatives reduce waste by {n}% in {industry}",
        ],
    },
    "fintech": {
        "label": "Fintech",
        "articles": [
            "{company} launches digital banking platform in {country}",
            "Cryptocurrency market cap reaches ${n}T milestone",
            "CBDC pilot program launches in {country} with {n} participants",
            "Blockchain payment network processes {n}M transactions per day",
            "Buy now pay later market reaches ${n}B in transaction volume",
            "Open banking regulations take effect in {country}",
            "DeFi platform {name} reaches ${n}B in total value locked",
            "AI-powered credit scoring platform {tool} approves {n}M loans",
            "Central bank digital currency transactions exceed ${n}B",
            "Stablecoin market cap grows to ${n}B",
            "Neobank {company} reaches {n}M customers in {country}",
            "Insurtech startup {company} raises ${n}M for AI underwriting",
            "Cross-border payment platform {tool} reduces transfer time to seconds",
            "Wealthtech platform {company} manages ${n}B in assets",
            "Regtech solutions help {n}% of banks automate compliance",
            "Embedded finance market expected to reach ${n}B by {year}",
            "Ripple partners with {company} for cross-border payments",
            "PayPal introduces {feature} for cryptocurrency transactions",
            "Digital wallet adoption reaches {n}% in {country}",
            "Tokenization of real-world assets gains traction in DeFi",
        ],
    },
    "gaming_xr": {
        "label": "Gaming & XR",
        "articles": [
            "Apple Vision Pro gets {n} new spatial computing apps",
            "Meta Quest {ver} sells {n}M units in first quarter",
            "Unity {ver} introduces {feature} for game developers",
            "Unreal Engine {ver} brings {feature} to real-time rendering",
            "Sony PSVR {n} sales exceed {n}M units",
            "{game_title} reaches {n}M concurrent players on Steam",
            "AR glasses from {company} feature {tech} display technology",
            "Cloud gaming platform {service} adds {n} new titles",
            "Spatial computing market projected to reach ${n}B by {year}",
            "Microsoft Mesh enables {feature} for collaborative AR",
            "Haptics technology startup {company} raises ${n}M",
            "VR training platform {tool} adopted by {n} Fortune 500 companies",
            "Nintendo Switch {ver} sells {n}M units in first week",
            "AI-powered NPCs demonstrate {capability} in new game",
            "XR collaboration platform {tool} hosts {n}K virtual meetings",
            "Mobile gaming revenue reaches ${n}B in Q{q}",
            "Indie game {title} achieves {n}M downloads on Steam",
            "Esports viewership reaches {n}M for major tournament",
            "Mixed reality headset {product} features eye-tracking technology",
            "Game engine {name} goes open source, community celebrates",
        ],
    },
    "healthcare_ai": {
        "label": "Healthcare AI",
        "articles": [
            "AI diagnostic tool {tool} achieves {n}% accuracy in detecting {condition}",
            "FDA approves AI-powered {device} for {medical_use}",
            "Drug discovery AI platform {tool} identifies {n} novel compounds",
            "AI-powered robotic surgery system performs {n}K successful procedures",
            "Digital health startup {company} raises ${n}M for {solution}",
            "Medical imaging AI detects {condition} {n}% earlier than human radiologists",
            "Electronic health record AI reduces administrative burden by {n}%",
            "Genomics AI platform {tool} sequences genome in under {n} hours",
            "Telemedicine platform {service} reaches {n}M virtual consultations",
            "AI predicts patient outcomes with {n}% accuracy in clinical trial",
            "Hospital deploys AI system to optimize bed management",
            "Wearable health device {product} monitors {condition} in real-time",
            "AI-powered mental health platform {tool} serves {n}K patients",
            "Precision medicine AI identifies optimal treatment for {condition}",
            "FDA clears AI algorithm for {imaging_modality} analysis",
            "Healthcare AI investments reach ${n}B in Q{q}",
            "AI system detects rare disease from {data_type} with {n}% sensitivity",
            "Clinical decision support tool {tool} reduces diagnostic errors by {n}%",
            "AI-powered drug repurposing identifies treatment for {condition}",
            "Remote patient monitoring platform {tool} reduces hospital readmissions by {n}%",
        ],
    },
    "industrial_ai": {
        "label": "Industrial AI",
        "articles": [
            "Smart factory initiative at {company} reduces downtime by {n}%",
            "Digital twin technology helps {company} optimize production by {n}%",
            "Predictive maintenance AI prevents {n}K hours of unplanned downtime",
            "Computer vision system {tool} achieves {n}% defect detection rate",
            "Industrial robotics market reaches ${n}B in {year}",
            "Additive manufacturing breakthrough enables {capability}",
            "AI-powered supply chain platform {tool} reduces costs by {n}%",
            "3D printing technology achieves {milestone} in {industry}",
            "Industrial IoT sensor network monitors {n}K assets in real-time",
            "Collaborative robot {model} deployed in {n} manufacturing facilities",
            "AI optimizes energy consumption in factory by {n}%",
            "Quality inspection AI system processes {n}K units per hour",
            "Manufacturing execution system {tool} integrates AI for scheduling",
            "Warehouse automation ROI reaches {n}% for early adopters",
            "AI-driven process control improves yield by {n}% in semiconductor fab",
            "Industrial edge computing platform {tool} processes {n}TB data daily",
            "Generative design AI creates {product} with {n}% less material",
            "Condition monitoring sensors prevent {n} equipment failures",
            "Robotic process automation saves {company} ${n}M annually",
            "Smart manufacturing market grows to ${n}B as Industry 4.0 accelerates",
        ],
    },
    "quantum_computing": {
        "label": "Quantum Computing",
        "articles": [
            "IBM unveils {n}-qubit quantum processor with {tech} architecture",
            "Google claims quantum supremacy milestone with {task} computation",
            "Quantum error correction breakthrough reduces error rate by {n}%",
            "{company} achieves quantum volume of {n} with new processor",
            "Quantum machine learning algorithm outperforms classical on {task}",
            "Rigetti launches {n}-qubit quantum processing unit via cloud",
            "Post-quantum cryptography standard approved by NIST",
            "IonQ announces trapped-ion quantum computer with {n} algorithmic qubits",
            "Quantum computing startup {company} raises ${n}M in Series {series}",
            "Honeywell merges quantum division with {company} to form new entity",
            "D-Wave reports {n}x speedup on optimization problem",
            "Quantum networking breakthrough enables {n}km entanglement distance",
            "Photonic quantum computer {name} achieves {milestone}",
            "Topological qubit research team demonstrates {achievement}",
            "Quantum simulation of {molecule} molecule achieved on {n} qubits",
            "AWS launches {product} quantum computing service region",
            "China invests ${n}B in quantum computing national laboratory",
            "Quantum algorithm for {problem} shows exponential speedup",
            "Cryogenic control system {product} enables scalable quantum computers",
            "Quantum-Safe cryptography transition guidance published by {organization}",
        ],
    },
    "robotics": {
        "label": "Robotics",
        "articles": [
            "Tesla Optimus robot demonstrates {task} in factory setting",
            "Boston Dynamics Atlas performs {complex_task} autonomously",
            "Figure AI raises ${n}B for general-purpose humanoid robot",
            "Unitree releases {model} humanoid robot at ${n}K price point",
            "Agility Robotics Digit deployed in {n} Spanx warehouses",
            "AI foundation model for robotics enables {capability}",
            "Humanoid robot market projected to reach ${n}B by {year}",
            "Robot dog {model} used for industrial inspection at {n} sites",
            "Service robot deployments grow {n}% in hospitality sector",
            "Warehouse robot fleet at {company} processes {n}K orders daily",
            "Robotic exoskeleton {product} helps workers reduce fatigue by {n}%",
            "Drone delivery service {service} completes {n}K deliveries per month",
            "Open-source robot platform {project} reaches {n}K users",
            "Agricultural robot {model} automates {task} with AI vision",
            "Surgical robot {system} performs {n}K successful procedures",
            "Robotaxi service {company} completes {n}K paid rides per week",
            "Autonomous mobile robot {product} deployed in {n} hospitals",
            "Robot perception system achieves {n}% accuracy in {environment}",
            "Collaborative robot safety standard updated for {application}",
            "AI-powered manipulation system {tool} handles {n} object types",
        ],
    },
    "semiconductor": {
        "label": "Semiconductor",
        "articles": [
            "TSMC begins mass production of {n}nm process technology",
            "NVIDIA Blackwell GPU delivers {n}x performance improvement in AI",
            "Intel announces {n}nm process node with {tech} technology",
            "ASML ships {n}th High-NA EUV lithography system",
            "AMD launches MI{X} AI accelerator with {n}GB HBM memory",
            "Samsung starts construction of ${n}B semiconductor fab in {location}",
            "Chiplet design standard UCIe gains {n} new members",
            "RISC-V architecture adoption grows {n}% in embedded systems",
            "ARM {arch} architecture brings {n}% performance gain",
            "Global chip shortage eases, lead times drop to {n} weeks",
            "Apple M{chip} delivers {n}x faster AI inference performance",
            "SK Hynix starts mass production of {n}-layer NAND flash",
            "SiFive raises ${n}M for RISC-V processor development",
            "Advanced packaging market reaches ${n}B as chiplets gain traction",
            "Micron announces {n}-generation HBM memory with {n}% bandwidth improvement",
            "CHIPS Act funding allocated: ${n}B to {company} for US fab",
            "Quantum dot display technology achieves {milestone} in manufacturing",
            "Gallium nitride semiconductor market grows to ${n}B",
            "EUV lithography tool {model} enables {n}nm features",
            "Global semiconductor revenue reaches ${n}B in {year}",
        ],
    },
    "space_tech": {
        "label": "Space Tech",
        "articles": [
            "SpaceX Starship completes {milestone} test flight",
            "NASA Artemis program achieves {milestone} with lunar mission",
            "Blue Origin New Glenn rocket reaches orbit on first attempt",
            "Starlink constellation reaches {n}K satellites in orbit",
            "Rocket Lab launches {n}th Electron mission of the year",
            "Mars rover {name} discovers {finding} on Martian surface",
            "ULA Vulcan Centaur rocket makes successful debut launch",
            "JAXA SLIM spacecraft achieves precision moon landing",
            "Space station {name} reaches {n} years of continuous habitation",
            "Asteroid mining startup {company} raises ${n}M",
            "Space solar power prototype demonstrates {tech} in orbit",
            "ESA launches {mission} to study {celestial_body}",
            "Commercial space station {name} passes design review",
            "Satellite constellation {service} provides global internet coverage",
            "China's Tiangong space station expands with {module} module",
            "Space debris removal mission {name} successfully captures debris",
            "Virgin Galactic completes {n}th spaceflight with tourists",
            "Relativity Space 3D-printed rocket {name} achieves orbit",
            "Venus mission {name} reveals {finding} about atmosphere",
            "Deep space atomic clock enables {capability} for navigation",
        ],
    },
}

COMPANIES = [
    "Google", "Microsoft", "Apple", "Amazon", "Meta", "NVIDIA", "Intel",
    "AMD", "IBM", "Oracle", "Salesforce", "Adobe", "SAP", "Tesla",
    "Samsung", "Sony", "LG", "Huawei", "Tencent", "Alibaba", "Baidu",
    "ByteDance", "Spotify", "Uber", "Airbnb", "Netflix", "Palantir",
    "CrowdStrike", "Cloudflare", "Datadog", "Snowflake", "Databricks",
    "MongoDB", "Elastic", "Confluent", "HashiCorp", "GitLab", "GitHub",
]

CITIES = [
    "San Francisco", "New York", "London", "Tokyo", "Singapore", "Berlin",
    "Beijing", "Shanghai", "Seoul", "Sydney", "Dubai", "Toronto",
    "Austin", "Seattle", "Boston", "Los Angeles", "Paris", "Stockholm",
]

COUNTRIES = [
    "United States", "China", "Japan", "United Kingdom", "Germany",
    "Singapore", "South Korea", "India", "Canada", "Australia",
    "France", "Sweden", "Norway", "United Arab Emirates",
]


def gen_value(placeholder):
    placeholder = placeholder.strip("{}")
    values = {
        "n": lambda: str(random.choice([3, 5, 10, 15, 20, 25, 30, 40, 45, 50, 60, 75, 80, 100, 120, 150, 200, 250, 300, 400, 500])),
        "N": lambda: str(random.choice([1, 2, 5, 10, 20, 50])),
        "ver": lambda: f"{random.choice([2, 3, 4])}.{random.choice([0, 1, 2, 5, 10])}",
        "feature": lambda: random.choice(["real-time", "multi-modal", "distributed", "federated", "edge", "serverless", "vector", "graph", "streaming", "automated"]),
        "project": lambda: random.choice(["Gemini", "Orion", "Atlas", "Nova", "Pegasus", "Titan", "Aurora", "Cortex", "Sparrow", "Raven"]),
        "field": lambda: random.choice(["natural language processing", "computer vision", "reinforcement learning", "robotics", "code generation", "mathematical reasoning"]),
        "metric": lambda: f"{random.choice([85, 90, 92, 95, 96, 97, 98, 99])}.{random.choice([0, 1, 2, 5])}%",
        "company": lambda: random.choice(COMPANIES),
        "company2": lambda: random.choice(COMPANIES),
        "industry": lambda: random.choice(["healthcare", "finance", "retail", "manufacturing", "education", "energy", "transportation", "agriculture"]),
        "model": lambda: random.choice(["Llama 4", "Falcon 2", "Mistral Large", "Gemma 2", "Phi-3", "Claude 4", "GPT-5", "Yi-34B", "DeepSeek-V3", "Cohere"]),
        "task": lambda: random.choice(["reasoning", "planning", "memory", "tool use", "multi-step", "long context", "summarization", "code generation"]),
        "tool": lambda: random.choice(["LangChain", "AutoGPT", "CrewAI", "Haystack", "LlamaIndex", "Guardrails", "Weights & Biases", "Comet", "MLflow", "Kubeflow"]),
        "B": lambda: f"{random.choice([1, 2, 3, 5, 10, 15, 20, 30, 50, 100])}",
        "M": lambda: f"{random.choice([1, 2, 5, 10, 20, 50, 100, 200, 500])}",
        "K": lambda: f"{random.choice([1, 5, 10, 20, 50, 100, 200, 500])}",
        "city": lambda: random.choice(CITIES),
        "country": lambda: random.choice(COUNTRIES),
        "year": lambda: str(random.choice([2024, 2025])),
        "q": lambda: str(random.choice([1, 2, 3, 4])),
        "param": lambda: str(random.choice([7, 13, 30, 34, 40, 70, 120, 180, 405])),
        "benchmark": lambda: random.choice(["MMLU", "HumanEval", "GSM8K", "HellaSwag", "ARC Challenge", "BIG-Bench", "SWE-bench"]),
        "capability": lambda: random.choice(["generating and debugging code", "understanding long documents", "solving math problems", "planning complex tasks", "analyzing images and text", "translating between languages", "creating artwork from descriptions"]),
        "category": lambda: random.choice(["high-risk", "limited-risk", "general-purpose", "large-scale", "regulated"]),
        "solution": lambda: random.choice(["AI-powered", "cloud-native", "blockchain-based", "edge computing", "quantum-safe", "zero-trust"]),
        "vulnerability": lambda: f"CVE-202{random.choice([4, 5])}-{random.randint(10000, 99999)}",
        "software": lambda: random.choice(["Windows", "Linux", "macOS", "iOS", "Android", "Chrome", "Firefox", "Safari", "Zoom", "Slack", "Teams"]),
        "sector": lambda: random.choice(["energy", "healthcare", "finance", "government", "defense", "transportation", "water"]),
        "vector": lambda: random.choice(["SolarWinds", "SolarWinds-style", "dependency confusion", "typosquatting", "malicious npm package", "third-party vendor"]),
        "name": lambda: random.choice(["LockBit 3.0", "BlackCat", "Clop", "Black Basta", "Akira", "Medusa", "RansomHouse", "BianLian"]),
        "percentage": lambda: f"{random.randint(10, 95)}%",
        "task_type": lambda: random.choice(["reasoning", "planning", "multi-step", "long-context", "code-gen"]),
        "device": lambda: random.choice(["imaging system", "monitoring device", "diagnostic tool", "screening platform", "analysis system"]),
        "medical_use": lambda: random.choice(["cancer screening", "cardiac monitoring", "neurological diagnosis", "pathology analysis", "radiology reading"]),
        "condition": lambda: random.choice(["cancer", "heart disease", "diabetes", "Alzheimer's", "pneumonia", "skin lesions", "breast cancer", "lung nodules"]),
        "imaging_modality": lambda: random.choice(["MRI", "CT", "X-ray", "ultrasound", "mammography", "pathology slide"]),
        "data_type": lambda: random.choice(["genomic data", "medical images", "EHR records", "wearable data", "lab results"]),
        "series": lambda: random.choice(["A", "B", "C", "D"]),
        "milestone": lambda: random.choice(["major milestone", "significant breakthrough", "key achievement", "historic first", "record-breaking result"]),
        "model_n": lambda: str(random.choice([3, 4, 5])),
        "tech": lambda: random.choice(["superconducting", "photonic", "silicon spin", "trapped ion", "topological", "neutral atom"]),
        "problem": lambda: random.choice(["optimization", "factorization", "search", "simulation", "scheduling"]),
        "organization": lambda: random.choice(["NIST", "ISO", "IETF", "ETSI", "IEEE"]),
        "auth": lambda: random.choice(["biometric", "passwordless", "FIDO2", "WebAuthn", "multifactor"]),
        "service": lambda: random.choice(["Starlink", "OneWeb", "Amazon Kuiper", "T-Mobile"]),
        "mission": lambda: random.choice(["Europa Clipper", "JUICE", "Hera", "Psyche", "Dragonfly", "Voyager"]),
        "celestial_body": lambda: random.choice(["Jupiter", "Mars", "Venus", "asteroids", "comets", "exoplanets"]),
        "finding": lambda: random.choice(["evidence of ancient water", "organic compounds", "unusual geological formations", "signs of volcanic activity", "ice deposits"]),
        "module": lambda: random.choice(["Mengtian", "Wentian", "Tianhe", "core module"]),
        "arch": lambda: random.choice(["v9", "v8.2", "v10"]),
        "chip": lambda: random.choice(["Thor", "Orin", "Drive", "EyeQ"]),
        "param_count": lambda: str(random.choice([7, 13, 30, 34, 40, 70, 120, 180, 405])),
        "complex_task": lambda: random.choice(["parkour", "backflip", "obstacle course", "package delivery", "stair climbing"]),
        "environment": lambda: random.choice(["warehouse", "hospital", "construction site", "office", "outdoor terrain", "factory floor"]),
        "application": lambda: random.choice(["assembly", "welding", "painting", "packaging", "inspection", "material handling"]),
        "product": lambda: random.choice(["Neural Sleeve", "PowerGlove", "LiftAssist", "FlexSuit", "BackSupport"]),
        "game_title": lambda: random.choice(["Elden Ring", "Cyberpunk 2077", "Baldur's Gate 3", "Palworld", "GTA VI", "Starfield", "Call of Duty"]),
        "label": lambda: random.choice(["AI Agents", "Autonomous Vehicles", "Business Innovation", "Cloud Native", "Cybersecurity", "Data & AI Infrastructure"]),
        "price": lambda: f"${random.choice([999, 1499, 1999, 2999, 3499])}",
        "purpose": lambda: random.choice(["traffic monitoring", "waste management", "public safety", "parking optimization", "air quality"]),
        "img": lambda: random.choice(["CT", "MRI", "X-ray", "pathology slide", "retinal scan"]),
    }
    fn = values.get(placeholder, lambda: "42")
    return fn()


def fill_template(template):
    def replacer(match):
        return gen_value(match.group(1))
    return re.sub(r"\{(\w+)\}", replacer, template)


def gen_articles_for_domain(domain_key, domain_info, count=10):
    label = domain_info["label"]
    templates = domain_info["articles"]
    articles = []
    for _ in range(count):
        t = random.choice(templates)
        title = fill_template(t)
        source = f"RSS:{random.choice(['Reddit', 'TechCrunch', 'VentureBeat', 'TheVerge', 'ArsTechnica'])}"
        url = f"https://example.com/{domain_key}/article-{random.randint(10000, 99999)}"
        summary_sentence = title[:random.randint(60, 120)].rstrip()
        if not summary_sentence.endswith((".", "!", "?")):
            summary_sentence += "."
        articles.append({
            "title": title,
            "source": source,
            "url": url,
            "summary": summary_sentence,
        })
    return articles


def build_report(domain_articles, date_str, total_count=0):
    lines = []
    lines.append(f"# TechPulse Daily -- Comprehensive Tech & Industry Digest")
    lines.append("")
    lines.append(f"> **Generated:** {date_str} 00:00 SGT | **Sources:** Historical Archive | **Mode:** AI-Generated")
    lines.append("")

    for domain_key, articles in domain_articles.items():
        label = DOMAIN_TEMPLATES[domain_key]["label"]
        lines.append(f"## {label.upper().replace(' ', '_')} -- LATEST NEWS")
        lines.append("")
        for i, a in enumerate(articles, 1):
            lines.append(f"### {i}. {a['title']}")
            lines.append(f"- **Source:** {a['source']}")
            lines.append(f"- **URL:** {a['url']}")
            lines.append(f"- **Summary:** {a['summary']}")
            lines.append("")
    return "\n".join(lines)


def try_openai_generate(domain_key, domain_label, date_str, api_key):
    if not api_key or api_key.startswith("sk-..."):
        raise ValueError("No valid API key")
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        prompt = f"""Generate {random.randint(8, 12)} realistic tech news headlines for the industry "{domain_label}" dated around {date_str}.
Each entry must have: title (concise, news-style heading), source (like "RSS:Reddit" or "WEB:TechCrunch"), and a 1-2 sentence summary.
Format as JSON list: [{{"title": "...", "source": "...", "summary": "..."}}]
Focus on realistic events and companies that would have been active in early-mid {date_str[:4]}."""
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8,
            max_tokens=2000,
        )
        import json
        text = resp.choices[0].message.content.strip()
        text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text, flags=re.DOTALL)
        data = json.loads(text)
        if isinstance(data, list):
            articles = []
            for item in data:
                articles.append({
                    "title": item.get("title", ""),
                    "source": item.get("source", f"RSS:Historical"),
                    "url": f"https://example.com/{domain_key}/archive-{random.randint(10000, 99999)}",
                    "summary": item.get("summary", ""),
                })
            if articles:
                return articles
    except Exception as e:
        logger.warning(f"OpenAI failed for {domain_label}: {e}")
    return None


def main():
    api_key = os.getenv("OPENAI_API_KEY", "")
    start_date = datetime(2024, 5, 15, tzinfo=SGT)
    end_date = datetime(2026, 5, 14, tzinfo=SGT)
    delta_days = (end_date - start_date).days
    existing = set(f.name for f in OUTPUT_DIR.glob("*.md") if f.name != ".gitkeep")

    enabled_count = sum(1 for d in DOMAIN_TEMPLATES)
    logger.info(f"Generating historical reports from {start_date.date()} to {end_date.date()}")
    logger.info(f"  Domains: {len(DOMAIN_TEMPLATES)}")
    logger.info(f"  Existing reports: {len(existing)}")
    logger.info(f"  OpenAI available: {bool(api_key) and not api_key.startswith('sk-...')}")

    weeks_per_report = 1
    current = start_date
    generated = 0
    skipped = 0

    while current <= end_date:
        date_str = current.strftime("%Y-%m-%d")
        filename = f"techpulse-daily-{date_str}.md"

        if filename in existing:
            current += timedelta(days=weeks_per_report * 7)
            skipped += 1
            continue

        domain_articles = {}
        for domain_key, domain_info in DOMAIN_TEMPLATES.items():
            articles = None
            if api_key and not api_key.startswith("sk-..."):
                try:
                    articles = try_openai_generate(domain_key, domain_info["label"], date_str, api_key)
                    if articles:
                        logger.info(f"  OpenAI: {domain_info['label']} -> {len(articles)} articles")
                except Exception:
                    pass

            if not articles:
                count = random.randint(8, 12)
                articles = gen_articles_for_domain(domain_key, domain_info, count=count)

            domain_articles[domain_key] = articles

        total_articles = sum(len(a) for a in domain_articles.values())
        report = build_report(domain_articles, date_str, total_articles)

        filepath = OUTPUT_DIR / filename
        filepath.write_text(report, encoding="utf-8")
        generated += 1
        logger.info(f"  [{date_str}] Created: {len(domain_articles)} domains, {total_articles} articles")

        current += timedelta(days=weeks_per_report * 7)

    total = generated + skipped
    logger.info(f"Done: {generated} generated, {skipped} skipped (already existed), {total} total")


if __name__ == "__main__":
    main()
