# Progress Tracker

`[ ]` Not started · `[~]` In progress · `[x]` Mastered

Last updated: 2026-05-25 (Phase 5 completo: Docker, K8s, GitHub Actions, Terraform, FastAPI+WebSockets)

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
| RunnableWithMessageHistory | [x] | wrapper que inyecta BaseChatMessageHistory por session_id; add_message() abstrae backend (RAM/Redis/Postgres) |
| LangGraph StateGraph | [x] | TypedDict state compartido entre nodos; graph = nodos + aristas compilados |
| LangGraph nodes + edges | [x] | nodos=funciones(state→state); arista normal=fija; condicional=función retorna nombre nodo |
| LangGraph conditional routing | [x] | should_continue() retorna string→nodo; add_conditional_edges() mapea; equivale a while loop manual |
| LangGraph human-in-the-loop | [x] | interrupt_before=["node"]; checkpoint guarda estado; resume con invoke(None, config=thread_id) |
| LangGraph persistence | [x] | checkpointer obligatorio para HITL; sin él ValueError; SqliteSaver/PostgresSaver |
| LangSmith tracing | [x] | LANGCHAIN_TRACING_V2=true; auto-traza nodos/tools/tokens; filtro por fecha+session |
| LangSmith evaluation datasets | [x] | colección input→output esperado para regression testing |
| LLM-as-judge evaluation | [x] | LLM califica respuestas de otro LLM con rubrica; riesgo: self-serving bias |
| Langfuse tracing | [x] | @observe() decorator en cualquier función Python; agnóstico de framework |
| Langfuse vs LangSmith | [x] | LangSmith=auto LangChain only; Langfuse=manual @observe() + self-hosted + cualquier stack |
| Strands Agent tool definition | [x] | @tool decorator extrae nombre/desc/tipos de fn+docstring+type hints via inspect; cero JSON manual |
| Strands + Bedrock integration | [x] | Agent(tools=[...]) abstrae loop; nativo Bedrock pero soporta otros providers |

---

## Phase 4: AWS

### Already Known
| Topic | Status | Notes |
|-------|--------|-------|
| FastAPI basics | [x] | Day 5, 6 |
| async/await | [x] | Day 5 |
| WebSockets (Loopgate) | [x] | Built but no notes |

### boto3 + Core Services
| Topic | Status | Notes |
|-------|--------|-------|
| boto3 client vs resource | [x] | |
| session + credential management | [x] | |
| boto3 error handling (ClientError) | [x] | |
| boto3 paginator | [x] | |
| S3 CRUD (upload/download/delete) | [x] | |
| S3 presigned URLs | [x] | |
| S3 event notifications | [x] | |
| S3 storage classes | [x] | |
| S3 versioning | [x] | |
| Lambda handler + signature | [x] | |
| Lambda layers | [x] | |
| Lambda cold start | [x] | |
| Lambda packaging dependencies | [x] | |
| Lambda environment variables | [x] | |
| Lambda timeout / memory limits | [x] | |
| Bedrock Converse API | [x] | schema unificado multi-modelo; content=[{"text":""}]; inferenceConfig; system=[{"text":""}]; response["output"]["message"]["content"][0]["text"] |
| Bedrock InvokeModel | [x] | model-specific params (extended thinking, top_k); usar cuando Converse no expone feature necesario |
| Bedrock Knowledge Bases | [x] | pipeline RAG gestionado: ingesta S3 + chunking + embeddings + vector store; retrieve() via bedrock-agent-runtime |
| Bedrock AgentCore | [x] | runtime gestionado para agentes en producción: sesiones aisladas, concurrencia, memoria persistente; tools=Lambda Action Groups |
| Bedrock Guardrails | [x] | ya dominado en Phase 2: intercepta input/output; harmful content, topic filter, PII, grounding |
| DynamoDB partition key + sort key | [x] | PK=hash→servidor físico; SK=orden dentro del partition; SK debe ser timestamp no UUID para orden cronológico |
| DynamoDB query vs scan | [x] | query=PK obligatorio→eficiente O(log n); scan=toca todos los servidores→caro; ScanIndexForward=False+Limit para más reciente |
| DynamoDB GSI | [x] | índice alternativo con diferente PK/SK; replica datos internamente; usar cuando query frecuente por atributo no-PK |
| DynamoDB single-table design | [x] | sin joins→múltiples tablas=múltiples round trips; co-localizar entidades relacionadas bajo mismo PK con prefijos en SK |
| Textract DetectDocumentText | [x] | texto plano=bloques LINE/WORD; equivalente a Tesseract sin preprocesado manual; Document=Bytes o S3Object |
| Textract AnalyzeDocument | [x] | FeatureTypes=["FORMS","TABLES"]; extrae key-value pairs y celdas de tabla; más caro que DetectDocumentText |
| Textract quality issues | [x] | |
| Textract vs Tesseract | [x] | |
| SageMaker (conceptual) | [x] | |
| Athena (conceptual) | [x] | |
| OpenSearch vector search (conceptual) | [x] | |
| EKS (conceptual) | [x] | |
| EC2 (conceptual) | [x] | |

