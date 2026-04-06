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
        """
        self.csv_path = csv_path
        df = self.load_data()
        self.df = df

    def load_data(self) -> pd.DataFrame:
        """
        Carga y limpia el CSV de perfumes.
        """
        try:
            df = pd.read_csv(self.csv_path)
        except FileNotFoundError:
            raise FileNotFoundError(f"CSV no encontrado: {self.csv_path}")

        if 'name' not in df.columns or 'brand' not in df.columns:
            raise ValueError("El CSV no tiene las columnas esperadas: 'name', 'brand'")

        df = df.dropna(subset=['name', 'brand'])
        df = df.drop_duplicates()
        df['name'] = df['name'].str.strip().str.lower()
        df['brand'] = df['brand'].str.strip().str.lower()

        if 'id' in df.columns:
            df = df.set_index('id')

        return df

    def get_all_perfumes(self) -> List[Dict[str, Any]]:
        """
        Retorna todos los perfumes como lista de diccionarios.
        """
        return self.df.reset_index().to_dict('records')

    def get_perfume_by_id(self, perfume_id: str) -> Optional[Dict[str, Any]]:
        """
        Busca un perfume por su ID.
        """
        if perfume_id in self.df.index:
            return self.df.loc[perfume_id].to_dict()
        return None

    def get_perfumes_by_ids(self, ids: List[str]) -> List[Dict[str, Any]]:
        """
        Busca múltiples perfumes por sus IDs.
        """
        return self.df.loc[self.df.index.isin(ids)].to_dict('records')

    def filter_perfumes(self, filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Filtra perfumes por múltiples criterios.
        """
        df_filtered = self.df.copy()

        for column, value in filters.items():
            if isinstance(value, list):
                df_filtered = df_filtered[
                    df_filtered[column].str.contains('|'.join(value), case=False, na=False)
                ]
            else:
                df_filtered = df_filtered[
                    df_filtered[column].str.lower() == value.lower()
                ]

        return df_filtered.to_dict('records')

