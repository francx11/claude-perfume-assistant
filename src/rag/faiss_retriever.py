"""FAISS-backed semantic retriever for perfume search."""

import hashlib
import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

import faiss

logger = logging.getLogger(__name__)

_CACHE_DIR = Path("data/embeddings")
_INDEX_FILE = _CACHE_DIR / "faiss.index"
_META_FILE = _CACHE_DIR / "faiss_meta.json"


def _csv_md5(csv_path: str) -> str:
    h = hashlib.md5()
    with open(csv_path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


class FAISSRetriever:
    """Retriever using FAISS IndexFlatIP for cosine similarity search."""

    def __init__(self, embeddings_generator, data_loader):
        self.embeddings_generator = embeddings_generator
        self.data_loader = data_loader
        self._index = None
        self._id_map: List[str] = []
        self._id_to_idx: Dict[str, int] = {}

    # ------------------------------------------------------------------
    # Cache helpers
    # ------------------------------------------------------------------

    def _load_cache(self, csv_path: Optional[str]) -> bool:
        """Load index from disk. Returns True if cache is valid and loaded."""
        if not _INDEX_FILE.exists() or not _META_FILE.exists():
            return False
        try:
            meta = json.loads(_META_FILE.read_text(encoding="utf-8"))
            if csv_path and meta.get("csv_md5") != _csv_md5(csv_path):
                logger.info("FAISS cache stale (CSV changed) — rebuilding")
                return False
            self._index = faiss.read_index(str(_INDEX_FILE))
            self._id_map = meta["id_map"]
            self._id_to_idx = {pid: i for i, pid in enumerate(self._id_map)}
            logger.info("FAISS index loaded from cache (%d vectors)", self._index.ntotal)
            return True
        except Exception:
            logger.warning("Failed to load FAISS cache — rebuilding", exc_info=True)
            return False

    def _save_cache(self, csv_path: Optional[str]) -> None:
        """Persist index and metadata to disk."""
        try:
            _CACHE_DIR.mkdir(parents=True, exist_ok=True)
            faiss.write_index(self._index, str(_INDEX_FILE))
            meta = {
                "id_map": self._id_map,
                "csv_md5": _csv_md5(csv_path) if csv_path else None,
            }
            _META_FILE.write_text(json.dumps(meta, ensure_ascii=False), encoding="utf-8")
            logger.info("FAISS index saved to cache")
        except Exception:
            logger.warning("Failed to save FAISS cache", exc_info=True)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def build_index(self, perfumes: List[Dict[str, Any]], csv_path: Optional[str] = None) -> None:
        """Build FAISS index. Loads from disk cache if valid, else recomputes."""
        if self._load_cache(csv_path):
            return

        logger.info("Building FAISS index for %d perfumes…", len(perfumes))
        texts = []
        for perfume in perfumes:
            text = f"{perfume.get('brand', '')} {perfume.get('name', '')}"
            notes = perfume.get("notes", "")
            if notes:
                text += f". Notes: {notes}"
            description = perfume.get("description", "")
            if description:
                text += f". {description}"
            texts.append(text)

        embeddings = self.embeddings_generator.generate_embeddings_batch(texts).astype("float32")
        faiss.normalize_L2(embeddings)

        dimension = embeddings.shape[1]
        self._index = faiss.IndexFlatIP(dimension)
        self._index.add(embeddings)
        self._id_map = [str(p["id"]) for p in perfumes]
        self._id_to_idx = {pid: i for i, pid in enumerate(self._id_map)}

        self._save_cache(csv_path)

    def semantic_search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Search perfumes by cosine similarity using FAISS."""
        if self._index is None:
            return []

        query_embedding = self.embeddings_generator.generate_embedding(query).astype("float32")
        query_embedding = query_embedding.reshape(1, -1)
        faiss.normalize_L2(query_embedding)

        scores, indices = self._index.search(query_embedding, top_k)

        ids = [self._id_map[i] for i in indices[0]]
        perfumes = self.data_loader.get_perfumes_by_ids(ids)
        for i, perfume in enumerate(perfumes):
            perfume["similarity_score"] = float(scores[0][i])

        return perfumes

    def find_similar_to_perfume(self, perfume_id: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Find perfumes similar to a given perfume using its stored embedding."""
        if self._index is None or perfume_id not in self._id_to_idx:
            return []

        idx = self._id_to_idx[perfume_id]
        embedding = self._index.reconstruct(idx).reshape(1, -1)

        scores, indices = self._index.search(embedding, top_k + 1)

        pairs = [(self._id_map[i], float(s)) for i, s in zip(indices[0], scores[0]) if self._id_map[i] != perfume_id][
            :top_k
        ]

        ids = [pid for pid, _ in pairs]
        score_map = {pid: s for pid, s in pairs}

        perfumes = self.data_loader.get_perfumes_by_ids(set(ids))
        for perfume in perfumes:
            perfume["similarity_score"] = score_map.get(str(perfume.get("id", "")), 0.0)

        return perfumes