---

## Databricks

### Module 1: Architecture & Core Concepts
| Topic | Status | Notes |
|-------|--------|-------|
| Data Lake vs Data Warehouse vs Lakehouse | [x] | Lakehouse = almacenamiento barato + ACID + soporte ML nativo |
| Delta Lake | [x] | Capa transaccional sobre Parquet en S3; `_delta_log/` actúa como WAL; resuelve escrituras concurrentes |
| Parquet (columnar format) | [x] | Columnar vs fila-a-fila; compresión superior; estadísticas por bloque para skip de datos |
| ACID (definición y letras) | [x] | A=Atomicidad, C=Consistencia, I=Aislamiento (escrituras concurrentes), D=Durabilidad |
| Unity Catalog | [x] | Gobernanza centralizada; namespace 3 niveles catalog.schema.table; reemplaza Hive Metastore por workspace |
| Tipos de cluster | [x] | All-purpose=dev interactivo; Job=ephemeral producción (más barato); SQL Warehouse=BI/SQL únicamente |

### Module 2: Delta Lake Deep Dive
| Topic | Status | Notes |
|-------|--------|-------|
| Transaction log (atomicity mechanism) | [x] | Parquet files primero → JSON log entry al final; log entry = commit; sin log = orphan files invisibles a lectores |
| Time Travel | [x] | `versionAsOf` / `timestampAsOf`; `dt.history().show()`; restore = read histórico + write overwrite |
| MERGE INTO (upsert) | [x] | whenMatchedUpdate + whenNotMatchedInsert; omitir whenNotMatchedBySourceDelete para no borrar ausentes |
| Partitioning | [x] | baja cardinalidad + frecuente en WHERE + >1GB por partición; anti-pattern: alta cardinalidad (user_id) |
| Z-ordering | [x] | clustering a nivel de archivo, no carpeta; ideal alta cardinalidad (product_id); `OPTIMIZE ... ZORDER BY` |
| OPTIMIZE + VACUUM | [x] | OPTIMIZE compacta small files; VACUUM borra orphan Parquet; RETAIN 0 mata time travel + puede romper lectores activos |

### Module 3: PySpark en Databricks
| Topic | Status | Notes |
|-------|--------|-------|
| PySpark vs pandas (cuándo usar cada uno) | [x] | pandas <1GB una máquina; PySpark >1GB distribuido; overhead coordinar workers no vale para datos pequeños |
| SparkSession en Databricks | [x] | `spark` ya existe globalmente; no necesitas crear SparkSession en Databricks |
| DataFrame read (3 formas) | [x] | `spark.table()` Unity Catalog+governance; `.load(path)` acceso S3 directo; `spark.sql()` queries complejas/SQL |
| Transformations comunes | [x] | filter, withColumn, drop, dropDuplicates, withColumnRenamed; todas lazy |
| Window functions | [x] | `partitionBy + orderBy + row_number().over(window)` → filtrar row_num==1; no confundir con groupBy que colapsa filas |
| Write modes (overwrite/append/merge) | [x] | overwrite=full refresh; append=additive sin duplicados; merge=CDC/upsert idempotente |
| dbutils.secrets | [x] | `dbutils.secrets.get(scope, key)`; nunca hardcodear credenciales en notebooks |
| dbutils.fs / widgets / notebook | [x] | ls/cp/rm/mkdirs; widgets para params interactivos; notebook.run() para orquestar |
| Auto Loader | [x] | `format("cloudFiles")`; detecta archivos nuevos S3/ADLS sin listar todo el bucket |
| Checkpoint (Auto Loader) | [x] | registra archivos procesados → idempotente; si borras: reprocesa todo desde cero |
| trigger(availableNow=True) | [x] | procesa todos los pendientes y para → job nocturno; vs processingTime=streaming continuo |
| Medallion Architecture | [x] | Bronze=raw inmutable append-only; Silver=clean+validado+dedup; Gold=agregado business-ready; reprocessar desde Bronze si hay bug |

