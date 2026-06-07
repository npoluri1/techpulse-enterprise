"""
AI TOOLS CATALOG
================
Comprehensive catalog of AI tools, agents, frameworks, and platforms
organized by category. Inspired by NovaPulse AI structure.

Each tool entry contains:
  - name: Official tool name
  - description: One-line summary
  - category: Primary category
  - tags: List of relevant tags
  - url: Official website or GitHub URL
  - stars: GitHub stars (approximate where noted with ~)
  - forks: GitHub forks (approximate where noted with ~)
  - openSource: True/False
  - alternativeTo: List of proprietary tools this replaces
  - featured: Whether to show in featured section
"""

AI_TOOLS_CATALOG = {
    "categories": [
        {
            "name": "AI Coding Agents",
            "icon": "💻",
            "description": "AI-powered coding assistants and development agents",
            "color": "#0071e3"
        },
        {
            "name": "AI Agent Frameworks",
            "icon": "🧩",
            "description": "Frameworks for building autonomous AI agents",
            "color": "#af52de"
        },
        {
            "name": "Vector Databases & RAG",
            "icon": "📊",
            "description": "Vector storage and retrieval augmented generation tools",
            "color": "#34c759"
        },
        {
            "name": "AI Video & Image",
            "icon": "🎬",
            "description": "AI-powered video and image generation tools",
            "color": "#ff9500"
        },
        {
            "name": "AI Voice & Audio",
            "icon": "🎙️",
            "description": "Voice synthesis, recognition, and audio AI tools",
            "color": "#ff3b30"
        },
        {
            "name": "AI Platforms & Infrastructure",
            "icon": "☁️",
            "description": "Cloud platforms and infrastructure for AI workloads",
            "color": "#5ac8fa"
        },
        {
            "name": "LLMs & Foundation Models",
            "icon": "🧠",
            "description": "Large language models and foundation AI models",
            "color": "#0071e3"
        },
        {
            "name": "AI Business & Marketing",
            "icon": "📈",
            "description": "AI tools for business, marketing, and sales",
            "color": "#ff9500"
        },
        {
            "name": "MLOps & Production",
            "icon": "⚙️",
            "description": "Tools for deploying and managing ML models in production",
            "color": "#86868b"
        },
        {
            "name": "AI Security & Compliance",
            "icon": "🛡️",
            "description": "AI security, compliance, and governance tools",
            "color": "#ff3b30"
        },
        {
            "name": "Analytics & Monitoring",
            "icon": "📉",
            "description": "AI-powered analytics and monitoring platforms",
            "color": "#34c759"
        },
        {
            "name": "Automation & Workflows",
            "icon": "🔄",
            "description": "AI workflow automation and orchestration tools",
            "color": "#af52de"
        }
    ],
    "tools": [
        # === AI CODING AGENTS ===
        {
            "name": "Claude Code",
            "description": "Anthropic's AI coding agent for terminal, IDE, and desktop",
            "category": "AI Coding Agents",
            "tags": ["coding", "agent", "Anthropic", "terminal"],
            "url": "https://github.com/anthropics/claude-code",
            "stars": 45000,
            "forks": 5200,
            "openSource": True,
            "alternativeTo": ["GitHub Copilot", "Cursor"],
            "featured": True
        },
        {
            "name": "OpenCode",
            "description": "Open source AI coding agent for terminal, IDE, and desktop with 75+ LLM providers",
            "category": "AI Coding Agents",
            "tags": ["coding", "agent", "open source", "multi-provider"],
            "url": "https://github.com/anomalyco/opencode",
            "stars": 164144,
            "forks": 19408,
            "openSource": True,
            "alternativeTo": ["Claude Code", "Cursor"],
            "featured": True
        },
        {
            "name": "Cline",
            "description": "Open-source AI coding agent for your editor and terminal with multi-file edits",
            "category": "AI Coding Agents",
            "tags": ["coding", "agent", "VS Code", "terminal"],
            "url": "https://github.com/cline/cline",
            "stars": 62198,
            "forks": 6504,
            "openSource": True,
            "alternativeTo": ["Claude Code", "Cursor"],
            "featured": True
        },
        {
            "name": "Aider",
            "description": "AI pair programming in the terminal with Git integration",
            "category": "AI Coding Agents",
            "tags": ["coding", "agent", "terminal", "Git"],
            "url": "https://github.com/paul-gauthier/aider",
            "stars": 35000,
            "forks": 4200,
            "openSource": True,
            "alternativeTo": ["GitHub Copilot"],
            "featured": True
        },
        {
            "name": "OpenAI Codex",
            "description": "All-in-one AI coding agent that creates projects from scratch",
            "category": "AI Coding Agents",
            "tags": ["coding", "agent", "OpenAI", "project generation"],
            "url": "https://github.com/openai/codex",
            "stars": 28000,
            "forks": 3500,
            "openSource": True,
            "alternativeTo": ["Claude Code", "Cursor"],
            "featured": True
        },
        {
            "name": "OpenHands",
            "description": "Open-source platform for scalable cloud coding agents",
            "category": "AI Coding Agents",
            "tags": ["coding", "agent", "cloud", "scalable"],
            "url": "https://github.com/All-Hands-AI/OpenHands",
            "stars": 74555,
            "forks": 9444,
            "openSource": True,
            "alternativeTo": ["Claude Code"],
            "featured": False
        },
        {
            "name": "Continue",
            "description": "Open-source AI code assistant for VS Code and JetBrains",
            "category": "AI Coding Agents",
            "tags": ["coding", "IDE", "VS Code", "JetBrains"],
            "url": "https://github.com/continuedev/continue",
            "stars": 25000,
            "forks": 3200,
            "openSource": True,
            "alternativeTo": ["GitHub Copilot", "Cursor"],
            "featured": False
        },
        {
            "name": "TabbyML",
            "description": "Self-hosted AI coding assistant with customizable models",
            "category": "AI Coding Agents",
            "tags": ["coding", "self-hosted", "privacy"],
            "url": "https://github.com/TabbyML/tabby",
            "stars": 28000,
            "forks": 3100,
            "openSource": True,
            "alternativeTo": ["GitHub Copilot"],
            "featured": False
        },
        {
            "name": "Goose (Block)",
            "description": "Extensible AI agent framework by Block (Square)",
            "category": "AI Coding Agents",
            "tags": ["coding", "agent", "framework", "extensible"],
            "url": "https://github.com/block/goose",
            "stars": 15000,
            "forks": 1800,
            "openSource": True,
            "alternativeTo": ["Claude Code"],
            "featured": False
        },
        {
            "name": "Qwen2.5-Coder",
            "description": "Alibaba's code generation model based on images and videos",
            "category": "AI Coding Agents",
            "tags": ["coding", "multimodal", "Alibaba", "open source"],
            "url": "https://github.com/QwenLM/Qwen2.5-Coder",
            "stars": 12000,
            "forks": 1500,
            "openSource": True,
            "alternativeTo": ["GitHub Copilot"],
            "featured": False
        },
        {
            "name": "Gemini CLI",
            "description": "Google's open-source terminal coding agent",
            "category": "AI Coding Agents",
            "tags": ["coding", "Google", "terminal", "CLI"],
            "url": "https://github.com/google-gemini/gemini-cli",
            "stars": 8500,
            "forks": 900,
            "openSource": True,
            "alternativeTo": ["Claude Code"],
            "featured": False
        },
        # === AI AGENT FRAMEWORKS ===
        {
            "name": "LangChain",
            "description": "Framework for building LLM-powered applications with chains and agents",
            "category": "AI Agent Frameworks",
            "tags": ["framework", "LLM", "chains", "agents", "RAG"],
            "url": "https://github.com/langchain-ai/langchain",
            "stars": 105000,
            "forks": 18500,
            "openSource": True,
            "alternativeTo": ["Voiceflow"],
            "featured": True
        },
        {
            "name": "LangGraph",
            "description": "Stateful, orchestrated agent workflows with graph-based execution",
            "category": "AI Agent Frameworks",
            "tags": ["framework", "agents", "stateful", "graph"],
            "url": "https://github.com/langchain-ai/langgraph",
            "stars": 12000,
            "forks": 1500,
            "openSource": True,
            "alternativeTo": ["n8n", "Make"],
            "featured": True
        },
        {
            "name": "CrewAI",
            "description": "Multi-agent orchestration framework for collaborative AI teams",
            "category": "AI Agent Frameworks",
            "tags": ["multi-agent", "orchestration", "teams"],
            "url": "https://github.com/crewAIInc/crewAI",
            "stars": 28000,
            "forks": 3500,
            "openSource": True,
            "alternativeTo": ["n8n"],
            "featured": True
        },
        {
            "name": "AutoGen (Microsoft)",
            "description": "Multi-agent conversation framework from Microsoft Research",
            "category": "AI Agent Frameworks",
            "tags": ["multi-agent", "conversation", "Microsoft"],
            "url": "https://github.com/microsoft/autogen",
            "stars": 38000,
            "forks": 5200,
            "openSource": True,
            "alternativeTo": ["Voiceflow"],
            "featured": True
        },
        {
            "name": "MetaGPT",
            "description": "Multi-agent framework that simulates a software company",
            "category": "AI Agent Frameworks",
            "tags": ["multi-agent", "software", "simulation"],
            "url": "https://github.com/FoundationAgents/MetaGPT",
            "stars": 45000,
            "forks": 5800,
            "openSource": True,
            "alternativeTo": ["Jira", "Linear"],
            "featured": False
        },
        {
            "name": "Dify",
            "description": "Build and deploy autonomous AI agents without coding",
            "category": "AI Agent Frameworks",
            "tags": ["no-code", "agents", "RAG", "workflows"],
            "url": "https://github.com/langgenius/dify",
            "stars": 142298,
            "forks": 22382,
            "openSource": True,
            "alternativeTo": ["Retool", "Voiceflow"],
            "featured": True
        },
        {
            "name": "Flowise AI",
            "description": "Visual builder for AI agents and LLM workflows with drag-and-drop",
            "category": "AI Agent Frameworks",
            "tags": ["no-code", "visual", "agents", "RAG"],
            "url": "https://github.com/FlowiseAI/Flowise",
            "stars": 53011,
            "forks": 24378,
            "openSource": True,
            "alternativeTo": ["n8n", "Voiceflow"],
            "featured": True
        },
        {
            "name": "Langflow",
            "description": "Visual builder for AI-powered applications and workflows",
            "category": "AI Agent Frameworks",
            "tags": ["low-code", "visual", "RAG", "agents"],
            "url": "https://github.com/langflow-ai/langflow",
            "stars": 148678,
            "forks": 9096,
            "openSource": True,
            "alternativeTo": ["Voiceflow"],
            "featured": True
        },
        {
            "name": "Smolagents (Hugging Face)",
            "description": "Minimalist agent framework from Hugging Face",
            "category": "AI Agent Frameworks",
            "tags": ["agents", "minimal", "HuggingFace"],
            "url": "https://github.com/huggingface/smolagents",
            "stars": 15000,
            "forks": 1800,
            "openSource": True,
            "alternativeTo": ["LangChain"],
            "featured": False
        },
        {
            "name": "Pydantic AI",
            "description": "Type-safe AI agent framework built on Pydantic",
            "category": "AI Agent Frameworks",
            "tags": ["agents", "type-safe", "Python", "Pydantic"],
            "url": "https://github.com/pydantic/pydantic-ai",
            "stars": 8000,
            "forks": 900,
            "openSource": True,
            "alternativeTo": ["LangChain"],
            "featured": False
        },
        {
            "name": "Letta",
            "description": "Stateful agents with advanced memory capabilities",
            "category": "AI Agent Frameworks",
            "tags": ["agents", "memory", "stateful"],
            "url": "https://github.com/letta-ai/letta",
            "stars": 12000,
            "forks": 1400,
            "openSource": True,
            "alternativeTo": ["LangChain"],
            "featured": False
        },
        {
            "name": "Haystack (deepset)",
            "description": "Framework for building production RAG pipelines and agents",
            "category": "AI Agent Frameworks",
            "tags": ["RAG", "pipelines", "production", "search"],
            "url": "https://github.com/deepset-ai/haystack",
            "stars": 18000,
            "forks": 2200,
            "openSource": True,
            "alternativeTo": ["LangChain"],
            "featured": False
        },
        # === VECTOR DATABASES & RAG ===
        {
            "name": "ChromaDB",
            "description": "Open-source vector database for AI applications",
            "category": "Vector Databases & RAG",
            "tags": ["vector", "database", "embeddings", "RAG"],
            "url": "https://github.com/chroma-core/chroma",
            "stars": 18000,
            "forks": 2000,
            "openSource": True,
            "alternativeTo": ["Pinecone", "Weaviate"],
            "featured": True
        },
        {
            "name": "Qdrant",
            "description": "High-performance vector similarity search engine",
            "category": "Vector Databases & RAG",
            "tags": ["vector", "search", "similarity", "production"],
            "url": "https://github.com/qdrant/qdrant",
            "stars": 22000,
            "forks": 2500,
            "openSource": True,
            "alternativeTo": ["Pinecone"],
            "featured": True
        },
        {
            "name": "Weaviate",
            "description": "AI-native vector database with built-in modules",
            "category": "Vector Databases & RAG",
            "tags": ["vector", "database", "AI-native", "modules"],
            "url": "https://github.com/weaviate/weaviate",
            "stars": 12000,
            "forks": 1400,
            "openSource": True,
            "alternativeTo": ["Pinecone"],
            "featured": True
        },
        {
            "name": "Milvus",
            "description": "Cloud-native vector database for billion-scale similarity search",
            "category": "Vector Databases & RAG",
            "tags": ["vector", "database", "scalable", "cloud-native"],
            "url": "https://github.com/milvus-io/milvus",
            "stars": 32000,
            "forks": 4500,
            "openSource": True,
            "alternativeTo": ["Pinecone"],
            "featured": False
        },
        {
            "name": "RAGflow",
            "description": "Open-source RAG engine with deep document understanding",
            "category": "Vector Databases & RAG",
            "tags": ["RAG", "document", "retrieval", "understanding"],
            "url": "https://github.com/infiniflow/ragflow",
            "stars": 8000,
            "forks": 900,
            "openSource": True,
            "alternativeTo": ["LangChain"],
            "featured": False
        },
        {
            "name": "LlamaIndex",
            "description": "Data framework for building LLM applications with custom data",
            "category": "Vector Databases & RAG",
            "tags": ["RAG", "data", "LLM", "indexing"],
            "url": "https://github.com/run-llama/llama_index",
            "stars": 38000,
            "forks": 4800,
            "openSource": True,
            "alternativeTo": ["LangChain"],
            "featured": True
        },
        # === AI VIDEO & IMAGE ===
        {
            "name": "Kling AI 3.0",
            "description": "Advanced AI video and image generation platform",
            "category": "AI Video & Image",
            "tags": ["video", "image", "generation", "AI"],
            "url": "https://klingai.com",
            "stars": 0,
            "forks": 0,
            "openSource": False,
            "alternativeTo": ["Runway", "Pika"],
            "featured": True
        },
        {
            "name": "Pika Agents",
            "description": "Conversational AI agent for video creation and editing",
            "category": "AI Video & Image",
            "tags": ["video", "conversation", "agents", "creation"],
            "url": "https://pika.art",
            "stars": 0,
            "forks": 0,
            "openSource": False,
            "alternativeTo": ["Runway"],
            "featured": False
        },
        {
            "name": "Heygen",
            "description": "AI avatar video production with voice cloning and editing",
            "category": "AI Video & Image",
            "tags": ["video", "avatar", "voice", "production"],
            "url": "https://heygen.com",
            "stars": 0,
            "forks": 0,
            "openSource": False,
            "alternativeTo": ["Synthesia"],
            "featured": True
        },
        {
            "name": "Runway",
            "description": "AI video generation, editing, and visual effects platform",
            "category": "AI Video & Image",
            "tags": ["video", "editing", "generation", "VFX"],
            "url": "https://runwayml.com",
            "stars": 0,
            "forks": 0,
            "openSource": False,
            "alternativeTo": ["Adobe After Effects"],
            "featured": True
        },
        {
            "name": "CapCut AI",
            "description": "AI-powered video, image, and voiceover creation tool",
            "category": "AI Video & Image",
            "tags": ["video", "editing", "voiceover", "ByteDance"],
            "url": "https://capcut.com",
            "stars": 0,
            "forks": 0,
            "openSource": False,
            "alternativeTo": ["Adobe Premiere"],
            "featured": False
        },
        {
            "name": "PixVerse",
            "description": "AI platform for creating videos from text and images",
            "category": "AI Video & Image",
            "tags": ["video", "generation", "text-to-video"],
            "url": "https://pixverse.ai",
            "stars": 0,
            "forks": 0,
            "openSource": False,
            "alternativeTo": ["Runway"],
            "featured": False
        },
        {
            "name": "Luma AI",
            "description": "AI campaign generation with video, image, and text workflows",
            "category": "AI Video & Image",
            "tags": ["video", "3D", "campaign", "workflows"],
            "url": "https://lumalabs.ai",
            "stars": 0,
            "forks": 0,
            "openSource": False,
            "alternativeTo": ["Blender"],
            "featured": False
        },
        {
            "name": "Project Genie (Google)",
            "description": "Google's AI for generating images and videos from prompts",
            "category": "AI Video & Image",
            "tags": ["video", "image", "Google", "generation"],
            "url": "https://deepmind.google",
            "stars": 0,
            "forks": 0,
            "openSource": False,
            "alternativeTo": ["Midjourney", "DALL-E"],
            "featured": False
        },
        # === AI VOICE & AUDIO ===
        {
            "name": "ElevenLabs",
            "description": "AI voice synthesis and voice agent platform",
            "category": "AI Voice & Audio",
            "tags": ["voice", "synthesis", "agents", "TTS"],
            "url": "https://elevenlabs.io",
            "stars": 0,
            "forks": 0,
            "openSource": False,
            "alternativeTo": ["Amazon Polly", "Google Cloud TTS"],
            "featured": True
        },
        {
            "name": "Hume AI",
            "description": "Voice generation and emotional intelligence AI",
            "category": "AI Voice & Audio",
            "tags": ["voice", "emotion", "generation", "AI"],
            "url": "https://hume.ai",
            "stars": 0,
            "forks": 0,
            "openSource": False,
            "alternativeTo": ["ElevenLabs"],
            "featured": False
        },
        {
            "name": "Gemini 3.1 Flash Live",
            "description": "Google's real-time voice and live video AI interaction",
            "category": "AI Voice & Audio",
            "tags": ["voice", "live", "video", "Google", "real-time"],
            "url": "https://deepmind.google",
            "stars": 0,
            "forks": 0,
            "openSource": False,
            "alternativeTo": ["ElevenLabs"],
            "featured": False
        },
        # === LLMS & FOUNDATION MODELS ===
        {
            "name": "Ollama",
            "description": "Run local LLMs with a simple CLI and API",
            "category": "LLMs & Foundation Models",
            "tags": ["LLM", "local", "CLI", "open source"],
            "url": "https://github.com/ollama/ollama",
            "stars": 120000,
            "forks": 12000,
            "openSource": True,
            "alternativeTo": ["OpenAI API", "Claude API"],
            "featured": True
        },
        {
            "name": "llama.cpp",
            "description": "Inference of LLaMA models in pure C/C++ with GPU support",
            "category": "LLMs & Foundation Models",
            "tags": ["inference", "C++", "LLaMA", "GPU"],
            "url": "https://github.com/ggml-ai/llama.cpp",
            "stars": 75000,
            "forks": 9500,
            "openSource": True,
            "alternativeTo": ["OpenAI API"],
            "featured": True
        },
        {
            "name": "vLLM",
            "description": "High-throughput LLM serving engine with PagedAttention",
            "category": "LLMs & Foundation Models",
            "tags": ["inference", "serving", "high-throughput", "GPU"],
            "url": "https://github.com/vllm-project/vllm",
            "stars": 45000,
            "forks": 5500,
            "openSource": True,
            "alternativeTo": ["OpenAI API"],
            "featured": True
        },
        {
            "name": "LocalAI",
            "description": "Self-hosted OpenAI API-compatible inference server",
            "category": "LLMs & Foundation Models",
            "tags": ["self-hosted", "API", "inference", "local"],
            "url": "https://github.com/mudler/LocalAI",
            "stars": 28000,
            "forks": 3200,
            "openSource": True,
            "alternativeTo": ["OpenAI API"],
            "featured": False
        },
        {
            "name": "Hugging Face Transformers",
            "description": "State-of-the-art ML models with unified API across frameworks",
            "category": "LLMs & Foundation Models",
            "tags": ["transformers", "models", "NLP", "hub"],
            "url": "https://github.com/huggingface/transformers",
            "stars": 140000,
            "forks": 28000,
            "openSource": True,
            "alternativeTo": ["OpenAI API"],
            "featured": True
        },
        {
            "name": "DeepSeek V3",
            "description": "High-performance open-source LLM with 671B parameters",
            "category": "LLMs & Foundation Models",
            "tags": ["LLM", "open source", "performance", "MoE"],
            "url": "https://github.com/deepseek-ai/DeepSeek-V3",
            "stars": 90000,
            "forks": 10000,
            "openSource": True,
            "alternativeTo": ["GPT-4", "Claude"],
            "featured": True
        },
        {
            "name": "Meta Llama",
            "description": "Meta's family of open-source large language models",
            "category": "LLMs & Foundation Models",
            "tags": ["LLM", "open source", "Meta", "foundation"],
            "url": "https://github.com/meta-llama/llama-models",
            "stars": 60000,
            "forks": 7500,
            "openSource": True,
            "alternativeTo": ["GPT-4", "Claude"],
            "featured": True
        },
        {
            "name": "Mistral AI",
            "description": "Efficient open-source LLMs with top performance-to-size ratio",
            "category": "LLMs & Foundation Models",
            "tags": ["LLM", "open source", "efficient", "French"],
            "url": "https://github.com/mistralai/mistral-inference",
            "stars": 12000,
            "forks": 1400,
            "openSource": True,
            "alternativeTo": ["GPT-4", "Claude"],
            "featured": True
        },
        {
            "name": "Gemma 4 (Google)",
            "description": "Google's open-source lightweight model for tech coding",
            "category": "LLMs & Foundation Models",
            "tags": ["LLM", "Google", "open source", "coding"],
            "url": "https://ai.google.dev/gemma",
            "stars": 5000,
            "forks": 600,
            "openSource": True,
            "alternativeTo": ["GPT-4", "Claude"],
            "featured": False
        },
        # === AI PLATFORMS & INFRASTRUCTURE ===
        {
            "name": "Open WebUI",
            "description": "Self-hosted AI interface for any model, any team",
            "category": "AI Platforms & Infrastructure",
            "tags": ["UI", "self-hosted", "multi-model", "team"],
            "url": "https://github.com/open-webui/open-webui",
            "stars": 138289,
            "forks": 19774,
            "openSource": True,
            "alternativeTo": ["Claude", "ChatGPT"],
            "featured": True
        },
        {
            "name": "OpenClaw",
            "description": "Personal AI assistant that arranges meetings, checks in for flights, and more through chat apps",
            "category": "AI Platforms & Infrastructure",
            "tags": ["assistant", "chat", "automation", "personal"],
            "url": "https://github.com/openclaw/openclaw",
            "stars": 374038,
            "forks": 77740,
            "openSource": True,
            "alternativeTo": ["Zo Computer", "Siri"],
            "featured": True
        },
        {
            "name": "n8n",
            "description": "Visual workflow automation with code flexibility and AI agents",
            "category": "Automation & Workflows",
            "tags": ["workflow", "automation", "AI agents", "no-code"],
            "url": "https://github.com/n8n-io/n8n",
            "stars": 189341,
            "forks": 57921,
            "openSource": True,
            "alternativeTo": ["Make", "Zapier"],
            "featured": True
        },
        {
            "name": "Supabase",
            "description": "Open-source Firebase alternative with real-time databases and auth",
            "category": "AI Platforms & Infrastructure",
            "tags": ["backend", "database", "auth", "real-time"],
            "url": "https://github.com/supabase/supabase",
            "stars": 102889,
            "forks": 12516,
            "openSource": True,
            "alternativeTo": ["Firebase"],
            "featured": True
        },
        {
            "name": "Firecrawl",
            "description": "Blazing-fast web crawling for modern developers built on Rust",
            "category": "AI Platforms & Infrastructure",
            "tags": ["crawling", "web", "scraping", "Rust"],
            "url": "https://github.com/firecrawl/firecrawl",
            "stars": 123144,
            "forks": 7468,
            "openSource": True,
            "alternativeTo": ["Browserbase"],
            "featured": True
        },
        {
            "name": "Browser Use",
            "description": "AI-powered browser automation for seamless web interactions",
            "category": "AI Platforms & Infrastructure",
            "tags": ["browser", "automation", "AI", "agents"],
            "url": "https://github.com/browser-use/browser-use",
            "stars": 95160,
            "forks": 10717,
            "openSource": True,
            "alternativeTo": ["Browserbase", "Selenium"],
            "featured": True
        },
        {
            "name": "Crawl4AI",
            "description": "Open-source web crawler optimized for AI and LLMs",
            "category": "AI Platforms & Infrastructure",
            "tags": ["crawling", "AI", "RAG", "markdown"],
            "url": "https://github.com/crawl4ai/crawl4ai",
            "stars": 66099,
            "forks": 6752,
            "openSource": True,
            "alternativeTo": ["Browserbase"],
            "featured": False
        },
        {
            "name": "Daytona",
            "description": "Lightning-fast AI code execution in secure sandboxes",
            "category": "AI Platforms & Infrastructure",
            "tags": ["sandbox", "execution", "secure", "AI"],
            "url": "https://github.com/daytonaio/daytona",
            "stars": 72471,
            "forks": 5582,
            "openSource": True,
            "alternativeTo": ["Modal"],
            "featured": False
        },
        # === ANALYTICS & MONITORING ===
        {
            "name": "OpenPanel",
            "description": "Cookie-free web and product analytics, self-hostable",
            "category": "Analytics & Monitoring",
            "tags": ["analytics", "privacy", "self-hosted", "GDPR"],
            "url": "https://github.com/OpenPanel/OpenPanel",
            "stars": 5797,
            "forks": 366,
            "openSource": True,
            "alternativeTo": ["Google Analytics"],
            "featured": True
        },
        {
            "name": "PostHog",
            "description": "All-in-one product analytics platform with session recording",
            "category": "Analytics & Monitoring",
            "tags": ["analytics", "product", "session recording", "feature flags"],
            "url": "https://github.com/PostHog/posthog",
            "stars": 25000,
            "forks": 3200,
            "openSource": True,
            "alternativeTo": ["Mixpanel", "Amplitude"],
            "featured": True
        },
        {
            "name": "Uptime Kuma",
            "description": "Self-hosted monitoring tool for websites and services",
            "category": "Analytics & Monitoring",
            "tags": ["monitoring", "uptime", "self-hosted", "alerts"],
            "url": "https://github.com/uptime-kuma/uptime-kuma",
            "stars": 87109,
            "forks": 7882,
            "openSource": True,
            "alternativeTo": ["Opsgenie", "Pingdom"],
            "featured": True
        },
        # === AI BUSINESS & MARKETING ===
        {
            "name": "Dub Partners",
            "description": "Affiliate marketing platform built for SaaS companies",
            "category": "AI Business & Marketing",
            "tags": ["affiliate", "marketing", "SaaS", "partners"],
            "url": "https://github.com/dubinc/dub",
            "stars": 23585,
            "forks": 3008,
            "openSource": True,
            "alternativeTo": ["PartnerStack", "Post Affiliate Pro"],
            "featured": True
        },
        {
            "name": "Postiz",
            "description": "Schedule and manage social media across 30+ networks",
            "category": "AI Business & Marketing",
            "tags": ["social media", "scheduling", "AI", "analytics"],
            "url": "https://github.com/postiz/postiz",
            "stars": 30609,
            "forks": 5616,
            "openSource": True,
            "alternativeTo": ["HootSuite", "Buffer"],
            "featured": True
        },
        {
            "name": "Novu",
            "description": "Multi-channel notification infrastructure for apps",
            "category": "AI Business & Marketing",
            "tags": ["notifications", "multi-channel", "infrastructure"],
            "url": "https://github.com/novuhq/novu",
            "stars": 39009,
            "forks": 4294,
            "openSource": True,
            "alternativeTo": ["Customer.io", "SendGrid"],
            "featured": True
        },
        # === AI SECURITY & COMPLIANCE ===
        {
            "name": "Openlane",
            "description": "Automate SOC 2, ISO 27001, and NIST compliance programs",
            "category": "AI Security & Compliance",
            "tags": ["compliance", "SOC 2", "ISO 27001", "security"],
            "url": "https://github.com/openlane/openlane",
            "stars": 245,
            "forks": 44,
            "openSource": True,
            "alternativeTo": ["Vanta", "Drata"],
            "featured": False
        },
        {
            "name": "Probo",
            "description": "Managed compliance for SOC 2, ISO 27001, HIPAA, and more",
            "category": "AI Security & Compliance",
            "tags": ["compliance", "security", "managed", "audit"],
            "url": "https://github.com/probo/probo",
            "stars": 1088,
            "forks": 163,
            "openSource": True,
            "alternativeTo": ["Vanta"],
            "featured": False
        },
        # === MLOPS & PRODUCTION ===
        {
            "name": "MLflow",
            "description": "Open-source platform for the complete ML lifecycle",
            "category": "MLOps & Production",
            "tags": ["MLOps", "experiment tracking", "models", "pipeline"],
            "url": "https://github.com/mlflow/mlflow",
            "stars": 20000,
            "forks": 4500,
            "openSource": True,
            "alternativeTo": ["Weights & Biases"],
            "featured": True
        },
        {
            "name": "Ray",
            "description": "Unified compute framework for AI and Python applications",
            "category": "MLOps & Production",
            "tags": ["compute", "distributed", "AI", "scaling"],
            "url": "https://github.com/ray-project/ray",
            "stars": 35000,
            "forks": 6000,
            "openSource": True,
            "alternativeTo": ["Dask"],
            "featured": False
        },
        {
            "name": "BentoML",
            "description": "Unified model serving framework for production AI",
            "category": "MLOps & Production",
            "tags": ["serving", "models", "deployment", "production"],
            "url": "https://github.com/bentoml/BentoML",
            "stars": 8000,
            "forks": 1000,
            "openSource": True,
            "alternativeTo": ["AWS SageMaker"],
            "featured": False
        },
        {
            "name": "Kubeflow",
            "description": "ML workflows on Kubernetes with portable, scalable pipelines",
            "category": "MLOps & Production",
            "tags": ["Kubernetes", "MLOps", "pipelines", "orchestration"],
            "url": "https://github.com/kubeflow/kubeflow",
            "stars": 14500,
            "forks": 2800,
            "openSource": True,
            "alternativeTo": ["Vertex AI"],
            "featured": False
        },
        # === MCP (MODEL CONTEXT PROTOCOL) ===
        {
            "name": "MCP Specification",
            "description": "Open protocol connecting AI models to external tools and data sources",
            "category": "AI Agent Frameworks",
            "tags": ["protocol", "tools", "integration", "Anthropic"],
            "url": "https://github.com/modelcontextprotocol/modelcontextprotocol",
            "stars": 50000,
            "forks": 5500,
            "openSource": True,
            "alternativeTo": ["OpenAI Plugins"],
            "featured": True
        },
        {
            "name": "GitHub MCP Server",
            "description": "GitHub integration for AI agents via MCP protocol",
            "category": "AI Agent Frameworks",
            "tags": ["GitHub", "MCP", "integration", "developer tools"],
            "url": "https://github.com/github/github-mcp-server",
            "stars": 12000,
            "forks": 1400,
            "openSource": True,
            "alternativeTo": ["GitHub Actions"],
            "featured": False
        },
        # === ADDITIONAL NOTABLE TOOLS ===
        {
            "name": "Cap",
            "description": "Open source screen recorder with editing and instant sharing",
            "category": "AI Platforms & Infrastructure",
            "tags": ["screen recording", "sharing", "Rust", "Tauri"],
            "url": "https://github.com/cap-js/cap",
            "stars": 19128,
            "forks": 1557,
            "openSource": True,
            "alternativeTo": ["Loom"],
            "featured": False
        },
        {
            "name": "Parlant",
            "description": "Structured control layer for customer-facing AI agents",
            "category": "AI Agent Frameworks",
            "tags": ["agents", "customer-facing", "guidelines", "control"],
            "url": "https://github.com/parlant/parlant",
            "stars": 18086,
            "forks": 1536,
            "openSource": True,
            "alternativeTo": ["Voiceflow"],
            "featured": False
        },
        {
            "name": "Hanko",
            "description": "Passkeys, SSO, and 2FA without vendor lock-in",
            "category": "AI Security & Compliance",
            "tags": ["auth", "passkeys", "SSO", "MFA", "open source"],
            "url": "https://github.com/hanko-io/hanko",
            "stars": 8930,
            "forks": 1012,
            "openSource": True,
            "alternativeTo": ["Clerk", "Auth0"],
            "featured": False
        },
        {
            "name": "Baserow",
            "description": "No-code database and app builder you can self-host",
            "category": "AI Platforms & Infrastructure",
            "tags": ["no-code", "database", "app builder", "self-hosted"],
            "url": "https://github.com/baserow/baserow",
            "stars": 4880,
            "forks": 607,
            "openSource": True,
            "alternativeTo": ["Airtable"],
            "featured": False
        },
        {
            "name": "Tolgee",
            "description": "Open-source localization platform for multilingual apps",
            "category": "AI Business & Marketing",
            "tags": ["localization", "translation", "i18n", "AI"],
            "url": "https://github.com/tolgee/tolgee",
            "stars": 3932,
            "forks": 357,
            "openSource": True,
            "alternativeTo": ["Crowdin"],
            "featured": False
        },
        {
            "name": "Excalidraw",
            "description": "Collaborative whiteboarding with a hand-drawn feel",
            "category": "AI Platforms & Infrastructure",
            "tags": ["whiteboarding", "collaboration", "diagrams"],
            "url": "https://github.com/excalidraw/excalidraw",
            "stars": 123874,
            "forks": 13742,
            "openSource": True,
            "alternativeTo": ["Miro", "Figma"],
            "featured": False
        },
        {
            "name": "Zed",
            "description": "High-performance code editor built in Rust with AI collaboration",
            "category": "AI Coding Agents",
            "tags": ["editor", "Rust", "collaboration", "AI"],
            "url": "https://github.com/zed-industries/zed",
            "stars": 83591,
            "forks": 8659,
            "openSource": True,
            "alternativeTo": ["VS Code", "Cursor"],
            "featured": False
        },
        {
            "name": "Mermaid",
            "description": "Create diagrams and flowcharts with simple markdown syntax",
            "category": "AI Platforms & Infrastructure",
            "tags": ["diagrams", "markdown", "documentation", "visualization"],
            "url": "https://github.com/mermaid-js/mermaid",
            "stars": 88236,
            "forks": 9003,
            "openSource": True,
            "alternativeTo": ["Microsoft Visio", "Lucidchart"],
            "featured": False
        },
        {
            "name": "Elasticsearch",
            "description": "The leading distributed search and analytics engine",
            "category": "Analytics & Monitoring",
            "tags": ["search", "analytics", "distributed", "logs"],
            "url": "https://github.com/elastic/elasticsearch",
            "stars": 76746,
            "forks": 25917,
            "openSource": True,
            "alternativeTo": ["Algolia", "Splunk"],
            "featured": False
        },
        {
            "name": "Hoppscotch",
            "description": "Lightweight, open-source API development and testing platform",
            "category": "AI Platforms & Infrastructure",
            "tags": ["API", "testing", "development", "HTTP"],
            "url": "https://github.com/hoppscotch/hoppscotch",
            "stars": 79272,
            "forks": 5888,
            "openSource": True,
            "alternativeTo": ["Postman"],
            "featured": False
        },
        {
            "name": "Apache Superset",
            "description": "Modern data exploration and visualization platform",
            "category": "Analytics & Monitoring",
            "tags": ["analytics", "visualization", "BI", "dashboards"],
            "url": "https://github.com/apache/superset",
            "stars": 72957,
            "forks": 17359,
            "openSource": True,
            "alternativeTo": ["Power BI", "Tableau"],
            "featured": False
        },
        {
            "name": "Home Assistant",
            "description": "Local control smart home automation with privacy first",
            "category": "AI Platforms & Infrastructure",
            "tags": ["smart home", "automation", "IoT", "local"],
            "url": "https://github.com/home-assistant/core",
            "stars": 87190,
            "forks": 37542,
            "openSource": True,
            "alternativeTo": ["Google Assistant", "Apple Home"],
            "featured": False
        },
        {
            "name": "LobeChat",
            "description": "Manage, build, and run AI agent teams around the clock",
            "category": "AI Agent Frameworks",
            "tags": ["agents", "teams", "automation", "scheduling"],
            "url": "https://github.com/lobehub/lobe-chat",
            "stars": 77561,
            "forks": 15264,
            "openSource": True,
            "alternativeTo": ["Claude", "ChatGPT"],
            "featured": False
        },
        {
            "name": "Immich",
            "description": "Self-hosted photo and video backup solution with AI features",
            "category": "AI Platforms & Infrastructure",
            "tags": ["photos", "backup", "self-hosted", "privacy"],
            "url": "https://github.com/immich-app/immich",
            "stars": 101349,
            "forks": 5666,
            "openSource": True,
            "alternativeTo": ["Google Photos"],
            "featured": False
        },
        {
            "name": "RustDesk",
            "description": "Secure, fast, and open-source remote desktop software",
            "category": "AI Platforms & Infrastructure",
            "tags": ["remote desktop", "Rust", "secure", "cross-platform"],
            "url": "https://github.com/rustdesk/rustdesk",
            "stars": 114779,
            "forks": 17303,
            "openSource": True,
            "alternativeTo": ["AnyDesk", "TeamViewer"],
            "featured": False
        },
        {
            "name": "Godot",
            "description": "Free, open-source game engine for 2D/3D development",
            "category": "AI Platforms & Infrastructure",
            "tags": ["game engine", "2D", "3D", "open source"],
            "url": "https://github.com/godotengine/godot",
            "stars": 111054,
            "forks": 25417,
            "openSource": True,
            "alternativeTo": ["Unreal Engine", "Unity"],
            "featured": False
        },
        {
            "name": "Ladybird",
            "description": "Independent browser engine built from scratch, not a fork",
            "category": "AI Platforms & Infrastructure",
            "tags": ["browser", "engine", "open source", "non-profit"],
            "url": "https://github.com/LadybirdWebBrowser/ladybird",
            "stars": 63522,
            "forks": 3049,
            "openSource": True,
            "alternativeTo": ["Firefox", "Chrome"],
            "featured": False
        },
        {
            "name": "LocalSend",
            "description": "Share files securely across all devices without servers",
            "category": "AI Platforms & Infrastructure",
            "tags": ["file sharing", "cross-platform", "encryption", "local"],
            "url": "https://github.com/localsend/localsend",
            "stars": 81808,
            "forks": 4415,
            "openSource": True,
            "alternativeTo": ["Apple AirDrop", "Shareit"],
            "featured": False
        },
        {
            "name": "AgentOS",
            "description": "TypeScript framework for building autonomous AI agents",
            "category": "AI Agent Frameworks",
            "tags": ["TypeScript", "agents", "cognitive memory", "orchestration"],
            "url": "https://github.com/agentos-dev/agentos",
            "stars": 488,
            "forks": 69,
            "openSource": True,
            "alternativeTo": ["LangChain"],
            "featured": False
        },
        {
            "name": "LearnHouse",
            "description": "Build, share & monetize courses with modern open-source LMS",
            "category": "AI Business & Marketing",
            "tags": ["LMS", "courses", "education", "monetization"],
            "url": "https://github.com/learnhouse/learnhouse",
            "stars": 1643,
            "forks": 327,
            "openSource": True,
            "alternativeTo": ["Miro", "Teachable"],
            "featured": False
        },
        {
            "name": "Open Mercato",
            "description": "CRM/ERP foundation framework with 80% already built",
            "category": "AI Business & Marketing",
            "tags": ["CRM", "ERP", "multi-tenancy", "RBAC"],
            "url": "https://github.com/openmercato/openmercato",
            "stars": 1329,
            "forks": 266,
            "openSource": True,
            "alternativeTo": ["SAP", "Salesforce"],
            "featured": False
        }
    ]
}
