# Module 5: MLflow en Databricks

## Topics
- Experiment tracking
- MLflow Model Registry
- Deploy desde Registry
- MLflow + Databricks integración nativa
- Feature Store (conceptual)

---

## Concepts

### ¿Qué problema resuelve MLflow?
Sin MLflow:
- Entrenas 20 modelos con distintos hiperparámetros → ¿cuál era el mejor?
- Usas modelo en prod → ¿qué versión? ¿con qué datos se entrenó?
- Equipo de 3 personas → nadie sabe qué ya se probó

MLflow resuelve: **reproducibilidad + tracking + deployment** de experimentos ML.

### 4 componentes de MLflow
| Componente | Función |
|------------|---------|
| **Tracking** | Log métricas, parámetros, artefactos por experimento |
| **Projects** | Empaquetar código ML en formato reproducible |
| **Models** | Formato estándar para deploy de modelos |
| **Registry** | Versionado y lifecycle de modelos (Staging/Production) |

### MLflow Tracking — logging básico
```python
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score, accuracy_score

# Databricks: MLflow ya configurado, experiments se guardan en workspace
mlflow.set_experiment("/Users/francisco/perfume_classifier")

with mlflow.start_run(run_name="rf_baseline"):
    # Log parámetros del modelo
    mlflow.log_param("n_estimators", 100)
    mlflow.log_param("max_depth", 5)
    mlflow.log_param("random_state", 42)

    # Entrenar
    model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    # Log métricas
    mlflow.log_metric("f1_score", f1_score(y_test, preds, average="weighted"))
    mlflow.log_metric("accuracy", accuracy_score(y_test, preds))

    # Log artefactos (archivos)
    mlflow.log_artifact("feature_importance.png")
    mlflow.log_artifact("preprocessing_config.json")

    # Log modelo con signature
    from mlflow.models import infer_signature
    signature = infer_signature(X_train, preds)
    mlflow.sklearn.log_model(model, "model", signature=signature)
```

### MLflow con autolog — menos código
```python
import mlflow.sklearn

mlflow.sklearn.autolog()  # captura automáticamente params, metrics, model

with mlflow.start_run():
    model = RandomForestClassifier(n_estimators=100)
    model.fit(X_train, y_train)
    # autolog registra todo automáticamente
```

**Soporte autolog:** sklearn, XGBoost, LightGBM, PyTorch, TensorFlow, Spark ML

### MLflow Model Registry
```python
# 1. Registrar modelo desde un run
model_uri = f"runs:/{run_id}/model"
registered = mlflow.register_model(model_uri, "PerfumeClassifier")

# 2. Transicionar stages (API antigua — MLflow < 2.0)
client = mlflow.tracking.MlflowClient()
client.transition_model_version_stage(
    name="PerfumeClassifier",
    version=registered.version,
    stage="Staging"  # None → Staging → Production → Archived
)

# MLflow >= 2.0: usar aliases en vez de stages
client.set_registered_model_alias("PerfumeClassifier", "champion", version=3)
client.set_registered_model_alias("PerfumeClassifier", "challenger", version=4)
```

### Cargar modelo desde Registry
```python
# En producción / scoring
model = mlflow.sklearn.load_model("models:/PerfumeClassifier/Production")
# o con alias:
model = mlflow.sklearn.load_model("models:/PerfumeClassifier@champion")

predictions = model.predict(new_data)

# Como PySpark UDF para scoring masivo en Databricks
from mlflow.pyfunc import spark_udf
predict_udf = mlflow.pyfunc.spark_udf(spark, "models:/PerfumeClassifier@champion")

df_scored = df.withColumn("prediction", predict_udf(*feature_columns))
```

### Comparar experiments en UI
- En Databricks: Experiments → seleccionar runs → Compare
- Ver parallel coordinates plot (hiperparámetros vs métricas)
- Filtrar por `metrics.f1_score > 0.85`

### MLflow + Databricks Feature Store (conceptual)
```python
from databricks.feature_store import FeatureStoreClient

fs = FeatureStoreClient()

# Definir feature table
fs.create_table(
    name="catalog.feature_store.user_features",
    primary_keys=["user_id"],
    schema=features_df.schema,
    description="User behavioral features"
)

# Escribir features
fs.write_table(name="catalog.feature_store.user_features", df=features_df)

# Leer features para training (point-in-time correct si hay timestamp)
training_df = fs.read_table("catalog.feature_store.user_features")
```

**Por qué Feature Store:** evita training-serving skew — mismas features en entrenamiento y en producción.

---

## Exercises

### Exercise 1 — Run tracking design
> Vas a entrenar 3 modelos (RandomForest, XGBoost, LogisticRegression) con distintos hiperparámetros.
> 
> **¿Qué loguearías con `mlflow.log_param`, `mlflow.log_metric`, y `mlflow.log_artifact` para cada run?**
> Diseña la estructura de logging antes de escribir código.

### Exercise 2 — Autolog vs manual
> ¿Cuándo usarías `mlflow.sklearn.autolog()` vs logging manual?
> Da un ejemplo de algo que autolog NO captura y que necesitas loguear manualmente.

### Exercise 3 — Model Registry workflow
> Tienes 2 versiones de `PerfumeClassifier`:
> - v1 en Production (f1=0.82)
> - v2 recién entrenada en Staging (f1=0.87)
>
> Escribe el código para:
> 1. Comparar las dos versiones programáticamente
> 2. Promover v2 a Production
> 3. Archivar v1

### Exercise 4 — Scoring masivo
> Tienes 10M de perfiles de usuario en una Delta table `catalog.silver.users`.
> Tu modelo `PerfumeClassifier@champion` predice qué familia olfativa prefiere cada usuario.
>
> Escribe el código para:
> 1. Cargar el modelo como Spark UDF
> 2. Aplicarlo a toda la tabla
> 3. Guardar resultados en `catalog.gold.user_predictions`

### Exercise 5 — Training-serving skew
> **¿Qué es training-serving skew? Da un ejemplo concreto.**
> **¿Cómo lo previene el Feature Store?**

### Exercise 6 — Interview question
> "Walk me through your MLflow workflow from experiment to production deployment."
> Responde en 5-6 frases como en entrevista real.

---

## Key terms to memorize
- **Run** — una ejecución de experimento con params, metrics, artifacts
- **Experiment** — colección de runs
- **`log_param`** — hiperparámetros (string/int/float)
- **`log_metric`** — métricas evaluables (float, puede ser por step)
- **`log_artifact`** — archivos (plots, configs, datos)
- **`log_model`** — guardar modelo en formato MLflow
- **Registry stages** — None → Staging → Production → Archived
- **Aliases** — `@champion`, `@challenger` (MLflow >= 2.0, mejor que stages)
- **`spark_udf`** — deploy modelo como UDF para scoring distribuido
- **Feature Store** — evita training-serving skew
