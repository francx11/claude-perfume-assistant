# Progress Tracker

`[ ]` Not started · `[~]` In progress · `[x]` Mastered

Last updated: 2026-05-14

---

## Phase 1: Python Solid

### Data Structures
| Topic | Status | Notes |
|-------|--------|-------|
| list vs tuple | [x] | |
| set / frozenset | [x] | |
| dict internals + time complexity | [x] | |
| mutable default argument bug | [x] | Default created once at def-time; use None sentinel |

### Functions
| Topic | Status | Notes |
|-------|--------|-------|
| generator (yield) | [x] | yield pausa la función; Iterator[T] type hint; O(1) memoria vs O(n) lista |
| lambda expressions | [x] | lambda p: p["name"] — función anónima de una expresión; sin return explícito |
| decorators | [x] | @log_call = execute_tool = log_call(execute_tool); wrapper(*args,**kwargs) para ser genérico |
| `__init__.py` purpose | [x] | marca carpeta como paquete Python; puede estar vacío o re-exportar imports |

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
| PEP8 formal rules | [x] | espacios, comas, línea ≤120, snake_case, docstrings, type hints |
| ruff (linter/formatter) | [x] | ruff check --fix + ruff format; configurable en pyproject.toml |
| uv (package manager) | [x] | reemplaza pip+requirements.txt; prod vs dev deps en pyproject.toml |
| pre-commit hooks | [x] | .pre-commit-config.yaml; bloquea commit si ruff/interrogate fallan |
| interrogate (docstring coverage) | [x] | fail-under=80; ignore-init-method + ignore-magic |

### Architecture
| Topic | Status | Notes |
|-------|--------|-------|
| SRP | [x] | Una clase = una razón para cambiar; OrchestratorAgent viola SRP (prompt + tools + call) |
| OCP | [x] | Abierto para extensión, cerrado para modificación; match/case en execute_tool viola OCP → usar registry dict |
| LSP | [x] | Subclase debe sustituir al padre sin romper; Penguin(Bird) con fly() viola LSP → rediseñar jerarquía |
| ISP | [x] | Interfaces pequeñas; no forzar dependencia de métodos que no se usan |
| DIP | [x] | Inyectar dependencias desde fuera; OrchestratorAgent no debe instanciar ClaudeClient internamente |
| Strategy pattern | [x] | registry dict en execute_tool(); comportamientos intercambiables detrás de interfaz común |
| Factory pattern | [x] | startup_event() construye y conecta objetos; útil cuando construcción es compleja o tipo depende de config |
| Observer pattern | [x] | subject emite eventos, observers suscritos reciben notificación; WebSockets en Loopgate |
| Repository pattern | [x] | DataLoader oculta que datos vienen de CSV; si migras a PostgreSQL los endpoints no cambian |
| Dependency Injection | [x] | proveer dependencias desde fuera; facilita tests (Mock) y desacoplamiento; ver DIP |

### Production Python
| Topic | Status | Notes |
|-------|--------|-------|
| scalable logging (structlog / logging module) | [x] | getLogger(__name__) por módulo; basicConfig en startup; INFO/DEBUG/ERROR por volumen; structured con extra={} |
| error handling in distributed systems | [x] | retry+backoff, circuit breaker, idempotency key, DLQ |
| retry + exponential backoff | [x] | 2**intento + random.random(); RateLimitError en ClaudeClient |
| circuit breaker | [x] | CLOSED→OPEN→HALF_OPEN; max_fallos + tiempo_reset; clase separada (OCP) |
| data pipeline optimization (generators, chunking) | [x] | generator yield fila a fila → O(1) mem; pd.read_csv(chunksize=N) para batches; cProfile/line_profiler para bottlenecks |
| pytest coverage (`--cov`) | [x] | |
| property-based testing (hypothesis) | [x] | |

---

## Phase 2: AI Core

### Classical ML
| Topic | Status | Notes |
|-------|--------|-------|
| logistic regression | [x] | combinación lineal z → sigmoid → prob 0-1; visto sesión anterior |
| decision tree | [x] | splits sucesivos; profundidad → overfitting; weaknesses: memoriza ruido |
| random forest | [x] | bagging + feature randomness → decorrelación → voto mayoritario cancela errores |
| SVM + kernel trick | [x] | hiperplano máximo margen; support vectors; kernel proyecta a dim superior para datos no lineales |
| KNN | [x] | K vecinos más cercanos por distancia; sin entrenamiento; lento O(n) en predicción |
| multiclass model selection | [x] | tamaño dataset, cómputo, naturaleza datos (lineal/no-lineal), interpretabilidad |
| confusion matrix (TP/FP/FN/TN) | [x] | accuracy oculta rendimiento por clase; FP/FN tienen costes distintos según problema |
| precision / recall / F1 | [x] | precision=TP/(TP+FP); recall=TP/(TP+FN); F1=media armónica; recall↑ cuando FN es catastrófico |
| k-fold cross-validation | [x] | K splits, cada uno test una vez; métrica = media de K evals; K=5/10 estándar |
| overfitting + prevention | [x] | modelo memoriza ruido; señal: train↑ test↓; soluciones: regularización, early stopping, más datos, dropout |
| imbalanced data (SMOTE, class weights) | [x] | modelo predice mayoritaria siempre; soluciones: class_weight, SMOTE, undersampling; métrica: F1 no accuracy |
| learning rate + gradient descent | [x] | LR=tamaño paso; alta→oscila/diverge; baja→lento; GD=paso en dirección contraria al gradiente; riesgo mínimo local |
| fine-tuning (transfer learning) | [x] | partir de modelo preentrenado + entrenar con datos dominio; vs RAG: cuando conocimiento estático y dataset suficiente |
| PCA | [x] | nuevas columnas = combinaciones lineales de originales ordenadas por varianza; reducción de dimensionalidad manteniendo X% varianza |
| feature importance | [x] | permutation importance (barajar columna → medir caída); built-in RandomForest; SHAP para predicciones individuales |

