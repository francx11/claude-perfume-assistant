# Module 2: Delta Lake (Core del trabajo diario)

## Topics
- ACID en sistema distribuido
- Time travel + versioning
- `MERGE INTO` — upsert pattern
- Partitioning + Z-ordering (performance)
- Vacuum + Optimize

---

## Concepts

### ACID en Delta Lake
| Property | Meaning | Delta implementation |
|----------|---------|---------------------|
| Atomicity | Todo o nada | Transaction log — write committed only when log entry written |
| Consistency | Data siempre válida | Schema enforcement rejects bad writes |
| Isolation | Writes concurrentes no interfieren | Optimistic concurrency control |
| Durability | Committed = persistido | Parquet files + transaction log in object storage |

**Transaction log** = `_delta_log/` directory con JSON files numerados (0000.json, 0001.json...)
Cada JSON = una operación (ADD file, REMOVE file, UPDATE metadata)

### Time Travel
```python
# Read versión anterior
df = spark.read.format("delta").option("versionAsOf", 3).load("s3://bucket/table")

# Read por timestamp
df = spark.read.format("delta").option("timestampAsOf", "2024-01-15").load("s3://bucket/table")

# Ver historial completo
from delta.tables import DeltaTable
dt = DeltaTable.forPath(spark, "s3://bucket/table")
dt.history().show()

# SQL equivalente
spark.sql("SELECT * FROM my_table VERSION AS OF 3")
spark.sql("DESCRIBE HISTORY my_table")
```

**Use cases:** rollback after bad write, reproducible ML training datasets, audit trails

### MERGE INTO (upsert) — pattern más usado en proyectos reales
```python
from delta.tables import DeltaTable

target = DeltaTable.forPath(spark, "s3://bucket/customers")
updates = spark.createDataFrame([...])  # source DataFrame

(target.alias("t")
    .merge(updates.alias("u"), "t.customer_id = u.customer_id")
    .whenMatchedUpdate(set={"name": "u.name", "email": "u.email", "updated_at": "u.updated_at"})
    .whenNotMatchedInsert(values={"customer_id": "u.customer_id", "name": "u.name", "email": "u.email", "updated_at": "u.updated_at"})
    .whenNotMatchedBySourceDelete()  # delete rows not in source (full sync)
    .execute()
)
```

**SQL equivalente:**
```sql
MERGE INTO customers AS t
USING updates AS u ON t.customer_id = u.customer_id
WHEN MATCHED THEN UPDATE SET name = u.name, email = u.email
WHEN NOT MATCHED THEN INSERT *
WHEN NOT MATCHED BY SOURCE THEN DELETE
```

### Partitioning
```python
# Write con partición
df.write.format("delta").partitionBy("country", "year").save("s3://bucket/sales")

# Cuándo particionar:
# - columna usada frecuentemente en WHERE/GROUP BY
# - cardinalidad baja (country: 50 valores, NO user_id: millones)
# - partición >1GB de datos
```

**Anti-pattern:** particionar por columna de alta cardinalidad → millones de carpetas pequeñas → lento

### Z-ordering (clustering secundario)
```sql
-- Optimiza layout de archivos para filtros en columnas de alta cardinalidad
OPTIMIZE sales ZORDER BY (product_id, customer_id)
```
- No crea carpetas como partitioning
- Coloca datos relacionados en mismo archivo Parquet
- Ideal para columnas de búsqueda frecuente con alta cardinalidad

### Optimize + Vacuum
```sql
-- Compacta small files → mejor performance de lectura
OPTIMIZE my_table

-- Borra archivos Parquet que ya no son referenciados por ninguna versión
-- PELIGRO: elimina capacidad de time travel anterior al retention period
VACUUM my_table RETAIN 168 HOURS  -- 7 días (default)

-- Ver qué archivos serían borrados (dry run)
VACUUM my_table RETAIN 168 HOURS DRY RUN
```

---

## Exercises

### Exercise 1 — Transaction log reasoning
> Delta Lake escribe un JSON al `_delta_log/` por cada operación.
> Si tu job falla a mitad de escribir 10 archivos Parquet:
> **¿Qué pasa con esos archivos? ¿Los verán los lectores? ¿Por qué?**

### Exercise 2 — MERGE INTO design
> Tienes una tabla `dim_products` (10M rows) en Delta Lake.
> Cada noche recibes un DataFrame `daily_updates` con ~5000 productos modificados y ~200 nuevos.
> 
> Escribe el código PySpark completo para:
> 1. Hacer upsert (update si existe, insert si no)
> 2. Asegurarte de que `updated_at` se actualiza solo en MATCHED
> 3. NO eliminar productos que no están en `daily_updates`

### Exercise 3 — Partitioning decision
> Para cada tabla, decide si particionas y por qué columna:
> 1. `events` (1TB/día, columns: user_id, event_type, country, timestamp)
> 2. `dim_customers` (5M rows, mostly static, columns: customer_id, country, plan_type)
> 3. `transactions` (500GB/mes, columns: transaction_id, user_id, date, amount, status)

### Exercise 4 — Time travel scenario
> Tu pipeline de ML entrenó un modelo el 2024-03-15.
> El 2024-03-20 alguien hizo un `DELETE` masivo por error en `training_features`.
> 
> Escribe el código para:
> 1. Ver el historial de la tabla
> 2. Restaurar la tabla al estado de 2024-03-14
> 3. (Bonus) Hacer el restore sin sobreescribir — crear tabla nueva con los datos históricos

### Exercise 5 — Vacuum danger
> Tienes `VACUUM my_table RETAIN 0 HOURS` en tu pipeline.
> **¿Qué problema grave crea? ¿Qué pierdes? ¿Cuándo es aceptable ejecutar vacuum agresivo?**

### Exercise 6 — Interview question
> "Explain MERGE INTO in Delta Lake and when you'd use it over a simple overwrite."
> Responde en 4-5 frases como en entrevista real.

---

## Key terms to memorize
- **`_delta_log/`** — transaction log, source of truth for Delta table state
- **Time travel** — `VERSION AS OF` / `timestampAsOf`
- **MERGE INTO** — upsert: whenMatchedUpdate + whenNotMatchedInsert
- **Partitioning** — physical folder split, low-cardinality columns only
- **Z-ordering** — file-level clustering, high-cardinality columns
- **OPTIMIZE** — compact small files
- **VACUUM** — delete unreferenced Parquet files (kills time travel)
