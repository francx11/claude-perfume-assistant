# Module 1: Architecture & Core Concepts

## Topics
- Lakehouse vs Data Warehouse vs Data Lake
- Delta Lake — what it is and why it matters
- Unity Catalog — centralized governance
- Workspace, clusters, notebooks

---

## Concepts

### Data Lake vs Data Warehouse vs Lakehouse

| | Data Lake | Data Warehouse | Lakehouse |
|---|---|---|---|
| Storage | Raw files (S3/ADLS) | Proprietary (Redshift, Snowflake) | Open format (Delta on S3/ADLS) |
| Schema | Schema-on-read | Schema-on-write | Schema-on-write + enforced |
| ACID | No | Yes | Yes (via Delta Lake) |
| ML workloads | Yes | No | Yes |
| SQL queries | Painful | Yes | Yes |
| Cost | Cheap storage | Expensive | Cheap storage + compute |

**Lakehouse = Data Lake storage + Data Warehouse reliability + ML support**

### Delta Lake
- Open-source storage layer on top of Parquet
- Adds: ACID transactions, time travel, schema enforcement, `MERGE INTO`
- Lives in object storage (S3, ADLS, GCS) — you own the data
- Databricks created it; now Linux Foundation project

### Unity Catalog
- Centralized governance for all data assets across workspaces
- 3-level namespace: `catalog.schema.table`
- Controls: who can read/write/manage which tables
- Replaces old per-workspace Hive Metastore

### Workspace anatomy
```
Workspace
├── Clusters          # compute (single-node dev / multi-node prod)
├── Notebooks         # interactive code (Python, SQL, Scala, R)
├── Repos             # Git integration (connect to GitHub)
├── Workflows (Jobs)  # scheduled/triggered pipelines
├── SQL Warehouses    # compute for Databricks SQL
└── Catalog Explorer  # browse Unity Catalog tables
```

### Cluster types
| Type | Use |
|------|-----|
| All-purpose | Interactive dev, notebooks |
| Job cluster | Runs one job, terminates — cheaper |
| SQL Warehouse | Databricks SQL queries only |

---

## Exercises

### Exercise 1 — Conceptual mapping
> Without looking at the table above, classify each tool as Data Lake, Data Warehouse, or Lakehouse:
> - Amazon S3 with raw CSV files
> - Google BigQuery
> - Snowflake
> - Databricks with Delta Lake
> - Amazon Redshift
> - Azure Data Lake Storage (ADLS) with Parquet + no catalog

### Exercise 2 — Socratic reasoning
> You have a PySpark job that writes a Parquet file to S3 every hour.
> Two jobs run simultaneously and both try to write to the same path.
> **What happens? Why is this a problem? How does Delta Lake solve it?**

### Exercise 3 — Unity Catalog namespace
> Given the 3-level namespace `catalog.schema.table`:
> Design a Unity Catalog structure for a company with:
> - 2 business units: `marketing` and `finance`
> - Each has `raw`, `clean`, and `aggregated` data layers
> - Shared `dim_customers` table used by both units
>
> Write the full table paths for:
> 1. Raw marketing events
> 2. Clean finance transactions
> 3. Shared customer dimension

### Exercise 4 — Cluster selection
> For each scenario, choose the right cluster type and explain why:
> 1. You're exploring a new dataset interactively
> 2. A nightly ETL job runs at 2am and processes 50GB
> 3. A BI analyst runs SQL queries via Tableau

### Exercise 5 — Interview question
> "What is a Lakehouse and why did it emerge?"
> Write a 3-sentence answer as if in a real interview.

---

## Key terms to memorize
- **Delta Lake** — ACID-compliant storage layer over Parquet
- **Transaction log** (`_delta_log/`) — JSON files recording every operation
- **Unity Catalog** — governance layer, 3-level namespace
- **All-purpose cluster** — interactive dev
- **Job cluster** — ephemeral, cheapest option for production jobs
