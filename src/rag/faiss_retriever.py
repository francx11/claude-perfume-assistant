"""FAISS-backed semantic retriever for perfume search."""

from typing import Any, Dict, List

import faiss


class FAISSRetriever:
    """Retriever using FAISS IndexFlatIP for cosine similarity search."""

    def __init__(self, embeddings_generator, data_loader):
        self.embeddings_generator = embeddings_generator
        self.data_loader = data_loader
        self._index = None
        self._id_map: List[str] = []
        self._id_to_idx: Dict[str, int] = {}

    def build_index(self, perfumes: List[Dict[str, Any]]) -> None:
        """Build FAISS index from perfume list."""
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
        faiss.normalize_L2(embeddings)  # |v| = 1 so inner product = cosine similarity

        dimension = embeddings.shape[1]
        self._index = faiss.IndexFlatIP(dimension)
        self._index.add(embeddings)
        self._id_map = [str(p["id"]) for p in perfumes]
        self._id_to_idx = {pid: i for i, pid in enumerate(self._id_map)}

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
