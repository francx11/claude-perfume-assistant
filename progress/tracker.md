# Progress Tracker

`[ ]` Not started · `[~]` In progress · `[x]` Mastered

Last updated: 2026-05-05

---

## Phase 1: Python Solid

### Data Structures
| Topic | Status | Notes |
|-------|--------|-------|
| list vs tuple | [ ] | |
| set / frozenset | [ ] | |
| dict internals + time complexity | [ ] | |
| mutable default argument bug | [x] | Default created once at def-time; use None sentinel |

### Functions
| Topic | Status | Notes |
|-------|--------|-------|
| generator (yield) | [ ] | |
| lambda expressions | [ ] | |
| decorators | [ ] | |
| `__init__.py` purpose | [ ] | |

### Already Known (from days 1–11)
| Topic | Status | Notes |
|-------|--------|-------|
| instance attributes / `self` | [x] | Day 1 |
| None checks (`is not None`) | [x] | Day 1 |
| dynamic kwargs `**{k:v}` | [x] | Day 1, 6 |
| dict/list comprehension | [x] | Day 4 |
| `match/case` | [x] | Day 4 |
| `**dict` unpacking | [x] | Day 4 |
| `next()` with generator expr | [x] | Day 6 |
| `enumerate()` | [x] | Day 7 |
| multiline strings | [x] | Day 6 |
| import conventions (PEP8) | [x] | Day 11 |
| virtual environment | [x] | Day 1 |
| `python-dotenv` / `.env` | [x] | Day 1 |

### Tooling
| Topic | Status | Notes |
|-------|--------|-------|
| PEP8 formal rules | [ ] | |
| ruff (linter/formatter) | [ ] | |
| uv (package manager) | [ ] | |
| pre-commit hooks | [ ] | |
| interrogate (docstring coverage) | [ ] | |

### Architecture
| Topic | Status | Notes |
|-------|--------|-------|
| SRP | [ ] | |
| OCP | [ ] | |
| LSP | [ ] | |
| ISP | [ ] | |
| DIP | [ ] | |
| Strategy pattern | [ ] | |
| Factory pattern | [ ] | |
| Observer pattern | [ ] | |
| Repository pattern | [ ] | |
| Dependency Injection | [ ] | |

### Production Python
| Topic | Status | Notes |
|-------|--------|-------|
| scalable logging (structlog / logging module) | [ ] | |
| error handling in distributed systems | [ ] | |
| retry + exponential backoff | [ ] | |
| circuit breaker | [ ] | |
| data pipeline optimization (generators, chunking) | [ ] | |
| pytest coverage (`--cov`) | [ ] | |
| property-based testing (hypothesis) | [ ] | |

---

## Phase 2: AI Core

### Classical ML
| Topic | Status | Notes |
|-------|--------|-------|
| logistic regression | [ ] | |
| decision tree | [ ] | |
| random forest | [ ] | |
| SVM + kernel trick | [ ] | |
| KNN | [ ] | |
| multiclass model selection | [ ] | |
| confusion matrix (TP/FP/FN/TN) | [ ] | |
| precision / recall / F1 | [ ] | |
| k-fold cross-validation | [ ] | |
| overfitting + prevention | [ ] | |
| imbalanced data (SMOTE, class weights) | [ ] | |
| learning rate + gradient descent | [ ] | |
| fine-tuning (transfer learning) | [ ] | |
| PCA | [ ] | |
| feature importance | [ ] | |

### RAG Deep Dive
| Topic | Status | Notes |
|-------|--------|-------|
| chunking strategies | [ ] | |
| RAG evaluation (RAGAS, faithfulness, relevancy) | [ ] | |
| ChromaDB (hands-on) | [ ] | |
| FAISS (hands-on) | [ ] | |
| hybrid search (BM25 + semantic) | [ ] | |
| re-ranking | [ ] | |
| HyDE | [ ] | |
| vector stores comparison (Chroma/Pinecone/pgvector/OpenSearch) | [ ] | |

### Already Known (from days 1–11)
| Topic | Status | Notes |
|-------|--------|-------|
| embedding concept | [x] | Day 1, 7 |
| RAG concept + flow | [x] | Day 1, 7 |
| RAG vs fine-tuning | [x] | Day 1, 7 |
| cosine similarity (formula + impl) | [x] | Day 7 |
| sentence-transformers (all-MiniLM-L6-v2) | [x] | Day 7 |
| O(n) search problem + FAISS/HNSW conceptual | [x] | Day 7 |
| vector databases (conceptual: Pinecone, Chroma, pgvector) | [x] | Day 7 |
| tool use / function calling | [x] | Day 4 |
| JSON Schema for tools | [x] | Day 4 |
| orchestrator pattern | [x] | Day 6 |
| tool_use loop (max 5 iter) | [x] | Day 6 |
| multiple tool_use blocks per turn | [x] | Day 6 |
| OCR (pytesseract + PIL pipeline) | [x] | Day 11 |

