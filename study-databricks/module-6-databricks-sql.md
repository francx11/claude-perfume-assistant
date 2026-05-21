# Module 6: Databricks SQL + Lakehouse

## Topics
- SQL Warehouses vs All-purpose clusters
- Managed tables vs External tables
- Databricks SQL (DBSQL) — queries, dashboards
- Delta Live Tables (DLT) — declarative pipelines
- Unity Catalog permissions

---

## Concepts

### SQL Warehouse vs All-purpose cluster
| | SQL Warehouse | All-purpose cluster |
|---|---|---|
| Optimized for | SQL queries, BI tools | PySpark, ML, interactive notebooks |
| Language | SQL only | Python, SQL, Scala, R |
| Scaling | Auto-scale (T-shirt sizes) | Manual config |
| Photon engine | Yes (default) | Optional |
| Connect via | JDBC/ODBC, REST API | Notebook only |
| BI tools | Tableau, Power BI, Looker | Not directly |

**Photon** = C++ vectorized query engine, hasta 12x más rápido que Spark para SQL puro.

### Managed vs External tables

```sql
-- Managed table (Databricks controla datos + metadata)
-- Si haces DROP TABLE → se borran los datos de S3/ADLS
CREATE TABLE catalog.silver.customers (
    customer_id STRING,
    name STRING,
    email STRING,
    created_at TIMESTAMP
) USING DELTA;

-- External table (tú controlas los datos, Databricks solo la metadata)
-- Si haces DROP TABLE → solo se elimina la metadata, datos siguen en S3
CREATE TABLE catalog.bronze.raw_events
USING DELTA
LOCATION 's3://my-bucket/raw/events/';
```

**Regla práctica:**
- Bronze (raw, viene de fuera) → External table (controlas los datos)
- Silver + Gold → Managed table (Databricks gestiona todo)

### Databricks SQL — operaciones comunes
```sql
-- Crear/reemplazar tabla desde query
CREATE OR REPLACE TABLE catalog.gold.daily_summary AS
SELECT
    event_date,
    event_type,
    COUNT(*) AS total_events,
    COUNT(DISTINCT user_id) AS unique_users
FROM catalog.silver.events
GROUP BY event_date, event_type;

-- CTAS con partición
CREATE OR REPLACE TABLE catalog.gold.sales_by_country
PARTITIONED BY (country)
AS SELECT * FROM catalog.silver.sales;

-- Dynamic overwrite partition (no borra otras particiones)
SET spark.sql.sources.partitionOverwriteMode = dynamic;
INSERT OVERWRITE catalog.gold.sales_by_country
SELECT * FROM catalog.silver.sales WHERE country = 'ES';

-- Optimize + Z-order desde SQL
OPTIMIZE catalog.silver.events ZORDER BY (user_id, event_type);
VACUUM catalog.silver.events RETAIN 168 HOURS;

-- Describe para ver metadata
DESCRIBE DETAIL catalog.silver.events;
DESCRIBE HISTORY catalog.silver.events;
```

### Delta Live Tables (DLT) — declarative pipelines
DLT permite definir tablas como transformaciones, y Databricks gestiona el orden de ejecución.

```python
import dlt
from pyspark.sql import functions as F

# Bronze — streaming desde Auto Loader
@dlt.table(
    name="raw_events",
    comment="Raw events ingested from S3",
    table_properties={"quality": "bronze"}
)
def raw_events():
    return (spark.readStream
        .format("cloudFiles")
        .option("cloudFiles.format", "json")
        .load("s3://bucket/raw/events/")
    )

# Silver — apply expectations (data quality)
@dlt.table(name="clean_events", comment="Validated and cleaned events")
@dlt.expect_or_drop("valid_user", "user_id IS NOT NULL")
@dlt.expect("valid_amount", "amount > 0")  # solo loguea, no dropea
def clean_events():
    return (dlt.read_stream("raw_events")
        .withColumn("event_date", F.to_date(F.col("timestamp")))
        .dropDuplicates(["event_id"])
    )

# Gold — batch aggregation
@dlt.table(name="daily_summary")
def daily_summary():
    return (dlt.read("clean_events")
        .groupBy("event_date", "event_type")
        .agg(F.count("*").alias("total"))
    )
```

