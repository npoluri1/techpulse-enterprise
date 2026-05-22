import os
import json
import logging
from typing import List, Dict, Optional

from enterprise_engine.config import config

logger = logging.getLogger("EnterpriseVectorStore")

try:
    import chromadb
    from chromadb.config import Settings
    HAS_CHROMA = True
except ImportError:
    HAS_CHROMA = False
    chromadb = None
    logger.warning("ChromaDB not installed. Vector search disabled.")

try:
    from sentence_transformers import SentenceTransformer
    HAS_SENTENCE_TRANSFORMERS = True
except ImportError:
    HAS_SENTENCE_TRANSFORMERS = False
    SentenceTransformer = None
    logger.warning("sentence-transformers not installed. Using fallback embeddings.")

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False
    np = None


class FreeVectorStore:
    def __init__(self):
        self.collection = None
        self.embedder = None
        self._init_chroma()
        self._init_embedder()

    def _init_chroma(self):
        if not HAS_CHROMA:
            logger.warning("ChromaDB not available")
            return
        try:
            os.makedirs(config.CHROMA_PERSIST_DIR, exist_ok=True)
            self.client = chromadb.PersistentClient(
                path=config.CHROMA_PERSIST_DIR,
                settings=Settings(anonymized_telemetry=False),
            )
            self.collection = self.client.get_or_create_collection(
                name="tech_intel",
                metadata={"hnsw:space": "cosine"},
            )
            logger.info(f"[VectorDB] ChromaDB initialized at {config.CHROMA_PERSIST_DIR}")
        except Exception as e:
            logger.error(f"[VectorDB] ChromaDB init failed: {e}")
            self.collection = None

    def _init_embedder(self):
        if HAS_SENTENCE_TRANSFORMERS:
            try:
                self.embedder = SentenceTransformer(config.EMBEDDING_MODEL)
                logger.info(f"[Embed] Loaded {config.EMBEDDING_MODEL}")
            except Exception as e:
                logger.error(f"[Embed] Failed to load model: {e}")
                self.embedder = None
        else:
            logger.warning("[Embed] No sentence-transformers, using simple hash embeddings")

    def _simple_embed(self, text: str) -> list:
        import hashlib
        text_bytes = text.encode("utf-8")
        hash_obj = hashlib.md5(text_bytes)
        seed = int(hash_obj.hexdigest()[:8], 16)
        if HAS_NUMPY:
            rng = np.random.RandomState(seed)
            return rng.randn(384).tolist()
        import random
        rng = random.Random(seed)
        return [rng.gauss(0, 1) for _ in range(384)]

    def _get_embedding(self, text: str) -> list:
        if self.embedder is not None:
            try:
                return self.embedder.encode(text[:2048]).tolist()
            except Exception as e:
                logger.warning(f"[Embed] encode failed: {e}")
        return self._simple_embed(text)

    def index_article(self, article: dict):
        if self.collection is None:
            return
        try:
            doc_id = article.get("id", article.get("url", ""))
            text = f"{article.get('title', '')}\n\n{article.get('summary', '')}"
            embedding = self._get_embedding(text)

            metadata = {
                "title": article.get("title", "")[:200],
                "url": article.get("url", ""),
                "source": article.get("source", ""),
                "category": article.get("category", "General"),
                "published": str(article.get("published", "")),
                "industry_tags": json.dumps(article.get("industry_tags", [])),
                "sector_tags": json.dumps(article.get("sector_tags", [])),
                "region_tags": json.dumps(article.get("region_tags", [])),
                "final_score": str(article.get("final_score", 0)),
                "funding_amount": str(article.get("funding_amount_usd") or "0"),
            }

            self.collection.add(
                ids=[doc_id],
                embeddings=[embedding],
                metadatas=[metadata],
                documents=[text],
            )
        except Exception as e:
            logger.warning(f"[VectorDB] Index failed for {article.get('title', '')[:50]}: {e}")

    def search(self, query: str, k: int = 10,
               filter_dict: Optional[dict] = None) -> List[dict]:
        if self.collection is None:
            return []
        try:
            query_embedding = self._get_embedding(query)
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=k,
                where=filter_dict if filter_dict else None,
            )
            articles = []
            for i in range(len(results["ids"][0])):
                meta = results["metadatas"][0][i]
                articles.append({
                    "id": results["ids"][0][i],
                    "title": meta.get("title", ""),
                    "url": meta.get("url", ""),
                    "source": meta.get("source", ""),
                    "category": meta.get("category", ""),
                    "published": meta.get("published", ""),
                    "content": results["documents"][0][i][:300],
                    "industry_tags": json.loads(meta.get("industry_tags", "[]")),
                    "sector_tags": json.loads(meta.get("sector_tags", "[]")),
                    "region_tags": json.loads(meta.get("region_tags", "[]")),
                    "final_score": float(meta.get("final_score", 0)),
                    "funding_amount": float(meta.get("funding_amount", 0)),
                    "score": results["distances"][0][i] if results.get("distances") else 0,
                })
            return articles
        except Exception as e:
            logger.error(f"[VectorDB] Search failed: {e}")
            return []

    def search_by_industry(self, industry: str, k: int = 10) -> List[dict]:
        return self.search(
            f"Latest news and developments in {industry}",
            k=k,
            filter_dict={"industry_tags": {"$contains": industry}},
        )

    def get_stats(self) -> dict:
        if self.collection is None:
            return {"count": 0, "status": "disconnected"}
        try:
            return {"count": self.collection.count(), "status": "connected"}
        except:
            return {"count": 0, "status": "error"}
