# Add Claude Tool (Function Calling)

**When to apply:** Adding a new capability that Claude can invoke during a conversation via tool use.

## Steps

1. Add tool definition in `PerfumeTools.get_tools_definitions()` (`src/tools/perfume_tools.py:29`):
```python
tool_definitions.append({
    "name": "my_tool",
    "description": "Clear description so Claude knows exactly when to use this",
    "input_schema": {
        "type": "object",
        "properties": {
            "required_param": {
                "type": "string",
                "description": "What this param controls (e.g., perfume brand name)"
            },
            "optional_param": {
                "type": "integer",
                "description": "Number of results to return",
                "default": 5
            }
        },
        "required": ["required_param"]
    }
})
```

2. Add the execution method in the same class:
```python
def my_tool(
    self,
    required_param: str,
    optional_param: int = 5
) -> List[Dict[str, Any]]:
    filters = {k: v for k, v in {"brand": required_param}.items() if v is not None}
    results = self.data_loader.filter_perfumes(filters)
    return results[:optional_param]
```

3. Register in `PerfumeTools.execute_tool()` via `match/case` (`src/tools/perfume_tools.py:143`):
```python
case "my_tool":
    return self.my_tool(**tool_input)
```

4. The orchestrator loop in `src/agents/orchestrator.py` handles tool dispatch automatically — no changes needed there unless the tool returns data requiring special post-processing in the final response.

## Existing Tools
| Tool | Method | Requires |
|------|--------|----------|
| `search_perfumes` | `search_perfumes(brand, notes, season, gender, max_results=5)` | DataLoader |
| `get_perfume_details` | `get_perfume_details(perfume_id)` | DataLoader |
| `recommend_similar` | `recommend_similar(perfume_id, top_k=3)` | RAGRetriever |

## Orchestrator tool-use loop behavior (`src/agents/orchestrator.py`)
- Extracts all `tool_use` blocks from a single response and executes them
- Bundles all tool results as a `user` message content array
- Max 5 iterations — design tools for single-turn resolution, not multi-step chains
- Final text extracted with: `next(b["text"] for b in response["content"] if b["type"] == "text")`

## Don't
- Don't put execution logic in the orchestrator — keep it in `PerfumeTools`
- Don't forget both `get_tools_definitions()` AND `execute_tool()` — missing one breaks silently
- Don't use Python `None` as a value in `input_schema` — Anthropic validates strict JSON Schema
- Don't omit `"required": [...]` array — omitting it means all params are optional to Claude
- Don't design tool chains longer than 5 steps — enforced limit in orchestrator
