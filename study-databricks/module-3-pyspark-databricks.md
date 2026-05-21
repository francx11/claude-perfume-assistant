# Module 3: PySpark en Databricks

## Topics
- SparkSession en Databricks (ya viene configurada)
- DataFrames, transformations, actions — repaso orientado a proyecto
- `dbutils` — utilidades nativas Databricks
- Auto Loader — ingesta incremental desde S3/ADLS
- Secrets management con `dbutils.secrets`

---

## Concepts

### SparkSession en Databricks
```python
# En Databricks NO necesitas crear SparkSession — ya existe como `spark`
spark.version  # ver versión de Spark

# En local/testing sí la creas:
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("test").getOrCreate()
```

### DataFrame operations — patterns de proyecto real

```python
from pyspark.sql import functions as F
from pyspark.sql.types import StructType, StructField, StringType, LongType, TimestampType

# Read Delta table (3 formas)
df = spark.table("catalog.schema.table")                          # Unity Catalog
df = spark.read.format("delta").load("s3://bucket/path")         # path directo
df = spark.sql("SELECT * FROM catalog.schema.table WHERE ...")    # SQL

# Transformations comunes en proyectos
df = (df
    .filter(F.col("status") == "active")
    .withColumn("full_name", F.concat(F.col("first"), F.lit(" "), F.col("last")))
    .withColumn("created_date", F.to_date(F.col("created_at")))
    .withColumn("year", F.year(F.col("created_at")))
    .withColumn("month", F.month(F.col("created_at")))
    .drop("raw_column")
    .dropDuplicates(["id"])
    .withColumnRenamed("old_name", "new_name")
)

# Window functions — muy usadas en proyectos
from pyspark.sql.window import Window

window = Window.partitionBy("customer_id").orderBy(F.desc("created_at"))
df = df.withColumn("row_num", F.row_number().over(window))
latest_per_customer = df.filter(F.col("row_num") == 1)

# Write a Delta table
(df.write
    .format("delta")
    .mode("overwrite")            # overwrite | append | ignore | error
    .option("overwriteSchema", "true")
    .partitionBy("year", "month")
    .saveAsTable("catalog.schema.table")   # Unity Catalog managed table
)

# Write con MERGE (ver Module 2)
```

### Modo overwrite vs append vs merge
| Mode | Use | Risk |
|------|-----|------|
| `overwrite` | Full refresh, small tables | Loses history (but Delta keeps versions) |
| `append` | Streaming, additive data | Duplicates if job retried |
| `merge` | CDC, upsert, idempotent | More code, slower than append |

### `dbutils` — utilidades clave
```python
# File system (DBFS + cloud storage)
dbutils.fs.ls("s3://my-bucket/data/")       # list files
dbutils.fs.cp("s3://src/", "s3://dst/", recurse=True)
dbutils.fs.rm("s3://bucket/path/", recurse=True)
dbutils.fs.mkdirs("s3://bucket/new-folder/")

# Ejecutar otro notebook y pasar parámetros
result = dbutils.notebook.run("./utils/helper_notebook", timeout_seconds=600,
                               arguments={"env": "prod", "date": "2024-01-15"})

# Widgets — parámetros interactivos en notebooks
dbutils.widgets.text("date", "2024-01-01", "Processing date")
processing_date = dbutils.widgets.get("date")

# Secrets — NUNCA hardcodear credenciales
api_key = dbutils.secrets.get(scope="my-scope", key="openai-api-key")
db_password = dbutils.secrets.get(scope="prod-secrets", key="postgres-password")

# Salir de notebook y retornar valor (para Jobs)
dbutils.notebook.exit("SUCCESS")
```

### Auto Loader — ingesta incremental
Auto Loader detecta archivos nuevos automáticamente sin necesidad de listar todo el bucket.

```python
# Ingesta incremental de S3 → Delta table
checkpoint_path = "s3://bucket/_checkpoints/raw_events"

df_stream = (spark.readStream
    .format("cloudFiles")                          # Auto Loader
    .option("cloudFiles.format", "json")           # json | csv | parquet | avro
    .option("cloudFiles.schemaLocation", checkpoint_path + "/schema")
    .option("cloudFiles.inferColumnTypes", "true")
    .load("s3://bucket/raw/events/")
)

# Añadir metadata del archivo
df_stream = df_stream.withColumn("_input_file", F.input_file_name())
df_stream = df_stream.withColumn("_ingested_at", F.current_timestamp())

# Escribir a Delta (streaming write)
(df_stream.writeStream
    .format("delta")
    .option("checkpointLocation", checkpoint_path)
    .option("mergeSchema", "true")
    .trigger(availableNow=True)     # procesa todos los archivos nuevos y para (batch mode)
    # .trigger(processingTime="10 minutes")  # streaming continuo
    .toTable("catalog.bronze.raw_events")
)
```

