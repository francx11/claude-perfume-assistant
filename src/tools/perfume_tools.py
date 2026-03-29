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
        """
        self.data_loader = data_loader
        self.rag_retriever = rag_retriever

    def get_tools_definitions(self) -> List[Dict[str, Any]]:
        """
        Retorna las definiciones de tools en formato Anthropic.
        """
        tool_definitions = []

        tool_definitions.append({
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
        })

        tool_definitions.append({
            "name": "get_perfume_details",
            "description": "Obtiene los detalles completos de un perfume por su ID",
            "input_schema": {
                "type": "object",
                "properties": {
                    "perfume_id": {
                        "type": "string",
                        "description": "ID único del perfume (ej: dior-sauvage)"
                    }
                },
                "required": ["perfume_id"]
            }
        })

        tool_definitions.append(  {
            "name": "recommend_similar",
            "description": "Recomienda perfumes similares",
            "input_schema": {
                "type": "object",
                "properties": {
                    "perfume_id": {
                        "type": "string",
                        "description": "ID único del perfume (ej: dior-sauvage)"
                    },
                    "top_k": {
                        "type": "integer",
                        "description": "Número de perfumes similares a retornar",
                        "default": 3
                    }
                },
                "required": ["perfume_id"]
            }
        })

        return tool_definitions

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
        """

        filters = {
            k: v for k, v in {
                "brand": brand,
                "notes": notes,
                "season": season,
                "gender": gender
            }.items() if v is not None
        }

        results = self.data_loader.filter_perfumes(filters)
        return results[:max_results]

    def get_perfume_details(self, perfume_id: str) -> Dict[str, Any]:
        """
        Obtiene detalles completos de un perfume.
        """
        perfume = self.data_loader.get_perfume_by_id(perfume_id)

        if perfume is None:
            return {"error": "Pefume no encontrado"}

        return perfume

    def recommend_similar(self, perfume_id: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Recomienda perfumes similares usando RAG.
        """
        if self.rag_retriever is None:
            return {"error": "RAG no disponible"}
        
        similar_perfume = self.rag_retriever.find_similar_to_perfume(perfume_id, top_k)

        return similar_perfume

    def execute_tool(self, tool_name: str, tool_input: Dict[str, Any]) -> Any:
        """
        Ejecuta una tool por nombre con sus parámetros.
        """

        match tool_name:
            case "search_perfumes":
                return self.search_perfumes(**tool_input)
            case "get_perfume_details":
                return self.get_perfume_details(**tool_input)
            case "recommend_similar":
                return self.recommend_similar(**tool_input)
            case _:
                return {"error": f"Tool no encontrada: {tool_name}"}