### Module 4: Workflows + Orchestration
| Topic | Status | Notes |
|-------|--------|-------|
| Databricks Jobs vs Airflow | [x] | Jobs=100% Databricks; Airflow=multi-sistema externo |
| Job anatomy (tasks + dependencias) | [x] | depends_on define orden; tasks paralelas cuando comparten upstream |
| `%run` vs `dbutils.notebook.run()` | [x] | %run=mismo contexto, solo notebooks interactivos; dbutils=proceso separado, válido en Jobs, solo retorna string |
| Task Values (set/get) | [x] | `taskValues.set(key, value)` upstream; `taskValues.get(taskKey, key)` downstream |
| Job parameters (widgets) | [x] | `dbutils.widgets.text/get`; accesibles desde todos los tasks |
| Job cluster vs All-purpose cluster | [x] | Job=ephemeral, muere al terminar, producción; All-purpose=siempre encendido, solo dev |
| Shared cluster | [x] | múltiples jobs comparten; bueno para jobs cortos y frecuentes; menos aislamiento |
| Triggers (cron / file arrival / REST API) | [x] | cron=horario fijo; file arrival=S3 event; REST API=sistema externo dispara |
| Retry + alertas | [x] | max_retries=3 suficiente para 20% fallo; timeout_seconds por task; alerts email/Slack on_failure |

### Module 6: Databricks SQL + Lakehouse
| Topic | Status | Notes |
|-------|--------|-------|
| SQL Warehouse vs All-purpose cluster | [x] | SQL Warehouse=JDBC/ODBC+Photon+BI tools; All-purpose=PySpark+ML+notebooks |
| Photon engine | [x] | C++ vectorized engine; hasta 12x más rápido que Spark JVM para SQL puro |
| Managed vs External tables | [x] | Managed=DROP borra datos; External=DROP solo borra metadata; Bronze=External, Silver/Gold=Managed |
| Dynamic partition overwrite | [x] | spark.sql.sources.partitionOverwriteMode=dynamic; solo toca particiones presentes en datos nuevos |
| Delta Live Tables (DLT) | [x] | @dlt.table declarativo; DLT infiere orden desde dlt.read(); vs Jobs=imperativo manual |
| DLT expectations | [x] | expect=log; expect_or_drop=elimina fila; expect_or_fail=para pipeline; quarantine=tabla separada |
| Unity Catalog permissions | [x] | GRANT SELECT/MODIFY/CREATE TABLE ON CATALOG/SCHEMA/TABLE; herencia hacia abajo; sin GRANT especial para SQL Warehouse |

### Module 5: MLflow en Databricks
| Topic | Status | Notes |
|-------|--------|-------|
| Experiment tracking (log_param/metric/artifact/model) | [x] | log_param=hiperparámetros fijos; log_metric=resultados evaluables (soporta step=); log_artifact=archivos; log_model=modelo serializado |
| autolog vs logging manual | [x] | autolog captura todo lo interno de sklearn; manual para artefactos custom y métricas de negocio |
| MLflow Model Registry (stages) | [x] | None→Staging→Production→Archived; transition_model_version_stage(); solo un modelo por stage |
| Model Registry aliases | [x] | @champion/@challenger en MLflow>=2.0; permite múltiples modelos activos simultáneos → A/B testing; mejor que stages |
| Cargar modelo desde Registry | [x] | `mlflow.sklearn.load_model("models:/PerfumeClassifier@champion")` |
| spark_udf para scoring masivo | [x] | `mlflow.pyfunc.spark_udf(spark, model_uri)`; distribuye predicciones en workers; evita .toPandas() + RAM overflow |
| Training-serving skew | [x] | features calculadas distinto en training vs producción → predicciones silenciosamente malas |
| Feature Store | [x] | features calculadas una vez, reutilizadas en training y producción; elimina training-serving skew |

