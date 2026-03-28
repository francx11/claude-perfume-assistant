"""
Cargador y gestor del catálogo de perfumes desde CSV.

Este módulo se encarga de:
- Cargar el CSV de Fragrantica
- Limpiar y normalizar los datos
- Proporcionar métodos de búsqueda y filtrado

DÍA 3: Implementarás este módulo después de explorar los datos en el notebook.
"""

import pandas as pd
from typing import List, Dict, Any, Optional


class DataLoader:
    """Cargador y gestor del catálogo de perfumes."""

    def __init__(self, csv_path: str):
        """
        Inicializa el loader y carga el CSV.

        TODO DÍA 3:
        1. Guardar csv_path como atributo
        2. Llamar a self.load_data() para cargar el CSV
        3. Guardar el DataFrame en self.df

        Args:
            csv_path: Ruta al archivo CSV de Fragrantica
        """
        pass

    def load_data(self) -> pd.DataFrame:
        """
        Carga y limpia el CSV de perfumes.

        TODO DÍA 3:
        1. Usar pd.read_csv() para cargar el archivo
        2. Limpiar datos:
           - Eliminar filas con valores nulos en columnas críticas (name, brand)
           - Eliminar duplicados
           - Normalizar nombres (strip, lowercase para búsquedas)
        3. Crear índice por ID si existe columna 'id'
        4. Retornar el DataFrame limpio

        ¿Qué aprendes aquí?
        - Carga de datos con pandas
        - Limpieza básica de datos
        - Preparación de datos para uso en producción

        Returns:
            DataFrame con los datos limpios

        Raises:
            FileNotFoundError: Si el CSV no existe
            ValueError: Si el CSV no tiene las columnas esperadas
        """
        pass

    def get_all_perfumes(self) -> List[Dict[str, Any]]:
        """
        Retorna todos los perfumes como lista de diccionarios.

        TODO DÍA 3:
        1. Convertir self.df a lista de diccionarios con .to_dict('records')
        2. Retornar la lista

        Returns:
            Lista de perfumes (cada uno es un diccionario)
        """
        pass

    def get_perfume_by_id(self, perfume_id: str) -> Optional[Dict[str, Any]]:
        """
        Busca un perfume por su ID.

        TODO DÍA 3:
        1. Filtrar self.df por la columna 'id' == perfume_id
        2. Si existe, convertir la fila a diccionario y retornarla
        3. Si no existe, retornar None

        Args:
            perfume_id: ID del perfume a buscar

        Returns:
            Diccionario con datos del perfume o None si no existe
        """
        pass

    def get_perfumes_by_ids(self, ids: List[str]) -> List[Dict[str, Any]]:
        """
        Busca múltiples perfumes por sus IDs.

        TODO DÍA 3:
        1. Filtrar self.df donde 'id' esté en la lista ids
        2. Convertir resultados a lista de diccionarios
        3. Retornar la lista

        ¿Por qué necesitamos esto?
        El RAG retriever retornará IDs de perfumes similares,
        y necesitamos obtener sus datos completos.

        Args:
            ids: Lista de IDs de perfumes

        Returns:
            Lista de perfumes encontrados
        """
        pass

    def filter_perfumes(self, filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Filtra perfumes por múltiples criterios.

        TODO DÍA 3:
        1. Empezar con df_filtered = self.df.copy()
        2. Para cada filtro en filters:
           - Si el filtro es una lista (ej: notes), verificar que algún valor coincida
           - Si es un string (ej: brand), verificar igualdad exacta
           - Si es un rango (ej: year), verificar que esté en el rango
        3. Convertir df_filtered a lista de diccionarios
        4. Retornar la lista

        Ejemplo de filtros:
        {
            "brand": "Dior",
            "season": "summer",
            "notes": ["citrus", "fresh"]  # Perfume debe tener al menos una de estas notas
        }

        Args:
            filters: Diccionario con criterios de filtrado

        Returns:
            Lista de perfumes que cumplen todos los criterios
        """
        pass
