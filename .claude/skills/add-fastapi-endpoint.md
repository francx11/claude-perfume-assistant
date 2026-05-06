# Add FastAPI Endpoint

**When to apply:** Adding a new REST route to `api/endpoints.py`.

## Steps

1. Define Pydantic request/response models near the top of `api/endpoints.py` (above `app`):
```python
class MyRequest(BaseModel):
    field: str
    optional_field: Optional[str] = None

class MyResponse(BaseModel):
    result: str
    data: Optional[List[Dict[str, Any]]] = None
```

2. Add the route, accessing components via `http_request.app.state.*`:
```python
@app.post("/my-endpoint", response_model=MyResponse)
async def my_endpoint(request: MyRequest, http_request: Request) -> MyResponse:
    try:
        result = http_request.app.state.orchestrator.process_query(request.field)
        return MyResponse(result=result["response"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

3. If the route needs a new component, initialize it in `startup_event()` and attach to `app.state`:
```python
@app.on_event("startup")
async def startup_event():
    ...
    app.state.new_component = NewComponent(api_key=os.getenv("SOME_KEY"))
```

4. For file uploads, validate `content_type` before processing (see existing pattern at `api/endpoints.py:85`):
```python
ALLOWED = {"image/jpeg", "image/png", "image/webp", "image/tiff", "image/bmp"}
if file.content_type not in ALLOWED:
    raise HTTPException(status_code=400, detail=f"Invalid type: {file.content_type}")
image_bytes = await file.read()
```

5. For GET routes with optional query params, use the same filter-dict pattern:
```python
@app.get("/my-search")
async def my_search(brand: Optional[str] = None, gender: Optional[str] = None) -> List[Dict[str, Any]]:
    filters = {k: v for k, v in {"brand": brand, "gender": gender}.items() if v is not None}
    return app.state.data_loader.filter_perfumes(filters)
```

## Existing Endpoints (avoid duplicating)
- `POST /chat` — conversational query via OrchestratorAgent
- `POST /ocr/extract` — image upload → pytesseract text extraction
- `GET /perfumes/{perfume_id}` — perfume by ID
- `GET /perfumes/{perfume_id}/similar` — RAG similarity (top_k param)
- `POST /search` — filter by brand/season/gender/notes (comma-separated)
- `GET /perfumes` — full catalog
- `GET /health` — component initialization status

## Don't
- Don't access `app.state` directly without `http_request` in async route params — use `http_request.app.state`
- Don't put model loading or startup logic inside route handlers
- Don't return raw DataFrames — always `.to_dict('records')` first
- Don't swallow `HTTPException` in a bare `except Exception` block — re-raise it explicitly
