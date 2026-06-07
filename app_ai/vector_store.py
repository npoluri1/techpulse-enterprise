import os
import logging
import shutil
from typing import List, Dict, Any, Optional
import numpy as np

logger = logging.getLogger("NewsAI.VectorStore")

CHROMA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "chroma_db")
os.makedirs(CHROMA_DIR, exist_ok=True)

class VectorStore:
    def __init__(self):
        self.embeddings_enabled = False
        self.collection = None
        self.embedder = None
        self._init_store()

    def _init_store(self):
        try:
            import chromadb
            from sentence_transformers import SentenceTransformer
            self.client = chromadb.PersistentClient(path=CHROMA_DIR)
            self.collection = self.client.get_or_create_collection(
                name="news_articles",
                metadata={"hnsw:space": "cosine"}
            )
            self.embedder = SentenceTransformer("all-MiniLM-L6-v2")
            self.embeddings_enabled = True
            logger.info("Vector store initialized with all-MiniLM-L6-v2")
        except Exception as e:
            logger.warning(f"Vector store init failed (non-critical): {e}")
            self.embeddings_enabled = False

    def get_embedding(self, text: str) -> List[float]:
        if not self.embeddings_enabled or not self.embedder:
            return []
        try:
            emb = self.embedder.encode(text[:512]).tolist()
            return emb
        except Exception as e:
            logger.error(f"Embedding failed: {e}")
            return []

    def add_article(self, article_id: str, title: str, summary: str, content: str = "", metadata: dict = None):
        if not self.embeddings_enabled or not self.collection:
            return False
        try:
            text = f"{title}. {summary[:300]}"
            embedding = self.get_embedding(text)
            if not embedding:
                return False
            meta = metadata or {}
            meta.update({"title": title[:200], "summary": summary[:300]})
            self.collection.add(
                ids=[article_id],
                embeddings=[embedding],
                metadatas=[meta]
            )
            return True
        except Exception as e:
            logger.error(f"Add article failed: {e}")
            return False

    def search(self, query: str, n_results: int = 10) -> List[Dict[str, Any]]:
        if not self.embeddings_enabled or not self.collection:
            return []
        try:
            query_emb = self.get_embedding(query)
            if not query_emb:
                return []
            results = self.collection.query(
                query_embeddings=[query_emb],
                n_results=n_results
            )
            output = []
            if results["ids"] and results["metadatas"]:
                for i, idx in enumerate(results["ids"][0]):
                    meta = results["metadatas"][0][i] if results["metadatas"][0] else {}
                    output.append({
                        "id": idx,
                        "title": meta.get("title", ""),
                        "summary": meta.get("summary", ""),
                        "category": meta.get("category", ""),
                        "url": meta.get("url", ""),
                        "source": meta.get("source", ""),
                        "score": float(results["distances"][0][i]) if results.get("distances") else 0.0
                    })
            return output
        except Exception as e:
            logger.error(f"Vector search failed: {e}")
            return []

    def delete_article(self, article_id: str):
        if not self.embeddings_enabled or not self.collection:
            return
        try:
            self.collection.delete(ids=[article_id])
        except Exception as e:
            logger.error(f"Delete failed: {e}")

    def count(self) -> int:
        if not self.embeddings_enabled or not self.collection:
            return 0
        try:
            return self.collection.count()
        except:
            return 0

vector_store = VectorStore()
