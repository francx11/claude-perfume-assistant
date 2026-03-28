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


class EmbeddingsGenerator:
    """Generador de embeddings usando sentence-transformers."""

    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        """
        Inicializa el generador de embeddings.

        TODO DÍA 7:
        1. Importar SentenceTransformer: from sentence_transformers import SentenceTransformer
        2. Cargar el modelo: self.model = SentenceTransformer(model_name)
        3. Guardar model_name como atributo

        ¿Qué es un embedding?
        Es una representación vectorial de un texto que captura su significado semántico.
        Textos similares tendrán embeddings cercanos en el espacio vectorial.

        ¿Por qué all-MiniLM-L6-v2?
        - Es pequeño (~80MB) y rápido
        - Genera embeddings de 384 dimensiones
        - Buen balance entre calidad y velocidad
        - Perfecto para aprendizaje

        Args:
            model_name: Nombre del modelo de sentence-transformers
        """
        pass

    def generate_embedding(self, text: str) -> np.ndarray:
        """
        Genera embedding para un texto.

        TODO DÍA 7:
        1. Usar self.model.encode(text) para generar el embedding
        2. El resultado es un numpy array de 384 dimensiones
        3. Retornar el array

        Args:
            text: Texto para el cual generar embedding

        Returns:
            Array numpy con el embedding (shape: (384,))
        """
        pass

    def generate_embeddings_batch(self, texts: List[str]) -> np.ndarray:
        """
        Genera embeddings para múltiples textos (más eficiente).

        TODO DÍA 7:
        1. Usar self.model.encode(texts) pasando la lista completa
        2. El modelo procesará los textos en batches automáticamente
        3. Retornar el array de embeddings

        ¿Por qué batch processing?
        Es mucho más rápido procesar múltiples textos a la vez que uno por uno.
        El modelo puede aprovechar paralelización y optimizaciones.

        Args:
            texts: Lista de textos

        Returns:
            Array numpy con embeddings (shape: (n_texts, 384))
        """
        pass

    def save_embeddings(self, embeddings: np.ndarray, filepath: str) -> None:
        """
        Guarda embeddings en disco.

        TODO DÍA 7:
        1. Usar np.save(filepath, embeddings) para guardar el array
        2. Esto crea un archivo .npy que se puede cargar rápidamente

        ¿Por qué guardar embeddings?
        Generar embeddings para miles de perfumes toma tiempo.
        Guardándolos, solo necesitamos generarlos una vez.

        Args:
            embeddings: Array de embeddings a guardar
            filepath: Ruta donde guardar (ej: "data/embeddings/perfumes.npy")
        """
        pass

    def load_embeddings(self, filepath: str) -> np.ndarray:
        """
        Carga embeddings desde disco.

        TODO DÍA 7:
        1. Usar np.load(filepath) para cargar el array
        2. Retornar el array cargado

        Args:
            filepath: Ruta del archivo .npy

        Returns:
            Array numpy con los embeddings cargados

        Raises:
            FileNotFoundError: Si el archivo no existe
        """
        pass