### RAG Deep Dive
| Topic | Status | Notes |
|-------|--------|-------|
| chunking strategies | [x] | fixed-size corta contexto; sentence mejor; overlap evita pérdida en bordes; semantic más preciso pero costoso |
| RAG evaluation (RAGAS, faithfulness, relevancy) | [x] | 2 pilares: retrieval (context precision/recall) + generación (faithfulness/relevancy); LLM como juez; Hit Rate@5 para recommender |
| ChromaDB (hands-on) | [x] | collection.add(ids, embeddings, documents, metadatas); hnsw:space cosine; 1-distance=similarity; misma interfaz que RAGRetriever |
| FAISS (hands-on) | [x] | IndexFlatIP + normalize_L2 = cosine similarity exacta; id_map para mapear índice entero → perfume_id; más control que ChromaDB |
| hybrid search (BM25 + semantic) | [x] | BM25=léxico exacto; semántico=concepto; hybrid=α*BM25+(1-α)*semantic; gana en queries mixtas |
| re-ranking | [x] | bi-encoder rápido (stage 1, top-100) → cross-encoder preciso (stage 2, top-5); cross-encoder ve query+doc juntos |
| HyDE | [x] | Query→LLM→doc hipotético→embed→search; Decorator pattern; SRP: retriever no hace LLM calls |
| vector stores comparison (Chroma/Pinecone/pgvector/OpenSearch) | [x] | Chroma=dev/proto; Pinecone=cloud/escala; pgvector=ya tienes Postgres; OpenSearch=AWS+full-text |

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
| zero-shot prompting | [x] | sin ejemplos en el prompt |
| few-shot prompting | [x] | ejemplos de input→output en el prompt |
| chain-of-thought (CoT) | [x] | forzar razonamiento paso a paso; zero-shot="think step by step"; few-shot=ejemplos con razonamiento |
| ReAct pattern | [x] | Thought→Act→Observation explícito en output; trazabilidad de decisiones; OrchestratorAgent razona internamente pero no expone Thoughts |
| LoRA | [x] | ΔW=A×B rango bajo; suma paralela a W; merge en inferencia → cero latencia; aplica a Q,K,V |
| QLoRA | [x] | LoRA + modelo base 4-bit NF4; A,B en bfloat16; ~8x menos memoria; peft+bitsandbytes |
| adapter layers | [x] | capas down(D→r)+up(r→D) insertadas entre capas transformer; preserva dimensiones; latencia extra en inferencia |
| agent vs multiagent | [x] | único=dominio simple; multi=especialización+paralelismo; patrones: orchestrator-worker, pipeline, peer-to-peer |
| ReAct (deep) | [x] | Thought→Act→Observation explícito; trazabilidad; insertar HITL antes de actions irreversibles |
| human-in-the-loop | [x] | patrón agentic: Approval(antes), Validation(después), Correction(escalado); no usar en tiempo real/volumen masivo/acciones reversibles |
| guardrails in Bedrock | [x] | servicio AWS que intercepta input/output del LLM; 4 categorías: harmful content, topic filter, PII, grounding; externo al modelo |
| prompt injection defense | [x] | direct (usuario) vs indirect (RAG/docs); defensas: roles separados, input validation, least privilege, guardrails, output validation |

### Data Frameworks
| Topic | Status | Notes |
|-------|--------|-------|
| pandas groupby / merge / pivot | [x] | groupby+agg, merge(on=key, how=inner/left/outer), pivot(index,columns,values) |
| pandas memory optimization | [x] | category para strings repetidos; downcast numérico; chunksize para CSVs grandes |
| polars vs pandas | [x] | Polars=Rust+multi-thread+lazy; pandas=single-thread+eager; Polars 5-100x más rápido en >1GB |
| polars lazy evaluation | [x] | scan_csv→filter→select→collect(); planifica antes de ejecutar; query optimizer reduce RAM y I/O |
| PySpark RDD vs DataFrame | [x] | RDD=sin esquema+lento; DataFrame=esquema+Catalyst optimizer+rápido; usar DataFrame siempre que puedas |
| PySpark transformations vs actions | [x] | transformation=lazy(filter,select,groupBy); action=ejecuta plan(collect,show,count,write); igual que Polars lazy |

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
| LCEL (pipe syntax) | [x] | pipe \| conecta Runnables; composabilidad vs llamadas anidadas |
| Runnable interface | [x] | interfaz común .invoke(); BaseRetriever/ChatModel/parsers la implementan |
| PromptTemplate | [x] | ChatPromptTemplate.from_messages(); separa estructura de valores |
| Output parsers | [x] | StrOutputParser/JsonOutputParser al final del pipe; equivale a json.loads() manual |
| BaseRetriever | [x] | hereda + implementa _get_relevant_documents(); Runnable gratis |
| VectorStoreRetriever | [x] | BaseRetriever pre-implementado; vectorstore.as_retriever() |
| create_retrieval_chain | [x] | retriever → contexto → prompt → LLM; always-on RAG vs tool-use RAG |
| Contextual compression | [x] | LLMChainExtractor reduce docs a parte relevante; tradeoff: LLM extra por retrieval |
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
