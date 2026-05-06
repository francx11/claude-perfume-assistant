# Extend RAG Pipeline

**When to apply:** Changing embeddings model, adding new search strategies, or reindexing the perfume catalog.

## Pipeline Architecture
```
DataLoader.get_all_perfumes()          → List[Dict] with id, name, brand, notes, description
         ↓
EmbeddingsGenerator.generate_embeddings_batch(texts)   src/rag/embeddings.py
         ↓  np.ndarray shape (N, 384)
RAGRetriever.build_index()             saves → data/embeddings/perfumes.npy
         ↓
RAGRetriever.semantic_search(query, top_k)
RAGRetriever.find_similar_to_perfume(perfume_id, top_k)
```

## Text format used for indexing (`src/rag/retriever.py:34`)
```python
text = f"{perfume.get('brand', '')} {perfume.get('name', '')}"
if notes:       text += f". Notes: {notes}"
if description: text += f". {description}"
```
To change what gets indexed, modify this block — then rebuild the index.

## Rebuild index after CSV changes or text-format changes
```python
from src.data.loader import DataLoader
from src.rag.embeddings import EmbeddingsGenerator
from src.rag.retriever import RAGRetriever

loader = DataLoader(csv_path="path/to/fragrantica.csv")
gen = EmbeddingsGenerator()           # model: all-MiniLM-L6-v2
retriever = RAGRetriever(gen, loader)
retriever.build_index(loader.get_all_perfumes())
# Auto-saves to data/embeddings/perfumes.npy
```

## Add a new search strategy
1. Add method to `RAGRetriever` delegating to `semantic_search`:
```python
def search_by_accord(self, accord: str, top_k: int = 5) -> List[Dict[str, Any]]:
    return self.semantic_search(f"perfume with {accord} accord", top_k)
```
2. Expose via `PerfumeTools` (see `add-claude-tool` skill).

## Cosine similarity implementation (`retriever.py:116`)
```python
dot_product = np.dot(vec1, vec2)
norm1, norm2 = np.linalg.norm(vec1), np.linalg.norm(vec2)
return 0.0 if norm1 == 0 or norm2 == 0 else dot_product / (norm1 * norm2)
```
`similarity_score` is attached to each returned perfume dict.

## State that must stay in sync
- `embeddings_matrix` (np.ndarray, shape N×D)
- `perfume_id_to_index` (Dict[str, int], built during `build_index`)
- `data/embeddings/perfumes.npy` (persisted matrix)

If any one of these is updated without the others, search results break.

## Don't
- Don't modify `embeddings_matrix` after `build_index()` — invalidates `perfume_id_to_index`
- Don't load `.npy` without rebuilding `perfume_id_to_index` — index-to-id mapping will be wrong
- Don't pass raw DataFrame rows to `build_index()` — call `.to_dict('records')` first
- Don't query `semantic_search` before `build_index()` — returns empty list silently
- [HUMAN APPROVAL REQUIRED] Don't delete `data/embeddings/perfumes.npy` without a rebuild plan