---

## Phase 5: Plus

| Topic | Status | Notes |
|-------|--------|-------|
| Dockerfile (key instructions) | [x] | FROM/COPY/RUN/EXPOSE/CMD/WORKDIR/AS; orden capas menos→más frecuente |
| multi-stage builds | [x] | AS base/deps/final; imagen final sin herramientas de build; reduce tamaño |
| Docker image layers | [x] | cada instrucción=capa; cache invalida en cascada; limpiar en mismo RUN |
| docker-compose | [x] | orquesta multi-servicio; build/ports/volumes/env_file; un solo comando |
| .dockerignore | [x] | excluye .env, embeddings, __pycache__, prueba*.py de COPY . . |
| K8s Pod | [x] | unidad mínima; 1+ contenedores comparten red+filesystem; patrón sidecar |
| K8s Deployment | [x] | gestiona réplicas; reinicia pods fallidos; rolling updates sin downtime |
| K8s Service (types) | [x] | ClusterIP=interno; NodePort=nodo; LoadBalancer=AWS ELB; IP estable + LB |
| K8s Ingress | [x] | un ELB para todos los servicios; enruta por URL; TLS/HTTPS |
| K8s ConfigMap / Secret | [x] | ConfigMap=config no sensible; Secret=credenciales base64 |
| K8s HPA | [x] | escala pods automáticamente por CPU/memoria/requests; horizontal=más pods |
| GitHub Actions workflow syntax | [x] | .github/workflows/*.yml; YAML; name/on/jobs/steps |
| GitHub Actions jobs + steps | [x] | job=VM propia; steps=secuenciales en misma VM; jobs paralelos por defecto |
| GitHub Actions triggers | [x] | push, pull_request, schedule (cron), workflow_dispatch |
| GitHub Actions secrets | [x] | Settings→Secrets; ${{ secrets.NAME }}; nunca hardcodear en YAML |
| GitHub Actions caching | [x] | actions/cache@v4; key=hash(requirements.txt); evita reinstalar deps |
| GitHub Actions matrix builds | [x] | matrix strategy; un job por combinación; corren en paralelo |
| Terraform HCL syntax | [x] | terraform/provider/resource/data/variable/output/locals; ref: tipo.nombre.attr |
| Terraform state file | [x] | mapa HCL↔AWS real; perderlo = caos; siempre backend S3 remoto |
| Terraform plan / apply | [x] | plan=dry-run diff; apply=ejecuta cambios reales; siempre plan antes |
| Terraform modules | [x] | carpeta con .tf reutilizable; encapsula recursos relacionados |
| Terraform AWS provider | [x] | region + credenciales; nunca hardcodear; IAM roles o env vars |

### FastAPI Advanced + WebSockets
| Topic | Status | Notes |
|-------|--------|-------|
| WebSockets in FastAPI | [x] | conexión bidireccional persistente; HTTP no sirve para push del servidor |
| connection manager (multi-WS) | [x] | lista de WebSockets activos; broadcast a todos; add/remove en connect/disconnect |
| FastAPI BackgroundTasks | [x] | responde inmediatamente; tarea pesada corre después; add_task(fn, args) |
| FastAPI middleware | [x] | intercepta todas requests/responses; logging, auth, CORS, security headers |

---

## Phase 6: Interview Simulation

| Activity | Status | Score | Notes |
|----------|--------|-------|-------|
| Mock interview #1 (basic) | [x] | 2.55/5 | Python 2.4 · ML 2.75 · AI General 2.5 — conceptos OK, faltan código+proyecto en respuestas |
| Mock interview #2 (intermediate) | [ ] | — | |
| Mock interview #3 (full, 45 min) | [ ] | — | |
| All basic questions ≥4/5 | [ ] | — | Repetir básicas antes de mock #3 |
| All intermediate questions ≥3.5/5 | [ ] | — | |
| All advanced questions ≥3/5 | [ ] | — | |
