# Día 1: Conexión básica con Claude API

## Lo que aprendí

### Python básico

- **Atributos de instancia**: se guardan en `__init__` usando `self.atributo = valor`, accesibles desde cualquier método de la clase
- **`pass`**: placeholder para bloques vacíos, se reemplaza con la implementación real
- **`None` checks**: usar `if x is not None` es más preciso que `if x` porque distingue entre `None` y lista vacía `[]`
- **Kwargs dinámicos**: con `**{"key": value}` puedes pasar argumentos opcionales a una función en una sola línea

### Entorno y configuración

- **Entorno virtual**: aisla las dependencias del proyecto del sistema global
- **`python-dotenv`**: carga variables del `.env` como variables de entorno, evitando hardcodear credenciales en el código
- **`.env` en `.gitignore`**: las credenciales nunca van al repositorio

### Claude API

- La librería `anthropic` expone `client.messages.create()` para enviar mensajes
- Los mensajes tienen formato `[{"role": "user", "content": "..."}]`
- La respuesta es un objeto que se convierte a dict con `.model_dump()`
- El texto de la respuesta está en `response["content"][0]["text"]`

## Código implementado

`src/api/claude_client.py` → métodos `__init__` y `send_message`

## Problemas resueltos

- Conflicto de versiones `anthropic` + `httpx` → solución: `pip install httpx==0.27.0`
- Modelo no disponible en la cuenta → usar el modelo correcto de los disponibles en tu API key

---

## Conceptos clave de IA

### ¿Qué son los Embeddings vectoriales?

Un embedding es una representación numérica de texto (o imágenes, audio...) en forma de vector, es decir, una lista de números.

```
"Perfume fresco de verano" → [0.12, -0.87, 0.34, 0.56, ...]  # 384 números
"Fragancia cítrica ligera" → [0.11, -0.91, 0.38, 0.52, ...]  # muy parecidos
"Motor de combustión"      → [0.95,  0.23, -0.67, 0.01, ...] # muy distintos
```

La clave: textos con significado similar producen vectores similares (cercanos en el espacio). Textos distintos producen vectores lejanos.

La similitud entre vectores se mide con **cosine similarity**: devuelve un valor entre 0 y 1, donde 1 es idéntico y 0 es completamente distinto.

**En entrevista:** "Un embedding es una representación densa de texto en un espacio vectorial de alta dimensión, donde la proximidad geométrica refleja similitud semántica."

---

### ¿Qué es RAG (Retrieval-Augmented Generation)?

El problema que resuelve: los LLMs como Claude no conocen tu base de datos privada (el catálogo de perfumes). RAG soluciona esto en dos pasos:

```
1. RETRIEVAL (recuperar)
   Query del usuario → embedding → buscar vectores similares en tu base de datos
   → recuperar los N documentos más relevantes

2. AUGMENTED GENERATION (generar con contexto)
   Esos documentos se añaden al prompt de Claude como contexto
   → Claude genera una respuesta basada en TU información
```

**Ejemplo en este proyecto:**

```
Usuario: "Quiero un perfume fresco para verano"
    ↓
RAG busca en el catálogo los 5 perfumes más similares semánticamente
    ↓
Se los pasa a Claude: "Aquí tienes 5 perfumes relevantes: [datos]... recomienda uno"
    ↓
Claude responde con conocimiento real del catálogo
```

**En entrevista:** "RAG es una técnica que combina búsqueda semántica sobre una base de conocimiento propia con la capacidad generativa de un LLM, permitiendo que el modelo responda con información actualizada y privada sin necesidad de fine-tuning."

**Diferencia RAG vs Fine-tuning:**

- Fine-tuning: reentrenar el modelo con tus datos (caro, lento, datos estáticos)
- RAG: recuperar datos en tiempo real y dárselos al modelo como contexto (barato, flexible, datos actualizables)
