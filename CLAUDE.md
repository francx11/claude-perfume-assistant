# PerfumeShop AI

Conversational perfume recommendation system powered by Claude API, RAG, and a Fragrantica CSV dataset.
Architecture: HTTP → FastAPI (`api/endpoints.py`) → `OrchestratorAgent` → `ClaudeClient` + `PerfumeTools` → `DataLoader` / `RAGRetriever`.
Learning project structured as day-by-day exercises (days 1–11), now transitioning to phase-based study.

## Stack
- Python 3.x
- `anthropic==0.39.0` · `fastapi==0.115.0` · `uvicorn[standard]==0.32.0` · `pydantic==2.9.0`
- `pandas==2.2.0` · `sentence-transformers==3.3.0` · `torch==2.5.0`
- `pytesseract==0.3.13` · `Pillow==11.0.0`
- `pytest==8.3.0` · `pytest-asyncio==0.24.0` · `httpx==0.28.0`

## Commands
```bash
uvicorn main:app --reload          # dev server
pytest tests/                      # run all tests
pytest tests/ -v -k "test_name"    # single test
```

## Code Conventions
- `snake_case` functions/variables; `PascalCase` classes
- Type hints on all signatures: `List`, `Dict`, `Any`, `Optional` from `typing`
- Naming: `get_*` retrieve · `search_*`/`filter_*` query · `extract_*` parse · `build_*` construct · `_handle_*`/`_build_*` private
- Conditional kwargs: `**({key: val} if condition else {})` — never pass `None` to Anthropic SDK
- Claude tools: define in `PerfumeTools.get_tools_definitions()`, dispatch in `execute_tool()` via `match/case`
- FastAPI: Pydantic models for request/response; components on `app.state.*` initialized in `startup_event()`
- Errors: let `AuthenticationError`, `RateLimitError`, `TimeoutError` propagate; wrap others in `HTTPException`
- All new code in English only

## Ignored Files
- `.env` — never read or commit
- `data/embeddings/*.npy` — generated artifacts
- `__pycache__/`, `*.pyc`, `.pytest_cache/`
- `prueba*.py` — scratch scripts

## Security Rules
- [HUMAN APPROVAL REQUIRED] Never commit `.env` or any file containing `ANTHROPIC_API_KEY`
- [HUMAN APPROVAL REQUIRED] Never delete or overwrite the Fragrantica CSV without a backup
- [HUMAN APPROVAL REQUIRED] Never force-push to `main`
- [HUMAN APPROVAL REQUIRED] Never modify deployment configs or CI/CD pipelines
- Always validate user-supplied file uploads via `content_type` allowlist (see `api/endpoints.py:85`)

## Auto-Maintenance
When you detect a recurring code pattern not described here, propose a CLAUDE.md update as a diff at the end of your response.

---

## Study Context

**Goal:** Pass internal AI Engineer interview. Full-time PHP/Magento dev studying in parallel.

**Background:**
- Professional: PHP/Magento, basic-intermediate Python
- Second active project: Loopgate (human-in-the-loop agents, FastAPI + WebSockets + React/TS)
- Completed days 1–11 of PerfumeShop AI — see `notas/` for details

### Teaching Rules
- **Socratic first**: ask a question that forces me to reason before explaining anything
- If I can't get it after 2 attempts, give a directional hint — not the solution
- Always connect new concepts to PerfumeShop AI or Loopgate when a natural link exists
- Flag interview-critical topics with [INTERVIEW CRITICAL] in responses
- At end of each session, propose a `progress/tracker.md` update with topics to mark as mastered

### What I've Already Built (treat as known)
- **Claude API**: `messages.create()`, tool use loop, tool definitions, JSON Schema format
- **FastAPI**: routes, Pydantic models, `async/await`, `app.state`, `UploadFile`, `HTTPException`, health check
- **RAG**: embeddings concept, cosine similarity implementation, `sentence-transformers`, `RAGRetriever`
- **Agents**: orchestrator pattern, tool_use loop (max 5 iter), multiple tool_use blocks per turn
- **Testing**: `pytest`, `Mock`, `patch` (patch where used, not defined), `side_effect`, `pytest.raises`
- **Pandas**: `read_csv`, `dropna`, `drop_duplicates`, `set_index`, `str.contains`, `to_dict('records')`
- **OCR**: `pytesseract`, PIL preprocessing (grayscale→contrast→binarize→resize), `BytesIO`
- **Python patterns**: dict/list comprehensions, `match/case`, `**dict` unpacking, `next()`, `enumerate()`

### What Still Needs Coverage
See `progress/tracker.md` for full status. Key gaps:
- Python: decorators, generators/yield, sets/tuples/lists diff, mutable defaults bug, lambda, PEP8 deep, SOLID, design patterns, logging, distributed errors
- ML Classical: classification, overfitting, confusion matrix, learning rate, PCA, cross-validation, imbalanced data
- LLMs advanced: RAG evaluation, chunking strategies, LoRA/adapters, prompt engineering, guardrails
- LangChain: LangGraph, LangSmith, Langfuse, Strands Agents
- AWS: boto3, S3, Lambda, Bedrock, DynamoDB, SageMaker, Textract, EKS, Athena
- Plus: Docker, Kubernetes, GitHub Actions, Terraform

### Study Plan
Phases in `study-plan/`:
1. `phase-1-python-solid.md` — Python gaps + tooling + patterns
2. `phase-2-ai-core.md` — Classical ML + RAG deep + LLMs advanced + data frameworks
3. `phase-3-langchain-strands.md` — LangChain, LangGraph, LangSmith, Langfuse, Strands
4. `phase-4-aws.md` — boto3, Bedrock, S3, Lambda, DynamoDB, Textract, SageMaker
5. `phase-5-plus.md` — Docker, K8s, CI/CD, Terraform
6. `phase-6-interview-sim.md` — Full interview simulation
