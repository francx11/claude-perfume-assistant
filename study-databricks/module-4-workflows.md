# Module 4: Workflows + Orchestration

## Topics
- Databricks Jobs vs Airflow
- Tasks, clusters, schedules, dependencias
- `%run` vs `dbutils.notebook.run()`
- Job parameters + task values
- Retry, alerts, monitoring

---

## Concepts

### Databricks Jobs vs Airflow
| | Databricks Jobs | Airflow |
|---|---|---|
| Compute | Databricks clusters (nativo) | Ejecuta en workers externos |
| Code | Notebooks, Python scripts, JARs, dbt | DAGs en Python |
| Trigger | Schedule / REST API / File arrival | Schedule / REST API / sensors |
| Monitoring | Job UI + email/Slack alerts | Airflow UI + logs |
| Setup | Zero config en Databricks | Requiere infraestructura propia |
| Best for | Pipelines 100% en Databricks | Orquestación multi-sistema |

**Regla práctica:** si tu pipeline vive enteramente en Databricks → usa Jobs. Si mezcla Databricks + Redshift + APIs externas → considera Airflow/Prefect.

### Anatomía de un Databricks Job
```
Job
├── Task 1: Bronze ingestion (notebook o Python script)
│   ├── Cluster: Job cluster (ephemeral, barato)
│   └── Output: task value "processed_files=150"
├── Task 2: Silver transformation (depends_on: Task 1)
│   └── Input: task value from Task 1
├── Task 3a: Gold aggregation A (depends_on: Task 2)
├── Task 3b: Gold aggregation B (depends_on: Task 2)  ← parallel
└── Task 4: Notification (depends_on: Task 3a, Task 3b)
```

### `%run` vs `dbutils.notebook.run()`

```python
# %run — ejecuta notebook en el MISMO contexto (comparte variables, imports)
# Solo funciona en notebooks interactivos, NO en Jobs
%run ./utils/common_functions
# Ahora puedes usar funciones definidas en common_functions directamente

# dbutils.notebook.run() — ejecuta notebook en contexto SEPARADO
# Funciona en Jobs, puede pasar parámetros y recibir output
result = dbutils.notebook.run(
    "./pipelines/process_events",
    timeout_seconds=1800,
    arguments={"date": "2024-01-15", "env": "prod"}
)
# result es string — lo que retorna dbutils.notebook.exit("value")
```

**Cuándo usar cada uno:**
- `%run` → importar helpers/funciones compartidas en notebooks de desarrollo
- `dbutils.notebook.run()` → orquestar notebooks como tareas en un Job

### Task Values — pasar datos entre tareas
```python
# En Task 1 — guardar valor para tareas downstream
dbutils.jobs.taskValues.set(key="record_count", value=df.count())
dbutils.jobs.taskValues.set(key="status", value="SUCCESS")

# En Task 2 — leer valor de Task 1
record_count = dbutils.jobs.taskValues.get(taskKey="task_1", key="record_count")
print(f"Task 1 procesó {record_count} registros")
```

### Job parameters (vs task values)
```python
# Job parameters: definidos al crear el job, accesibles en todos los tasks
# Se pasan por widgets

dbutils.widgets.text("env", "dev")
dbutils.widgets.text("date", "2024-01-01")

env = dbutils.widgets.get("env")
date = dbutils.widgets.get("date")
```

### Cluster selection en Jobs
```python
# Job cluster (recomendado para producción)
# - Crea al inicio del job, termina al final
# - Sin costo cuando no corre
# - Config en el Job UI o API

# All-purpose cluster (solo dev)
# - Siempre encendido = costo continuo
# - Nunca usar en producción

# Shared cluster (múltiples jobs comparten)
# - Bueno para jobs cortos y frecuentes
# - Menos aislamiento
```

### Triggers
```yaml
# Cron schedule (en Job UI o via API)
schedule:
  quartz_cron_expression: "0 0 2 * * ?"   # 2am cada día
  timezone_id: "Europe/Madrid"

# File arrival trigger (requiere Auto Loader o configuración)
# Cuando llega archivo a S3 → ejecuta job

# REST API trigger (para integración externa)
POST /api/2.1/jobs/run-now
{
  "job_id": 123,
  "job_parameters": {"date": "2024-01-15"}
}
```

### Retry + alertas
```yaml
# En cada task se puede configurar:
max_retries: 3
retry_on_timeout: true
timeout_seconds: 3600

# Alertas (Job UI → Edit → Notifications)
on_failure: email | webhook (Slack)
on_success: email | webhook
on_start: email | webhook
```

---

## Exercises

### Exercise 1 — %run vs dbutils.notebook.run()
> Tienes un notebook `utils/spark_helpers.py` con funciones de transformación comunes.
> Tienes un Job con 3 tasks que todas necesitan esas funciones.
> 
> **¿Usarías `%run` o `dbutils.notebook.run()` para importar los helpers? ¿Por qué?**
> **¿Qué problema tiene `%run` en el contexto de un Job con tasks paralelas?**

### Exercise 2 — Diseño de Job
> Diseña un Databricks Job para este pipeline:
> - **Fuente:** archivos JSON en S3 (llegan cada hora)
> - **Bronze:** ingestar con Auto Loader → `catalog.bronze.events`
> - **Silver:** limpiar, deduplicar → `catalog.silver.events`
> - **Gold A:** agregar por día → `catalog.gold.daily_summary`
> - **Gold B:** top 10 productos → `catalog.gold.top_products`
> - **Notificación:** Slack si alguna task falla
>
> Dibuja (texto) la estructura de tasks, dependencias, y cluster type para cada task.

### Exercise 3 — Task values
> Task 1 de tu Job procesa archivos y hace `dbutils.jobs.taskValues.set(key="files_count", value=42)`.
> Task 2 depende de Task 1.
> 
> Escribe el código en Task 2 para:
> 1. Leer el valor de Task 1
> 2. Si `files_count == 0`, salir del notebook con mensaje "NO_DATA" sin fallar el job
> 3. Si `files_count > 0`, continuar procesamiento

### Exercise 4 — Cluster cost optimization
> Tu empresa tiene un Job que corre cada 5 minutos con datos muy pequeños (< 1MB).
> Actualmente usa un all-purpose cluster que cuesta $0.20/DBU.
> 
> **¿Qué cambiarías y por qué? ¿Qué trade-off tiene tu solución?**

### Exercise 5 — Retry strategy
> Tu pipeline llama a una API externa que falla 20% de las veces con timeout.
> El job tarda 45 minutos en total.
> 
> Configura la estrategia de retry: ¿max_retries? ¿timeout_seconds? ¿en qué task?

### Exercise 6 — Interview question
> "How do you handle dependencies between tasks in a Databricks Job?"
> Responde en 4-5 frases como en entrevista real.

---

## Key terms to memorize
- **Job cluster** — ephemeral, barato, muere al terminar el job
- **All-purpose cluster** — interactivo, caro en producción
- **`%run`** — mismo contexto, solo notebooks interactivos
- **`dbutils.notebook.run()`** — contexto separado, válido en Jobs
- **Task values** — `taskValues.set/get` para pasar datos entre tasks
- **Job parameters** — widgets accesibles desde todos los tasks
- **Trigger** — cron / file arrival / REST API
