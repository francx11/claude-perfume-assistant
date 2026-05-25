"""
Script de prueba para Día 7: RAG (Embeddings + Retriever)
"""
from src.data.loader import DataLoader
from src.rag.embeddings import EmbeddingsGenerator
from src.rag.retriever import RAGRetriever

print("=== Prueba RAG Día 7 ===\n")

# Inicializar componentes
loader = DataLoader("data/raw/fragrantica.csv")
embeddings_gen = EmbeddingsGenerator()
retriever = RAGRetriever(embeddings_generator=embeddings_gen, data_loader=loader)

# Construir índice
print("Construyendo índice de embeddings (puede tardar unos segundos)...")
perfumes = loader.get_all_perfumes()
retriever.build_index(perfumes)
print(f"Índice construido con {len(perfumes)} perfumes\n")

# 1. Búsqueda semántica
print("=== Búsqueda semántica ===")
query = "perfume fresco para el verano con notas cítricas"
resultados = retriever.semantic_search(query, top_k=3)
print(f"Query: '{query}'")
for p in resultados:
    print(f"  - {p['name']} ({p['brand']}) | score: {p['similarity_score']:.3f}")

print()

# 2. Perfumes similares
print("=== Perfumes similares a Dior Sauvage ===")
similares = retriever.find_similar_to_perfume("dior-sauvage", top_k=3)
for p in similares:
    print(f"  - {p['name']} ({p['brand']}) | score: {p['similarity_score']:.3f}")