### LLMs Advanced
| Topic | Status | Notes |
|-------|--------|-------|
| zero-shot prompting | [ ] | |
| few-shot prompting | [ ] | |
| chain-of-thought (CoT) | [ ] | |
| ReAct pattern | [ ] | |
| LoRA | [ ] | |
| QLoRA | [ ] | |
| adapter layers | [ ] | |
| agent vs multiagent | [ ] | |
| guardrails in Bedrock | [ ] | |
| prompt injection defense | [ ] | |

### Data Frameworks
| Topic | Status | Notes |
|-------|--------|-------|
| pandas groupby / merge / pivot | [ ] | |
| pandas memory optimization | [ ] | |
| polars vs pandas | [ ] | |
| polars lazy evaluation | [ ] | |
| PySpark RDD vs DataFrame | [ ] | |
| PySpark transformations vs actions | [ ] | |

### Already Known — Pandas (from days 1–11)
| Topic | Status | Notes |
|-------|--------|-------|
| read_csv, dropna, drop_duplicates | [x] | Day 3 |
| str.strip / str.lower / str.contains | [x] | Day 3 |
| set_index / df.loc | [x] | Day 3 |
| to_dict('records') | [x] | Day 3 |
| df.isin / filter patterns | [x] | Day 3 |
| reset_index() | [x] | Day 7 |
| NumPy (dot, linalg.norm, array ops) | [x] | Day 7 |

---

## Phase 3: LangChain Ecosystem + Strands

| Topic | Status | Notes |
|-------|--------|-------|
| LCEL (pipe syntax) | [ ] | |
| PromptTemplate | [ ] | |
| Output parsers | [ ] | |
| VectorStoreRetriever | [ ] | |
| create_retrieval_chain | [ ] | |
| RunnableWithMessageHistory | [ ] | |
| LangGraph StateGraph | [ ] | |
| LangGraph nodes + edges | [ ] | |
| LangGraph conditional routing | [ ] | |
| LangGraph human-in-the-loop | [ ] | |
| LangGraph persistence | [ ] | |
| LangSmith tracing | [ ] | |
| LangSmith evaluation datasets | [ ] | |
| LLM-as-judge evaluation | [ ] | |
| Langfuse tracing | [ ] | |
| Langfuse vs LangSmith | [ ] | |
| Strands Agent tool definition | [ ] | |
| Strands + Bedrock integration | [ ] | |

---

## Phase 4: AWS

### Already Known
| Topic | Status | Notes |
|-------|--------|-------|
| FastAPI basics | [x] | Day 5, 6 |
| async/await | [x] | Day 5 |
| WebSockets (Loopgate) | [~] | Built but no notes |

### boto3 + Core Services
| Topic | Status | Notes |
|-------|--------|-------|
| boto3 client vs resource | [ ] | |
| session + credential management | [ ] | |
| boto3 error handling (ClientError) | [ ] | |
| S3 CRUD (upload/download/delete) | [ ] | |
| S3 presigned URLs | [ ] | |
| Lambda handler + signature | [ ] | |
| Lambda layers | [ ] | |
| Lambda cold start | [ ] | |
| Lambda packaging dependencies | [ ] | |
| Bedrock Converse API | [ ] | |
| Bedrock InvokeModel | [ ] | |
| Bedrock Knowledge Bases | [ ] | |
| Bedrock AgentCore | [ ] | |
| Bedrock Guardrails | [ ] | |
| DynamoDB partition key + sort key | [ ] | |
| DynamoDB query vs scan | [ ] | |
| DynamoDB GSI | [ ] | |
| DynamoDB single-table design | [ ] | |
| Textract DetectDocumentText | [ ] | |
| Textract AnalyzeDocument | [ ] | |
| SageMaker (conceptual) | [ ] | |
| Athena (conceptual) | [ ] | |
| OpenSearch vector search (conceptual) | [ ] | |
| EKS (conceptual) | [ ] | |

---

## Phase 5: Plus

| Topic | Status | Notes |
|-------|--------|-------|
| Dockerfile (key instructions) | [ ] | |
| multi-stage builds | [ ] | |
| Docker image layers | [ ] | |
| docker-compose | [ ] | |
| K8s Pod | [ ] | |
| K8s Deployment | [ ] | |
| K8s Service (types) | [ ] | |
| K8s Ingress | [ ] | |
| K8s ConfigMap / Secret | [ ] | |
| K8s HPA | [ ] | |
| GitHub Actions workflow syntax | [ ] | |
| GitHub Actions jobs + steps | [ ] | |
| GitHub Actions secrets | [ ] | |
| GitHub Actions caching | [ ] | |
| Terraform HCL syntax | [ ] | |
| Terraform state file | [ ] | |
| Terraform plan / apply | [ ] | |
| Terraform AWS provider | [ ] | |

---

## Phase 6: Interview Simulation

| Activity | Status | Score | Notes |
|----------|--------|-------|-------|
| Mock interview #1 (basic) | [ ] | — | |
| Mock interview #2 (intermediate) | [ ] | — | |
| Mock interview #3 (full, 45 min) | [ ] | — | |
| All basic questions ≥4/5 | [ ] | — | |
| All intermediate questions ≥3.5/5 | [ ] | — | |
| All advanced questions ≥3/5 | [ ] | — | |
