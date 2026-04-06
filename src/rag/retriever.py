"""
Sistema de búsqueda semántica usando embeddings.

Este módulo implementa:
- Construcción de índice de embeddings
- Búsqueda por similitud coseno
- Ranking de resultados por relevancia

DÍA 7: Implementarás este módulo para completar tu sistema RAG.
"""

import numpy as np
from typing import List, Dict, Any


class RAGRetriever:
    """Retriever para búsqueda semántica de perfumes."""

    def __init__(self, embeddings_generator, data_loader):
        """
        Inicializa el retriever.
        """
        self.embeddings_generator = embeddings_generator
        self.data_loader = data_loader
        self.embeddings_matrix = None
        self.perfume_id_to_index = {}

    def build_index(self, perfumes: List[Dict[str, Any]]) -> None:
        """
        Construye índice de embeddings para todos los perfumes.
        """
        texts = []
        for perfume in perfumes:
            text = f"{perfume.get('brand', '')} {perfume.get('name', '')}"
            
            notes = perfume.get('notes', '')
            if notes:
                text += f". Notes: {notes}"
            
            description = perfume.get('description', '')
            if description:
                text += f". {description}"
            
            texts.append(text)

        self.embeddings_matrix = self.embeddings_generator.generate_embeddings_batch(texts)
        self.perfume_id_to_index = {}

        for i, perfume in enumerate(perfumes):
            self.perfume_id_to_index[perfume['id']] = i

        import os
        os.makedirs("data/embeddings", exist_ok=True)
        self.embeddings_generator.save_embeddings(
            self.embeddings_matrix,
            "data/embeddings/perfumes.npy"
        )

    def semantic_search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Busca perfumes más similares a la query.
        """
        if self.embeddings_matrix is None:
            return []

        query_embedding = self.embeddings_generator.generate_embedding(query)
        scores = []
        for i in range(len(self.embeddings_matrix)):
            score = self._cosine_similarity(query_embedding, self.embeddings_matrix[i])
            scores.append((i, score))

        scores.sort(key=lambda x: x[1], reverse=True)
        top_indices = [idx for idx, score in scores[:top_k]]
        top_scores = [score for idx, score in scores[:top_k]]

        index_to_id = {v: k for k, v in self.perfume_id_to_index.items()}
        top_ids = [index_to_id[i] for i in top_indices]

        perfumes = self.data_loader.get_perfumes_by_ids(top_ids)
        for i, perfume in enumerate(perfumes):
            perfume["similarity_score"] = top_scores[i]

        return perfumes

    def find_similar_to_perfume(self, perfume_id: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Encuentra perfumes similares a uno dado.
        """
        if perfume_id not in self.perfume_id_to_index:
            return []
        index = self.perfume_id_to_index[perfume_id]

        perfume_embedding = self.embeddings_matrix[index]

        scores = []
        for i in range(len(self.embeddings_matrix)):
            if i == index:
                continue
            score = self._cosine_similarity(perfume_embedding, self.embeddings_matrix[i])
            scores.append((i, score))

        scores.sort(key=lambda x: x[1], reverse=True)

        top_indices = [idx for idx, score in scores[:top_k]]
        top_scores = [score for idx, score in scores[:top_k]]

        index_to_id = {v: k for k, v in self.perfume_id_to_index.items()}
        top_ids = [index_to_id[i] for i in top_indices]

        perfumes = self.data_loader.get_perfumes_by_ids(top_ids)
        for i, perfume in enumerate(perfumes):
            perfume["similarity_score"] = top_scores[i]

        return perfumes

    def _cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """
        Calcula similitud coseno entre dos vectores.
        """
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        if norm1 == 0 or norm2 == 0:
            return 0.0
        return dot_product / (norm1 * norm2)
