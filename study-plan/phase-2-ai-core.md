# Phase 2: AI Core

**Prerequisite:** Phase 1 complete.
**Goal:** Classical ML for interviews + deepen RAG + LLMs advanced + data frameworks.

---

## Part A: Classical ML Concepts [INTERVIEW CRITICAL]

> These are conceptual/interview topics. You don't need to implement them — you need to explain them clearly.

### Classification Models

| Topic | Interview Questions | Status |
|-------|-------------------|--------|
| Logistic regression | "How does logistic regression work?" | [ ] |
| Decision tree | "What is a decision tree? What are its weaknesses?" | [ ] |
| Random forest | "How does random forest improve on a single tree?" | [ ] |
| SVM | "What is SVM? What is a kernel trick?" | [ ] |
| KNN | "How does KNN work? What are its limitations?" | [ ] |
| Multiclass selection | "How do you choose a model for a multiclass problem?" | [ ] |

**Exercise:** The perfume recommendation could be framed as classification. Ask Claude: "If I wanted to classify a query as one of 10 perfume families, which model would I choose and why?"

---

### Model Evaluation

| Topic | Interview Questions | Status |
|-------|-------------------|--------|
| Confusion matrix | "What is a confusion matrix? What are TP, FP, FN, TN?" | [ ] |
| Precision/Recall/F1 | "When do you optimize for precision vs recall?" | [ ] |
| Cross-validation | "What is k-fold cross-validation? Why use it?" | [ ] |
| Overfitting | "What is overfitting? How do you prevent it?" | [ ] |
| Imbalanced data | "Your dataset is 95% class A, 5% class B. What do you do?" | [ ] |

**Exercise:** Confusion matrix drill — Claude gives you a 2x2 matrix with numbers, you calculate precision, recall, and F1. Do it without looking at formulas.

---

### Model Internals

| Topic | Interview Questions | Status |
|-------|-------------------|--------|
| Learning rate | "What is learning rate? What happens if it's too high/low?" | [ ] |
| Gradient descent | "Explain gradient descent in plain terms." | [ ] |
| Fine-tuning | "What is fine-tuning? How is it different from training from scratch?" | [ ] |
| PCA | "What is PCA? When would you use it?" | [ ] |
| Feature importance | "How do you identify which features matter most?" | [ ] |

