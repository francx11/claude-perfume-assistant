"""
Generador de embeddings para búsqueda semántica.

Este módulo se encarga de:
- Cargar modelo de sentence-transformers
- Generar embeddings vectoriales de textos
- Guardar y cargar embeddings desde disco

DÍA 7: Implementarás este módulo para tu primer sistema RAG.
"""

import numpy as np
from typing import List
from sentence_transformers import SentenceTransformer


class EmbeddingsGenerator:
    """Generador de embeddings usando sentence-transformers."""

    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        """
        Inicializa el generador de embeddings.
        """
        self.model = SentenceTransformer(model_name)
        self.model_name = model_name

    def generate_embedding(self, text: str) -> np.ndarray:
        """
        Genera embedding para un texto.
        """
        return self.model.encode(text)

    def generate_embeddings_batch(self, texts: List[str]) -> np.ndarray:
        """
        Genera embeddings para múltiples textos (más eficiente).
        """
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