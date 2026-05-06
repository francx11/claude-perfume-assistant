# Project Integration

**When to apply:** User learned a concept and wants to apply it to PerfumeShop AI or Loopgate, OR when a new phase exercise requires adding/modifying code in the real projects.

## Integration Map

### PerfumeShop AI — Where New Concepts Land

| Concept | Integration Point | File |
|---------|------------------|------|
| Decorators | `@log_call` on `execute_tool` | `src/tools/perfume_tools.py` |
| Generator | `get_all_perfumes()` as generator | `src/data/loader.py` |
| Structured logging | Orchestrator tool call logs | `src/agents/orchestrator.py` |
| SOLID / DIP | Inject retriever as interface | `src/agents/orchestrator.py` |
| ChromaDB | Replace `.npy` + cosine loop | `src/rag/retriever.py` |
| FAISS | Replace cosine loop | `src/rag/retriever.py` |
| Prompt engineering | Rewrite system prompt with CoT | `src/agents/orchestrator.py` |
| LangGraph | Rebuild orchestrator as graph | new `src/agents/graph_orchestrator.py` |
| LangSmith | Add tracing | env vars + `langchain_core.tracers` |
| Langfuse | `@observe()` on process_query | `src/agents/orchestrator.py` |
| boto3 / S3 | Store/load embeddings from S3 | new `src/aws/embeddings_store.py` |
| Bedrock | Alternative Claude client | new `src/api/bedrock_client.py` |
| Textract | Replace pytesseract | `src/ocr/document_processor.py` |
| Docker | Containerize full app | new `Dockerfile` + `docker-compose.yml` |
| GitHub Actions | CI pipeline | new `.github/workflows/ci.yml` |
| Terraform | S3 bucket infra | new `infra/main.tf` |
| pytest coverage | `--cov` flag | `tests/` |
| pandas advanced | `get_stats()` method | `src/data/loader.py` |

### Loopgate — Where New Concepts Land

| Concept | Integration Point |
|---------|-----------------|
| WebSocket architecture | Explain human-in-the-loop gate in interview |
| LangGraph human-in-the-loop | Map to Loopgate's approval flow |
| K8s Deployment | Deploy Loopgate on EKS |
| GitHub Actions | CI/CD for Loopgate |

---

## Integration Protocol

### When user wants to add a feature:
1. Ask: "Before writing code — which file in the project should this go in? Why?"
2. Ask: "What inputs does it need? What should it return?"
3. Ask: "What test would verify it works?"
4. User writes the code → Claude reviews
5. Ask: "How would you explain this addition in an interview answer about [concept]?"

### When user wants to understand existing code through a new concept:
1. Point to the specific file/line where the concept is already present
2. Ask: "Now that you know what [concept] is — where do you see it in `src/agents/orchestrator.py`?"
3. Connect: "The tool_use loop you built IS the [ReAct / agent / LangGraph] pattern — explain why."

---

## Pitfalls to Avoid

- Don't let the user abstract prematurely — keep changes to one file at a time
- Don't replace working code with framework code just to use the framework — explain the tradeoff first
- Always ask "What does this break?" before implementing a change in a running component
- When adding AWS code: check for `[HUMAN APPROVAL REQUIRED]` rules in CLAUDE.md first
