"""
Generador de embeddings para búsqueda semántica.

Este módulo se encarga de:
- Cargar modelo de sentence-transformers
- Generar embeddings vectoriales de textos
- Guardar y cargar embeddings desde disco

DÍA 7: Implementarás este módulo para tu primer sistema RAG.
"""

from typing import List

import numpy as np
from sentence_transformers import SentenceTransformer


class EmbeddingsGenerator:
    """Generador de embeddings usando sentence-transformers."""

    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.model_name = model_name
        self._model = None

    @property
    def model(self) -> SentenceTransformer:
        """Lazy-loaded SentenceTransformer — loads on first access."""
        if self._model is None:
            self._model = SentenceTransformer(self.model_name)
        return self._model

    def generate_embedding(self, text: str) -> np.ndarray:
        """Generate a single embedding vector for text."""
        return self.model.encode(text)

    def generate_embeddings_batch(self, texts: List[str]) -> np.ndarray:
        """Generate embeddings for multiple texts (batched, more efficient)."""
        return self.model.encode(texts)

    def save_embeddings(self, embeddings: np.ndarray, filepath: str) -> None:
        """
        Guarda embeddings en disco.
        """
        np.save(filepath, embeddings)

    def load_embeddings(self, filepath: str) -> np.ndarray:
        """
        Carga embeddings desde disco.
        """
        return np.load(filepath)