**DLT vs Jobs:** DLT = pipeline declarativo con data quality integrada. Jobs = orquestación general.

### Unity Catalog — permisos
```sql
-- Dar permisos
GRANT SELECT ON TABLE catalog.gold.daily_summary TO `data-analysts-group`;
GRANT CREATE TABLE ON SCHEMA catalog.silver TO `data-engineers-group`;
GRANT ALL PRIVILEGES ON CATALOG main TO `admin-group`;

-- Ver permisos
SHOW GRANTS ON TABLE catalog.gold.daily_summary;

-- Revocar
REVOKE SELECT ON TABLE catalog.gold.daily_summary FROM `data-analysts-group`;
```

**Niveles de permisos (mayor a menor):**
`CATALOG → SCHEMA → TABLE → COLUMN`

### Conectar Tableau/Power BI
```
1. SQL Warehouse → Connection details → Copy Server Hostname
2. Tableau: Connect → Databricks → Server: <hostname>, HTTP Path: <path>
3. Autenticación: Personal Access Token (PAT)
4. Seleccionar catalog.schema.table
```

---

## Exercises

### Exercise 1 — Managed vs External
> Tu empresa tiene estos datos:
> - Logs de nginx que se generan externamente y llegan a `s3://company-data/nginx/`
> - Tabla `dim_products` que construyes desde múltiples fuentes en Databricks
> - Tabla `raw_api_responses` con datos raw de una API externa
> - Tabla `gold_daily_kpis` que produces con PySpark
>
> Para cada una: ¿managed o external? ¿Por qué?

### Exercise 2 — SQL Warehouse selection
> Para cada caso elige SQL Warehouse o All-purpose cluster:
> 1. Data scientist explorando un nuevo dataset con pandas y matplotlib
> 2. BI analyst corriendo queries desde Power BI
> 3. Job de ETL que usa PySpark para procesar 500GB nocturnamente
> 4. Data engineer testeando una query SQL nueva

### Exercise 3 — DLT expectations
> Tienes una tabla de transacciones bancarias con las reglas:
> - `transaction_id` nunca puede ser null → si falla, dropear fila
> - `amount` debe ser positivo → si falla, solo loguear (no dropear)
> - `currency` debe ser uno de: EUR, USD, GBP → si falla, quarantine (mover a tabla aparte)
>
> Escribe las anotaciones DLT `@dlt.expect_*` correspondientes.

### Exercise 4 — Unity Catalog permissions
> Diseña la estructura de permisos para:
> - Equipo `data-engineers`: puede leer/escribir en Bronze y Silver, leer Gold
> - Equipo `data-analysts`: solo lectura en Gold y Silver
> - Equipo `ml-team`: leer Silver y Gold, crear tablas en `catalog.ml_experiments`
> - Usuarios externos (BI tool): solo lectura en Gold vía SQL Warehouse
>
> Escribe los GRANT statements.

### Exercise 5 — Dynamic partition overwrite
> Tienes `catalog.gold.sales_by_country` particionada por `country`.
> Procesas datos nuevos para España (ES) y quieres sobreescribir SOLO esa partición.
> 
> **¿Qué pasa si usas `mode("overwrite")` sin configuración especial?**
> **¿Cómo usas dynamic partition overwrite correctamente?**

### Exercise 6 — Interview question
> "What is Delta Live Tables and how does it differ from a traditional Databricks Job?"
> Responde en 4-5 frases como en entrevista real.

---

## Key terms to memorize
- **SQL Warehouse** — SQL + BI tools, Photon engine, JDBC/ODBC
- **Photon** — vectorized C++ engine, fast SQL
- **Managed table** — DROP = borra datos; ideal Silver/Gold
- **External table** — DROP = solo metadata; ideal Bronze/raw
- **DLT** — declarative pipelines con `@dlt.table`, data quality con `@dlt.expect_*`
- **`expect_or_drop`** — fila inválida se elimina de la tabla
- **`expect`** — fila inválida se loguea pero queda en tabla
- **Unity Catalog GRANT** — `GRANT SELECT ON TABLE ... TO ...`
- **Dynamic partition overwrite** — sobreescribe solo particiones presentes en los datos nuevos
