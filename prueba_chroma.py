"""Prueba ChromaRetriever vs RAGRetriever original."""

import time

from src.data.loader import DataLoader
from src.rag.chroma_retriever import ChromaRetriever
from src.rag.embeddings import EmbeddingsGenerator
from src.rag.retriever import RAGRetriever

CSV_PATH = "data/raw/fragrantica.csv"
QUERY = "floral perfume for summer, fresh and light"
TOP_K = 5
SAMPLE = 200  # subset para que sea rápido

print("Cargando datos...")
loader = DataLoader(CSV_PATH)
perfumes = loader.get_all_perfumes()[:SAMPLE]
print(f"{len(perfumes)} perfumes cargados\n")

print("Inicializando embeddings generator...")
gen = EmbeddingsGenerator()

# --- RAGRetriever original ---
print("=== RAGRetriever (cosine manual) ===")
rag = RAGRetriever(gen, loader)
t0 = time.time()
rag.build_index(perfumes)
t_build_rag = time.time() - t0

t0 = time.time()
results_rag = rag.semantic_search(QUERY, top_k=TOP_K)
t_search_rag = time.time() - t0

print(f"Build: {t_build_rag:.2f}s | Search: {t_search_rag:.4f}s")
for p in results_rag:
    print(f"  [{p['similarity_score']:.3f}] {p.get('brand', '?')} - {p.get('name', '?')}")

# --- ChromaRetriever ---
print("\n=== ChromaRetriever (HNSW) ===")
chroma = ChromaRetriever(gen, loader)
t0 = time.time()
chroma.build_index(perfumes)
t_build_chroma = time.time() - t0

t0 = time.time()
results_chroma = chroma.semantic_search(QUERY, top_k=TOP_K)
t_search_chroma = time.time() - t0

print(f"Build: {t_build_chroma:.2f}s | Search: {t_search_chroma:.4f}s")
for p in results_chroma:
    print(f"  [{p['similarity_score']:.3f}] {p.get('brand', '?')} - {p.get('name', '?')}")