**Resources:**
- [StatQuest YouTube — ML fundamentals](https://www.youtube.com/@statquest) (visual, excellent for interview prep)
- [Scikit-learn docs — User Guide](https://scikit-learn.org/stable/user_guide.html)

---

## Part B: RAG Deep Dive

> You already built RAG. Now go deeper.

### Chunking Strategies

| Topic | Interview Questions | Status |
|-------|-------------------|--------|
| Fixed-size chunking | "What are the tradeoffs of chunking strategies?" | [ ] |
| Sentence chunking | "When would sentence chunking outperform fixed-size?" | [ ] |
| Semantic chunking | "What is semantic chunking?" | [ ] |
| Overlap | "Why add overlap between chunks?" | [ ] |

**Exercise:** The current RAG in `src/rag/retriever.py` indexes whole perfume records. What if descriptions were 5 paragraphs long? Explain to Claude what chunking strategy you'd use and why. No implementation needed yet.

---

### RAG Evaluation [INTERVIEW CRITICAL]

| Topic | Interview Questions | Status |
|-------|-------------------|--------|
| RAGAS framework | "How do you evaluate a RAG system?" | [ ] |
| Faithfulness | "What is faithfulness in RAG evaluation?" | [ ] |
| Answer relevancy | "What is answer relevancy?" | [ ] |
| Context precision/recall | "What are context precision and context recall?" | [ ] |

**Exercise:** Design (no code) a manual evaluation for PerfumeShop RAG:
- 10 test queries with expected perfumes
- Metric: did the retrieved perfumes include the expected one in top-5?
- Discuss with Claude: what other metrics matter for a recommender?

**Resources:** [RAGAS docs](https://docs.ragas.io/)

---

### Vector Stores (Hands-on) [INTERVIEW CRITICAL]

| Topic | Interview Questions | Status |
|-------|-------------------|--------|
| Vector store concept | "What is a vector store? How is it different from a regular DB?" | [ ] |
| Chroma | "What is ChromaDB? When would you use it?" | [ ] |
| Pinecone | "Pinecone vs Chroma — tradeoffs?" | [ ] |
| pgvector | "What is pgvector? When does it make sense?" | [ ] |
| OpenSearch vectors | "How does AWS OpenSearch handle vector search?" | [ ] |

**Exercise:** Replace the current `.npy` file + cosine similarity in `src/rag/retriever.py` with ChromaDB:
1. `pip install chromadb`
2. Create collection, add perfume embeddings
3. Query with `collection.query(query_embeddings=..., n_results=5)`
4. Compare results with current implementation

---

### Advanced Retrieval Techniques

| Topic | Interview Questions | Status |
|-------|-------------------|--------|
| Hybrid search | "What is hybrid search? How do you combine BM25 + semantic?" | [ ] |
| Re-ranking | "What is a re-ranker? When do you use one?" | [ ] |
| FAISS | "What is FAISS? What problem does it solve?" | [ ] |
| HyDE | "What is HyDE (Hypothetical Document Embeddings)?" | [ ] |

**Exercise (FAISS):** Replace cosine similarity loop in `src/rag/retriever.py` with FAISS:
```python
import faiss
index = faiss.IndexFlatIP(384)  # Inner product = cosine on normalized vectors
index.add(embeddings_matrix.astype('float32'))
D, I = index.search(query_embedding.reshape(1, -1).astype('float32'), k=5)
```
Measure speed difference. Explain why FAISS matters at scale.

---

## Part C: LLMs Advanced [INTERVIEW CRITICAL]

### Prompt Engineering

| Topic | Interview Questions | Status |
|-------|-------------------|--------|
| Zero-shot | "What is zero-shot prompting?" | [ ] |
| Few-shot | "What is few-shot prompting? Give an example." | [ ] |
| Chain-of-thought | "What is chain-of-thought prompting? When does it help?" | [ ] |
| ReAct | "What is the ReAct pattern?" | [ ] |
| System prompt | "Why does the system prompt matter in a RAG system?" | [ ] |

**Exercise:** The system prompt in `src/agents/orchestrator.py` is basic. Rewrite it using few-shot CoT: give Claude 2 examples of user query → thought process → tool calls → response. Test if recommendation quality improves.

---

### Parameter-Efficient Fine-Tuning

| Topic | Interview Questions | Status |
|-------|-------------------|--------|
| LoRA | "What is LoRA? How does it reduce compute cost?" | [ ] |
| QLoRA | "What is QLoRA? How does it differ from LoRA?" | [ ] |
| Adapters | "What are adapter layers?" | [ ] |
| When NOT to fine-tune | "When would you use RAG instead of fine-tuning?" | [ ] |

**Resources:** [LoRA paper summary](https://huggingface.co/docs/peft/conceptual_guides/lora)

---

### Agent Architectures [INTERVIEW CRITICAL]

| Topic | Interview Questions | Status |
|-------|-------------------|--------|
| Agent vs multiagent | "What is the difference between an agent and a multiagent system?" | [ ] |
| ReAct agent | "How does a ReAct agent work?" | [ ] |
| Human-in-the-loop | "What is human-in-the-loop in agent systems?" | [ ] |
| Multiple data sources | "Design an agent that queries SQL + vector store + API." | [ ] |

**Exercise:** Loopgate IS a human-in-the-loop system. Explain to Claude its architecture and where the "human gate" sits. Then contrast with PerfumeShop's fully automatic loop.

---

### Guardrails & Safety [INTERVIEW CRITICAL]

| Topic | Interview Questions | Status |
|-------|-------------------|--------|
| Guardrails in Bedrock | "What are guardrails in Amazon Bedrock?" | [ ] |
| Prompt injection | "What is prompt injection? How do you defend against it?" | [ ] |
| Output validation | "How do you validate LLM outputs in production?" | [ ] |

---

## Part D: Data Frameworks

### pandas Advanced

| Topic | Interview Questions | Status |
|-------|-------------------|--------|
| groupby | "How do you aggregate data by category in pandas?" | [ ] |
| merge/join | "When do you use merge vs join in pandas?" | [ ] |
| memory optimization | "How do you reduce pandas DataFrame memory usage?" | [ ] |
| vectorized ops | "Why avoid loops in pandas?" | [ ] |

**Exercise:** In `src/data/loader.py`, add a method `get_stats()` that returns:
- Number of perfumes per brand (groupby + count)
- Average rating per gender (groupby + mean, if column exists)
- Top 5 most common notes (str.split + explode + value_counts)

---

### Polars (conceptual)

| Topic | Interview Questions | Status |
|-------|-------------------|--------|
| polars vs pandas | "What is Polars? How is it different from pandas?" | [ ] |
| lazy evaluation | "What is lazy evaluation in Polars?" | [ ] |

**Exercise:** Rewrite `DataLoader.load_data()` using Polars. Compare: syntax differences, when would you choose one over the other?

---

### PySpark (conceptual only)

| Topic | Interview Questions | Status |
|-------|-------------------|--------|
| RDD vs DataFrame | "What is the difference between RDD and DataFrame in Spark?" | [ ] |
| transformations vs actions | "What is the difference between a transformation and an action in Spark?" | [ ] |
| when to use Spark | "When would you use Spark instead of pandas?" | [ ] |

**Resources:** [PySpark docs – RDD Programming Guide](https://spark.apache.org/docs/latest/rdd-programming-guide.html)

---

## Completion Criteria

- [ ] Can explain all Classical ML interview questions without notes (2 min each)
- [ ] Can calculate precision/recall/F1 from a confusion matrix on paper
- [ ] ChromaDB replacing `.npy` in `src/rag/retriever.py`
- [ ] FAISS implementation working in retriever
- [ ] `get_stats()` method in DataLoader
- [ ] Can explain LoRA in one minute without notes
- [ ] Can design a multiagent architecture for a new problem on a whiteboard
