"""
Cargador y gestor del catálogo de perfumes desde CSV.

Este módulo se encarga de:
- Cargar el CSV de Fragrantica
- Limpiar y normalizar los datos
- Proporcionar métodos de búsqueda y filtrado

DÍA 3: Implementarás este módulo después de explorar los datos en el notebook.
"""

from typing import Any, Dict, Iterator, List, Optional

import pandas as pd


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

        if "name" not in df.columns or "brand" not in df.columns:
            raise ValueError("El CSV no tiene las columnas esperadas: 'name', 'brand'")

        df = df.dropna(subset=["name", "brand"])
        df = df.drop_duplicates()
        df["name"] = df["name"].str.strip().str.lower()
        df["brand"] = df["brand"].str.strip().str.lower()

        if "notes" in df.columns:
            df["notes"] = df["notes"].str.strip("[]").str.strip()

        if "id" in df.columns:
            df = df.set_index("id")

        return df

    def get_all_perfumes(self) -> List[Dict[str, Any]]:
        """
        Retorna todos los perfumes como lista de diccionarios.
        """
        return self.df.reset_index().to_dict("records")

    def iter_perfumes(self) -> Iterator[Dict[str, Any]]:
        """
        Itera perfumes uno a uno sin cargar toda la lista en memoria.
        """
        for idx, row in self.df.iterrows():
            yield {"id": idx, **row.to_dict()}

    def get_perfume_by_id(self, perfume_id: str) -> Optional[Dict[str, Any]]:
        """
        Busca un perfume por su ID.
        """
        if perfume_id in self.df.index:
            return self.df.loc[perfume_id].to_dict()
        return None

    def get_perfumes_by_ids(self, ids: set[str]) -> List[Dict[str, Any]]:
        """
        Busca múltiples perfumes por sus IDs.
        """
        return self.df.loc[self.df.index.isin(ids)].to_dict("records")

    def filter_perfumes(self, filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Filtra perfumes por múltiples criterios.
        Lists/sets usan OR substring matching. Strings usan substring matching para season/gender,
        exact match para brand y otros campos escalares.
        """
        _SUBSTRING_COLUMNS = {"notes", "season", "gender"}
        df_filtered = self.df.copy()

        for column, value in filters.items():
            if column not in df_filtered.columns:
                continue
            if isinstance(value, (list, set)):
                mask = pd.Series(False, index=df_filtered.index)
                for v in value:
                    mask = mask | df_filtered[column].str.lower().str.contains(str(v).lower(), na=False)
                df_filtered = df_filtered[mask]
            elif column in _SUBSTRING_COLUMNS:
                df_filtered = df_filtered[df_filtered[column].str.lower().str.contains(value.lower(), na=False)]
            else:
                df_filtered = df_filtered[df_filtered[column].str.lower() == value.lower()]

        return df_filtered.reset_index().to_dict("records")

    def search_by_query(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """
        Búsqueda libre: OR across terms, ranked by match count descending.
        A result must match at least one term in name, notes, description, or brand.
        """
        search_columns = [c for c in ["name", "notes", "description", "brand"] if c in self.df.columns]
        terms = query.lower().split()

        df_work = self.df.copy()

        def _count_matches(row) -> int:
            text = " ".join(str(row[c]) for c in search_columns if c in row.index).lower()
            return sum(1 for t in terms if t in text)

        df_work["_score"] = df_work.apply(_count_matches, axis=1)
        df_filtered = df_work[df_work["_score"] > 0].sort_values("_score", ascending=False)

        return df_filtered.head(max_results).drop(columns=["_score"]).reset_index().to_dict("records")
