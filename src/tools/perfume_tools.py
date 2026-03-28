"""
Tools para que Claude pueda buscar, filtrar y recomendar perfumes.

Este módulo implementa:
- Definiciones de tools en formato Anthropic
- Funciones ejecutables para cada tool
- Integración con DataLoader y RAG

DÍA 4: Implementarás este módulo para darle "superpoderes" a Claude.
"""

from typing import List, Dict, Any, Optional


class PerfumeTools:
    """Tools para búsqueda y recomendación de perfumes."""

    def __init__(self, data_loader, rag_retriever=None):
        """
        Inicializa las tools.

        TODO DÍA 4:
        1. Guardar data_loader como atributo
        2. Guardar rag_retriever como atributo (puede ser None al inicio)

        Args:
            data_loader: Instancia de DataLoader
            rag_retriever: Instancia de RAGRetriever (opcional, se agrega en día 7)
        """
        pass

    def get_tools_definitions(self) -> List[Dict[str, Any]]:
        """
        Retorna las definiciones de tools en formato Anthropic.

        TODO DÍA 4:
        1. Crear una lista con definiciones de tools
        2. Cada tool debe tener:
           - name: nombre en snake_case
           - description: qué hace la tool
           - input_schema: JSON Schema con los parámetros

        Ejemplo de una tool:
        {
            "name": "search_perfumes",
            "description": "Busca perfumes por criterios específicos como marca, notas, temporada",
            "input_schema": {
                "type": "object",
                "properties": {
                    "brand": {
                        "type": "string",
                        "description": "Marca del perfume (ej: Dior, Chanel)"
                    },
                    "notes": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Notas olfativas (ej: citrus, woody, floral)"
                    },
                    "season": {
                        "type": "string",
                        "enum": ["spring", "summer", "fall", "winter", "all-year"],
                        "description": "Temporada recomendada"
                    }
                }
            }
        }

        Tools a implementar:
        1. search_perfumes: Buscar por criterios
        2. get_perfume_details: Obtener detalles de un perfume específico
        3. recommend_similar: Recomendar perfumes similares (día 7, requiere RAG)

        Returns:
            Lista de definiciones de tools
        """
        pass

    def search_perfumes(
        self,
        brand: Optional[str] = None,
        notes: Optional[List[str]] = None,
        season: Optional[str] = None,
        gender: Optional[str] = None,
        max_results: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Busca perfumes por criterios específicos.

        TODO DÍA 4:
        1. Construir diccionario de filtros con los parámetros no-None
        2. Llamar a data_loader.filter_perfumes(filters)
        3. Limitar resultados a max_results
        4. Retornar lista de perfumes

        Args:
            brand: Marca del perfume
            notes: Lista de notas olfativas
            season: Temporada
            gender: Género objetivo
            max_results: Máximo número de resultados

        Returns:
            Lista de perfumes que cumplen los criterios
        """
        pass

    def get_perfume_details(self, perfume_id: str) -> Dict[str, Any]:
        """
        Obtiene detalles completos de un perfume.

        TODO DÍA 4:
        1. Llamar a data_loader.get_perfume_by_id(perfume_id)
        2. Si no existe, retornar {"error": "Perfume no encontrado"}
        3. Si existe, retornar el diccionario del perfume

        Args:
            perfume_id: ID del perfume

        Returns:
            Diccionario con datos del perfume o error
        """
        pass

    def recommend_similar(self, perfume_id: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Recomienda perfumes similares usando RAG.

        TODO DÍA 7 (no día 4):
        1. Verificar que self.rag_retriever no sea None
        2. Si es None, retornar {"error": "RAG no disponible"}
        3. Llamar a rag_retriever.find_similar_to_perfume(perfume_id, top_k)
        4. Retornar lista de perfumes similares

        ¿Por qué esto es día 7?
        Necesitas implementar el sistema RAG primero.
        Por ahora, puedes dejar esta función con un pass o retornar error.

        Args:
            perfume_id: ID del perfume de referencia
            top_k: Número de similares a retornar

        Returns:
            Lista de perfumes similares
        """
        pass

    def execute_tool(self, tool_name: str, tool_input: Dict[str, Any]) -> Any:
        """
        Ejecuta una tool por nombre con sus parámetros.

        TODO DÍA 4:
        1. Usar un if/elif para determinar qué tool ejecutar
        2. Llamar al método correspondiente con los parámetros de tool_input
        3. Retornar el resultado
        4. Si tool_name no existe, retornar {"error": "Tool no encontrada"}

        Ejemplo:
        if tool_name == "search_perfumes":
            return self.search_perfumes(**tool_input)
        elif tool_name == "get_perfume_details":
            return self.get_perfume_details(**tool_input)
        ...

        ¿Por qué necesitamos esto?
        Claude nos dirá qué tool ejecutar y con qué parámetros.
        Este método hace el dispatch dinámico.

        Args:
            tool_name: Nombre de la tool a ejecutar
            tool_input: Diccionario con parámetros

        Returns:
            Resultado de ejecutar la tool
        """
        pass
