# Día 5: Endpoints FastAPI

## Lo que aprendí

### Qué es FastAPI

FastAPI es el equivalente a Laravel/Symfony en Python. Define rutas HTTP, valida requests/responses automáticamente con Pydantic, y genera documentación Swagger en `/docs` sin configuración extra.

Comparativa con PHP:

```python
# FastAPI
@app.get("/perfumes/{id}")
async def get_perfume(id: str):
    return {"name": "Sauvage"}
```

```php
// Laravel equivalente
Route::get('/perfumes/{id}', fn($id) => ["name" => "Sauvage"]);
```

### Decoradores de rutas

`@app.get()`, `@app.post()`, `@app.put()`, `@app.delete()` mapean métodos HTTP a funciones Python. Son como los atributos `#[Route]` de Symfony o `Route::get()` de Laravel.

### Convención REST GET vs POST

- `GET` → leer datos, sin modificar nada. Los parámetros van en la URL
- `POST` → enviar datos en el body para crear o procesar algo
- `GET /perfumes/{id}` para obtener un perfume concreto
- `GET /perfumes` para listar todos
- `GET /search?brand=Dior&season=summer` para filtrar con query parameters

### Query parameters vs Path parameters

```python
# Path parameter → obligatorio, va en la URL
@app.get("/perfumes/{perfume_id}")
async def get_perfume(perfume_id: str):  # /perfumes/dior-sauvage

# Query parameter → opcional, va después del ?
@app.get("/search")
async def search(brand: Optional[str] = None):  # /search?brand=Dior
```

### Pydantic para validación

Pydantic valida automáticamente los tipos de datos en requests y responses. Es como los Form Requests de Laravel:

```python
class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None
```

Si el cliente envía un tipo incorrecto, FastAPI devuelve un 422 automáticamente.

### async/await

En PHP tradicional cada request bloquea el hilo. Con `async`, mientras esperas respuesta de Claude, el servidor atiende otras peticiones:

```python
async def chat(request):
    response = await llamada_lenta()  # no bloquea otros requests
    return response
```

### app.state

Equivalente al contenedor de servicios de Laravel. Inicializas los componentes una vez al arrancar y los reutilizas en todos los endpoints:

```python
@app.on_event("startup")
async def startup_event():
    app.state.data_loader = DataLoader(...)
    app.state.orchestrator = OrchestratorAgent(...)

# En cualquier endpoint:
result = app.state.data_loader.get_all_perfumes()
```

### Manejo de errores HTTP

En FastAPI los errores HTTP se lanzan con `HTTPException`, equivalente a `abort()` en Laravel:

```python
raise HTTPException(status_code=404, detail="Perfume no encontrado")
raise HTTPException(status_code=500, detail=str(e))
```

Cuando lanzas una `HTTPException` dentro de un `except`, necesitas re-lanzarla antes del `except Exception` genérico para que no sea capturada:

```python
except HTTPException:
    raise  # re-lanzar sin modificar
except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
```

### Health check

Endpoint estándar en cualquier API para verificar que el servicio está vivo y sus dependencias inicializadas. Lo usan los sistemas de monitorización y los load balancers:

```python
@app.get("/health")
async def health_check():
    try:
        _ = app.state.orchestrator  # verifica que existe
        return {"status": "ok"}
    except AttributeError:
        return {"status": "error", "message": "Components not initialized"}
```

## Código implementado

`api/endpoints.py` → endpoints `/chat`, `/perfumes`, `/perfumes/{id}`, `/search`, `/recommend`, `/health`
`main.py` → arranque del servidor con uvicorn

## Para entrevista

**¿Qué es FastAPI?**
Un framework web Python moderno y de alto rendimiento basado en Starlette y Pydantic. Usa type hints de Python para validar automáticamente requests/responses y generar documentación OpenAPI. Es asíncrono por defecto, lo que lo hace muy eficiente para APIs que hacen muchas llamadas a servicios externos como LLMs.

**¿Qué diferencia hay entre GET y POST?**
GET es idempotente: puedes llamarlo N veces y el estado del servidor no cambia. Se usa para leer datos. POST no es idempotente: crea o procesa algo. Los parámetros de GET van en la URL, los de POST en el body.

**¿Qué es Pydantic?**
Una librería de validación de datos que usa type hints de Python. Define la forma esperada de los datos y valida automáticamente que los tipos sean correctos. FastAPI lo usa para validar requests y serializar responses a JSON.

**¿Por qué async en los endpoints?**
Porque los endpoints hacen llamadas a servicios externos (Claude API, base de datos). Con async, el servidor puede atender otras peticiones mientras espera esas respuestas, en lugar de bloquear un hilo por cada request.
