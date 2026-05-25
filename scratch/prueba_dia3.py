"""
Script de prueba para Día 3: DataLoader
"""
from src.data.loader import DataLoader

loader = DataLoader("data/raw/fragrantica.csv")

# 1. Todos los perfumes
perfumes = loader.get_all_perfumes()
print(f"Total perfumes: {len(perfumes)}")
print(f"Primero: {perfumes[0]['name']} - {perfumes[0]['brand']}\n")

# 2. Buscar por ID
perfume = loader.get_perfume_by_id("dior-sauvage")
print(f"Por ID 'dior-sauvage': {perfume}\n")

# 3. Buscar varios por ID
varios = loader.get_perfumes_by_ids(["dior-sauvage", "creed-aventus"])
print(f"Por IDs: {[p['name'] for p in varios]}\n")

# 4. Filtrar por brand
filtrados = loader.filter_perfumes({"brand": "Dior"})
print(f"Filtro brand=Dior: {[p['name'] for p in filtrados]}\n")

# 5. Filtrar por notas
filtrados = loader.filter_perfumes({"notes": ["vanilla", "musk"]})
print(f"Filtro notes=[vanilla, musk]: {[p['name'] for p in filtrados]}")
