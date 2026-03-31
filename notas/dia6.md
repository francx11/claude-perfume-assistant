# Día 6: Orquestador Conversacional

## Python

### Patrón Orquestador

El orquestador es el componente central que coordina todos los demás. Recibe el mensaje del usuario, decide qué hacer, delega en otros componentes y devuelve la respuesta. Es el equivalente a un controlador en MVC pero con lógica de negocio más compleja.

### Strings multilínea

En Python los strings largos se escriben con triple comillas:

```python
return """Primera línea
Segunda línea
Tercera línea"""
```

Útil para system prompts y textos largos.

### `next()` con generador

```python
# Devuelve el primer elemento que cumple la condición
tool_use_block = next(b for b in response["content"] if b["type"] == "tool_use")

# Con valor por defecto si no encuentra nada
text = next((b["text"] for b in content if b["type"] == "text"), "Sin respuesta")
```

Es como `array_filter` + `reset()` de PHP en una línea.

### List comprehension para filtrar

```python
# Obtener TODOS los tool_use blocks (no solo el primero)
tool_use_blocks = [b for b in response["content"] if b["type"] == "tool_use"]
```

### Parámetros opcionales con kwargs dinámicos

```python
# Pasar system prompt solo si existe
**({"system": system} if system is not None else {})
```

### `import` dentro de función

```python
def mi_funcion():
    import json  # válido pero no recomendado
```

Mejor importar al inicio del fichero. Se hace dentro de funciones cuando la dependencia es opcional o para evitar imports circulares.

---

## FastAPI / Uvicorn

### Uvicorn

Servidor web asíncrono para Python. Equivalente a Apache/Nginx+PHP-FPM pero para aplicaciones async. FastAPI define las rutas, Uvicorn escucha el puerto y gestiona las conexiones HTTP.

### `Request` de FastAPI vs modelos Pydantic

Cuando un endpoint recibe un modelo Pydantic (`ChatRequest`) y también necesita acceder a `app.state`, hay que inyectar el `Request` de FastAPI como parámetro separado:

```python
from fastapi import Request

async def chat(request: ChatRequest, http_request: Request):
    orchestrator = http_request.app.state.orchestrator
```

`request` (Pydantic) tiene los datos del body. `http_request` (FastAPI) tiene acceso al contexto de la aplicación.

### `python-multipart`

Dependencia necesaria cuando FastAPI tiene endpoints con `UploadFile`. Sin ella el servidor arranca pero falla en runtime.

---

## Errores encontrados y soluciones

### `'ChatRequest' object has no attribute 'app'`

Causa: intentar acceder a `request.app.state` cuando `request` es un modelo Pydantic, no el objeto `Request` de FastAPI.
Solución: inyectar `Request` de FastAPI como parámetro adicional del endpoint.

### `tool_use ids were found without tool_result blocks`

Causa: Claude puede devolver múltiples `tool_use` en un mismo mensaje. El código solo procesaba el primero con `next()`, dejando los demás sin respuesta.
Solución: iterar sobre todos los `tool_use` blocks y añadir todos sus `tool_result` en un único mensaje de respuesta antes de volver a llamar a Claude.

### `'State' object has no attribute 'perfume_tools'`

Causa: `perfume_tools` no se guardó en `app.state` durante el startup.
Solución: añadir `app.state.perfume_tools = perfume_tools` en `startup_event()`.

---

## Para entrevista

**¿Qué es un orquestador en un sistema de IA?**
Es el componente que coordina el flujo entre el usuario, el LLM y las herramientas externas. Gestiona el historial conversacional, detecta cuándo el modelo quiere usar una tool, la ejecuta y devuelve el resultado al modelo hasta obtener una respuesta final en lenguaje natural.

**¿Qué es el tool_use loop?**
Cuando un LLM tiene tools disponibles, puede encadenar múltiples llamadas a herramientas antes de dar una respuesta final. El orquestador debe manejar este bucle: detectar `stop_reason == "tool_use"`, ejecutar la tool, devolver el resultado al modelo, y repetir hasta que el modelo responda con texto. Se limita el número de iteraciones para evitar bucles infinitos.

**¿Por qué es importante el system prompt?**
Define el comportamiento, personalidad y capacidades del asistente. Sin él, el modelo responde de forma genérica sin saber que es un asistente de perfumes ni cómo usar las tools disponibles. Un buen system prompt mejora significativamente la calidad y consistencia de las respuestas.

**¿Qué es Uvicorn?**
Un servidor ASGI (Asynchronous Server Gateway Interface) para Python. Es el equivalente a PHP-FPM pero para aplicaciones asíncronas. FastAPI define la lógica de la aplicación, Uvicorn gestiona las conexiones HTTP y el event loop de asyncio.
