"""ChromaDB-backed semantic retriever for perfume search."""

from typing import Any, Dict, List

import chromadb


class ChromaRetriever:
    """Retriever using ChromaDB vector store instead of manual cosine similarity."""

    def __init__(self, embeddings_generator, data_loader):
        self.embeddings_generator = embeddings_generator
        self.data_loader = data_loader
        self._client = chromadb.Client()
        self._collection = self._client.create_collection(
            "perfumes",
            metadata={"hnsw:space": "cosine"},
        )

    def build_index(self, perfumes: List[Dict[str, Any]]) -> None:
        """Build ChromaDB collection from perfume list."""
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

        embeddings = self.embeddings_generator.generate_embeddings_batch(texts)

        self._collection.add(
            ids=[str(p["id"]) for p in perfumes],
            embeddings=embeddings.tolist(),
            documents=texts,
            metadatas=[
                {
                    "brand": str(p.get("brand", "")),
                    "name": str(p.get("name", "")),
                    "price": float(p["price"]) if p.get("price") else 0.0,
                    "gender": str(p.get("gender", "")),
                }
                for p in perfumes
            ],
        )

    def semantic_search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Search perfumes by semantic similarity using ChromaDB."""
        query_embedding = self.embeddings_generator.generate_embedding(query)

        results = self._collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=top_k,
        )

        ids = results["ids"][0]
        distances = results["distances"][0]

        perfumes = self.data_loader.get_perfumes_by_ids(ids)
        for i, perfume in enumerate(perfumes):
            perfume["similarity_score"] = 1.0 - distances[i]

        return perfumes
