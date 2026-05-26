"""
Tools para que Claude pueda buscar, filtrar y recomendar perfumes.

Este módulo implementa:
- Definiciones de tools en formato Anthropic
- Funciones ejecutables para cada tool
- Integración con DataLoader y RAG

DÍA 4: Implementarás este módulo para darle "superpoderes" a Claude.
"""

from typing import Any, Dict, List, Optional


def log_call(func):
    """Decorator that logs function name and arguments before each call."""

    def wrapper(*args, **kwargs):
        """Execute the wrapped function after logging its invocation."""
        print(f"[tool] {func.__name__} | args={args[1:]} kwargs={kwargs}")
        return func(*args, **kwargs)

    return wrapper


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

        tool_definitions.append(
            {
                "name": "search_perfumes",
                "description": (
                    "Busca perfumes por criterios específicos. "
                    "Usa 'query' para búsqueda libre en inglés (ej: 'rose jasmine romantic evening'). "
                    "Combina con 'brand', 'notes' o 'season' para filtros adicionales. "
                    "Para ocasiones románticas usa términos en inglés: rose, jasmine, vanilla, musk, oud, amber."
                ),
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": (
                                "Búsqueda libre en inglés sobre nombre, notas y descripción "
                                "(ej: 'rose romantic evening', 'fresh citrus summer', 'woody masculine')"
                            ),
                        },
                        "brand": {"type": "string", "description": "Marca del perfume (ej: Dior, Chanel)"},
                        "notes": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Notas olfativas en inglés (ej: rose, vanilla, citrus, woody, musk)",
                        },
                        "season": {
                            "type": "string",
                            "enum": ["spring", "summer", "fall", "winter", "all-year"],
                            "description": "Temporada recomendada",
                        },
                        "gender": {
                            "type": "string",
                            "enum": ["male", "female", "unisex"],
                            "description": "Género del perfume",
                        },
                    },
                },
            }
        )

        tool_definitions.append(
            {
                "name": "get_perfume_details",
                "description": "Obtiene los detalles completos de un perfume por su ID",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "perfume_id": {"type": "string", "description": "ID único del perfume (ej: dior-sauvage)"}
                    },
                    "required": ["perfume_id"],
                },
            }
        )

        tool_definitions.append(
            {
                "name": "recommend_similar",
                "description": "Recomienda perfumes similares",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "perfume_id": {"type": "string", "description": "ID único del perfume (ej: dior-sauvage)"},
                        "top_k": {
                            "type": "integer",
                            "description": "Número de perfumes similares a retornar",
                            "default": 3,
                        },
                    },
                    "required": ["perfume_id"],
                },
            }
        )

        return tool_definitions

    def search_perfumes(
        self,
        query: Optional[str] = None,
        brand: Optional[str] = None,
        notes: Optional[List[str]] = None,
        season: Optional[str] = None,
        gender: Optional[str] = None,
        max_results: int = 5,
    ) -> List[Dict[str, Any]]:
        """
        Busca perfumes por criterios específicos.
        Si se provee query, arranca desde búsqueda libre; luego aplica filtros adicionales.
        """
        if query:
            results = self.data_loader.search_by_query(query, max_results=50)
            # Aplicar filtros adicionales sobre los resultados de query
            import pandas as pd

            if results:
                df = pd.DataFrame(results)
                if brand and "brand" in df.columns:
                    df = df[df["brand"].str.lower() == brand.lower()]
                if season and "season" in df.columns:
                    df = df[df["season"].str.lower() == season.lower()]
                if gender and "gender" in df.columns:
                    df = df[df["gender"].str.lower() == gender.lower()]
                if notes and "notes" in df.columns:
                    for note in notes:
                        df = df[df["notes"].str.lower().str.contains(note.lower(), na=False)]
                return df.head(max_results).to_dict("records")
            return []

        filters = {
            k: v
            for k, v in {"brand": brand, "notes": notes, "season": season, "gender": gender}.items()
            if v is not None
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

    @log_call
    def execute_tool(self, tool_name: str, tool_input: Dict[str, Any]) -> Any:
        """
        Ejecuta una tool por nombre con sus parámetros.
        """
        registry = {
            "search_perfumes": self.search_perfumes,
            "get_perfume_details": self.get_perfume_details,
            "recommend_similar": self.recommend_similar,
        }
        handler = registry.get(tool_name)
        if handler is None:
            return {"error": f"Tool no encontrada: {tool_name}"}
        return handler(**tool_input)
