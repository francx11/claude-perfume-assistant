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

        TODO DÍA 7:
        1. Guardar embeddings_generator y data_loader como atributos
        2. Inicializar self.embeddings_matrix = None
        3. Inicializar self.perfume_id_to_index = {}

        Args:
            embeddings_generator: Instancia de EmbeddingsGenerator
            data_loader: Instancia de DataLoader
        """
        pass

    def build_index(self, perfumes: List[Dict[str, Any]]) -> None:
        """
        Construye índice de embeddings para todos los perfumes.

        TODO DÍA 7:
        1. Para cada perfume, crear un texto descriptivo combinando:
           - brand + name
           - notes (unidas con comas)
           - description (si existe)
        2. Generar embeddings para todos los textos usando generate_embeddings_batch()
        3. Guardar embeddings en self.embeddings_matrix
        4. Crear mapeo de perfume_id -> índice en self.perfume_id_to_index
        5. Opcionalmente, guardar embeddings en disco con save_embeddings()

        ¿Por qué crear un texto descriptivo?
        El embedding debe capturar toda la información relevante del perfume
        para que la búsqueda semántica funcione bien.

        Args:
            perfumes: Lista de perfumes del catálogo
        """
        pass

    def semantic_search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Busca perfumes más similares a la query.

        TODO DÍA 7:
        1. Generar embedding de la query con embeddings_generator.generate_embedding()
        2. Calcular similitud coseno entre query_embedding y cada embedding en self.embeddings_matrix
        3. Ordenar resultados por similitud (mayor a menor)
        4. Tomar los top_k resultados
        5. Obtener datos completos de los perfumes usando data_loader.get_perfumes_by_ids()
        6. Agregar campo 'similarity_score' a cada perfume
        7. Retornar lista de perfumes

        ¿Qué es similitud coseno?
        Mide el ángulo entre dos vectores. Valores cercanos a 1 = muy similares.
        Es la métrica estándar para comparar embeddings.

        Args:
            query: Texto de búsqueda del usuario
            top_k: Número de resultados a retornar

        Returns:
            Lista de perfumes ordenados por relevancia
        """
        pass

    def find_similar_to_perfume(self, perfume_id: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Encuentra perfumes similares a uno dado.

        TODO DÍA 7:
        1. Obtener índice del perfume usando self.perfume_id_to_index[perfume_id]
        2. Obtener embedding del perfume desde self.embeddings_matrix[index]
        3. Calcular similitud con todos los demás perfumes
        4. Ordenar y tomar top_k (excluyendo el perfume original)
        5. Retornar lista de perfumes similares

        Args:
            perfume_id: ID del perfume de referencia
            top_k: Número de similares a retornar

        Returns:
            Lista de perfumes similares
        """
        pass

    def _cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """
        Calcula similitud coseno entre dos vectores.

        TODO DÍA 7:
        1. Calcular producto punto: dot_product = np.dot(vec1, vec2)
        2. Calcular normas: norm1 = np.linalg.norm(vec1), norm2 = np.linalg.norm(vec2)
        3. Retornar: dot_product / (norm1 * norm2)

        Fórmula: cos(θ) = (A · B) / (||A|| * ||B||)

        Args:
            vec1: Primer vector
            vec2: Segundo vector

        Returns:
            Similitud coseno (entre -1 y 1)
        """
        pass
