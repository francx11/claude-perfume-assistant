# Databricks Professional Seminar

Método: Socrático. Lee concepto → intenta ejercicio → luego revisa.

## Módulos

| # | Archivo | Temas clave | Prioridad |
|---|---------|-------------|-----------|
| 1 | [module-1-architecture.md](module-1-architecture.md) | Lakehouse, Delta Lake, Unity Catalog, clusters | Alta |
| 2 | [module-2-delta-lake.md](module-2-delta-lake.md) | ACID, time travel, MERGE INTO, partitioning, vacuum | Alta |
| 3 | [module-3-pyspark-databricks.md](module-3-pyspark-databricks.md) | dbutils, Auto Loader, Medallion, window functions | Alta |
| 4 | [module-4-workflows.md](module-4-workflows.md) | Jobs, tasks, %run vs dbutils.notebook.run, task values | Alta |
| 5 | [module-5-mlflow.md](module-5-mlflow.md) | Experiment tracking, Model Registry, Feature Store | Media |
| 6 | [module-6-databricks-sql.md](module-6-databricks-sql.md) | SQL Warehouse, managed/external, DLT, Unity Catalog perms | Media |

## Orden recomendado
1 → 2 → 3 → 4 (base de cualquier proyecto real)
5 (si proyecto tiene componente ML)
6 (si proyecto tiene BI/analytics o analistas SQL)

## Interview critical topics
- Delta Lake ACID + transaction log
- MERGE INTO pattern
- Medallion Architecture (Bronze/Silver/Gold)
- Managed vs External tables
- MLflow tracking + Registry
- Unity Catalog 3-level namespace
