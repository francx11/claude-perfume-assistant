# Día 7: Embeddings y Búsqueda Semántica (RAG)

## Python y NumPy

### NumPy (`np`)

Librería de computación numérica de Python. Equivalente a tener arrays de alto rendimiento. En PHP trabajas con arrays normales, en Python cuando necesitas operaciones matemáticas sobre grandes cantidades de números usas NumPy:

```python
import numpy as np

array = np.array([1.0, 2.0, 3.0])
array * 2           # [2.0, 4.0, 6.0] — operación vectorizada sin bucles
np.dot(a, b)        # producto punto entre dos vectores
np.linalg.norm(v)   # norma (longitud) de un vector
```

### `enumerate()`

Devuelve índice y elemento a la vez en un bucle:

```python
for i, perfume in enumerate(perfumes):
    self.perfume_id_to_index[perfume['id']] = i
```

Equivalente a `foreach ($perfumes as $i => $perfume)` en PHP.

### Invertir un diccionario

```python
index_to_id = {v: k for k, v in self.perfume_id_to_index.items()}
```

Convierte `{id: index}` en `{index: id}` para buscar en sentido inverso.

### `reset_index()` en pandas

Cuando usas `set_index('id')` en un DataFrame, el campo `id` deja de ser una columna y pasa a ser el índice. Para recuperarlo como columna al convertir a diccionario:

```python
df.reset_index().to_dict('records')  # el id vuelve a aparecer como campo
```

---

## El algoritmo del Retriever: Similitud Coseno

### Qué es

Mide el ángulo entre dos vectores en un espacio de alta dimensión. No mide la distancia (longitud), sino la dirección. Dos vectores que apuntan en la misma dirección tienen similitud 1, aunque tengan magnitudes distintas.

### Fórmula

```
cos(θ) = (A · B) / (||A|| × ||B||)
```

- `A · B` = producto punto (suma de productos elemento a elemento)
- `||A||` = norma de A (raíz cuadrada de la suma de cuadrados)
- Resultado entre -1 y 1. En embeddings normalizados, entre 0 y 1.

### Implementación

```python
def _cosine_similarity(self, vec1, vec2):
    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot_product / (norm1 * norm2)
```

### Complejidad del algoritmo actual

El retriever implementado es **búsqueda lineal O(n)**:

- Para cada query, calcula similitud con TODOS los perfumes
- Con 25 perfumes es instantáneo
- Con 1 millón de perfumes sería inaceptablemente lento

---

## Técnicas alternativas e innovadoras para el Retriever

### 1. FAISS (Facebook AI Similarity Search)

Librería de Meta para búsqueda aproximada de vecinos más cercanos (ANN). En lugar de comparar con todos los vectores, usa estructuras de índice que permiten búsquedas en O(log n):

```python
import faiss
index = faiss.IndexFlatL2(384)  # 384 dimensiones
index.add(embeddings_matrix)
distances, indices = index.search(query_embedding, k=5)
```

Usado en producción por empresas como Meta, Spotify y Airbnb.

### 2. HNSW (Hierarchical Navigable Small World)

Algoritmo de grafos para búsqueda aproximada. Construye un grafo jerárquico donde los nodos cercanos están conectados. Mucho más rápido que búsqueda lineal con pérdida mínima de precisión. Disponible en la librería `hnswlib`.

### 3. Bases de datos vectoriales

Soluciones especializadas para almacenar y buscar embeddings a escala:

- **Pinecone**: servicio cloud, sin infraestructura que gestionar
- **Weaviate**: open source, combina búsqueda vectorial con filtros tradicionales
- **Chroma**: ligero, ideal para proyectos pequeños y prototipos
- **pgvector**: extensión de PostgreSQL para vectores, ideal si ya usas Postgres

### 4. Hybrid Search (BM25 + Embeddings)

Combina búsqueda por palabras clave (BM25, como Elasticsearch) con búsqueda semántica por embeddings. El resultado final pondera ambas puntuaciones:

```
score_final = α × score_bm25 + (1-α) × score_semántico
```

Mejor que usar solo embeddings cuando el usuario busca términos exactos (nombres de marcas, notas específicas).

### 5. Re-ranking con Cross-Encoders

Dos fases:

1. Recuperar top-100 candidatos con embeddings (rápido)
2. Re-rankear con un modelo más preciso (cross-encoder) que analiza query+documento juntos

Mucho más preciso que solo embeddings, con coste computacional razonable porque solo re-rankea los candidatos preseleccionados.

---

## Para entrevista

**¿Qué es un embedding?**
Una representación densa de texto en un espacio vectorial de alta dimensión donde la proximidad geométrica refleja similitud semántica. Textos con significado similar producen vectores cercanos.

**¿Por qué similitud coseno y no distancia euclidiana?**
La distancia euclidiana es sensible a la magnitud de los vectores. La similitud coseno solo mide la dirección, lo que la hace más robusta para comparar textos de diferente longitud. Dos textos que hablan de lo mismo pero uno es más largo tendrán vectores similares en dirección aunque distintos en magnitud.

**¿Cuál es el problema de escalar el retriever actual?**
Es O(n): compara la query con cada embedding uno a uno. Con millones de documentos es inviable. La solución es usar índices ANN (Approximate Nearest Neighbors) como FAISS o HNSW que sacrifican un pequeño porcentaje de precisión a cambio de búsquedas en O(log n).

**¿Qué es RAG y por qué es mejor que fine-tuning?**
RAG (Retrieval-Augmented Generation) recupera documentos relevantes en tiempo real y los pasa como contexto al LLM. Es más flexible que fine-tuning porque los datos se pueden actualizar sin reentrenar el modelo, y más barato porque no requiere GPU para entrenamiento.