**Checkpoint** = registro de qué archivos ya fueron procesados → idempotente, no reprocesa

### Medallion Architecture (patrón estándar de proyecto)
```
Bronze → Silver → Gold

Bronze: raw data, sin transformar, append-only (Auto Loader)
Silver: cleaned, validated, deduplicated (MERGE o overwrite)
Gold:   aggregated, business-ready (overwrite o MERGE)
```

```python
# Bronze: ingestar raw
# Silver: limpiar
df_silver = (spark.table("catalog.bronze.raw_events")
    .filter(F.col("event_type").isNotNull())
    .withColumn("event_date", F.to_date(F.col("timestamp")))
    .dropDuplicates(["event_id"])
)
df_silver.write.format("delta").mode("overwrite").saveAsTable("catalog.silver.events")

# Gold: agregar
df_gold = (spark.table("catalog.silver.events")
    .groupBy("event_date", "event_type")
    .agg(F.count("*").alias("total_events"),
         F.countDistinct("user_id").alias("unique_users"))
)
df_gold.write.format("delta").mode("overwrite").saveAsTable("catalog.gold.daily_event_summary")
```

---

## Exercises

### Exercise 1 — dbutils.secrets
> Tu notebook necesita conectarse a una API externa con una API key.
> **¿Por qué NO debes hacer `api_key = "sk-abc123..."` directamente en el notebook?**
> **¿Qué alternativa usa Databricks? Escribe el código correcto.**

### Exercise 2 — Window function
> Tienes tabla `orders` con columnas: `order_id`, `customer_id`, `amount`, `created_at`.
> Escribe PySpark para obtener el **pedido más reciente por cliente** (1 fila por cliente).

### Exercise 3 — Auto Loader design
> Tu empresa recibe archivos JSON en `s3://data-lake/raw/transactions/` cada 15 minutos.
> Los archivos nunca se sobreescriben, solo se añaden nuevos.
> 
> Diseña el pipeline completo:
> 1. ¿Qué formato de trigger usarías para un Job nocturno? ¿Y para streaming real-time?
> 2. ¿Para qué sirve el checkpoint? ¿Qué pasa si lo borras?
> 3. Escribe el código readStream → writeStream completo

### Exercise 4 — Medallion architecture
> Tienes estos datos raw en Bronze:
> ```
> {"user_id": "123", "event": "purchase", "ts": "2024-01-15T10:30:00Z", "amount": "45.99"}
> {"user_id": null, "event": "view", "ts": "2024-01-15T10:31:00Z", "amount": null}
> {"user_id": "123", "event": "purchase", "ts": "2024-01-15T10:30:00Z", "amount": "45.99"}  -- duplicado
> ```
> 
> Escribe las transformaciones Bronze → Silver → Gold donde:
> - Silver: filtra nulls en user_id, deduplica, castea tipos correctos
> - Gold: total de compras y suma de amount por usuario por día

### Exercise 5 — overwrite vs append vs merge decision
> Para cada escenario elige el write mode y justifica:
> 1. Tabla `dim_products` que se recarga completa cada noche desde un API
> 2. Tabla `events` que recibe 100K filas nuevas cada hora (nunca se modifican)
> 3. Tabla `user_profiles` donde los usuarios pueden actualizar su email/nombre

### Exercise 6 — Interview question
> "What is the Medallion Architecture and why is it a best practice?"
> Responde en 4 frases como en entrevista real.

---

## Key terms to memorize
- **`dbutils.secrets`** — fetch credentials sin exponerlas en código
- **`dbutils.widgets`** — parámetros dinámicos en notebooks/jobs
- **Auto Loader** — `format("cloudFiles")`, detecta archivos nuevos en S3/ADLS
- **Checkpoint** — registra archivos procesados, garantiza idempotencia
- **`trigger(availableNow=True)`** — procesa batch y para (no streaming continuo)
- **Medallion** — Bronze (raw) → Silver (clean) → Gold (aggregated)
- **Window functions** — `partitionBy + orderBy + row_number/rank/lag/lead`
