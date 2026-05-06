# Write pytest Tests

**When to apply:** Adding tests for `ClaudeClient`, FastAPI endpoints, `PerfumeTools`, or `DataLoader`.

## Test file location
`tests/test_<module_name>.py` — mirror the `src/` structure.

## Pattern 1: Mock Anthropic API (ClaudeClient / Orchestrator)
Patch at `src.api.claude_client.Anthropic` — not at `anthropic.Anthropic`.
```python
from unittest.mock import Mock, patch
from src.api.claude_client import ClaudeClient

def test_send_message_text():
    mock_response = Mock()
    mock_response.model_dump.return_value = {
        "content": [{"type": "text", "text": "Hello"}],
        "stop_reason": "end_turn"
    }
    with patch('src.api.claude_client.Anthropic') as mock_anthropic:
        mock_anthropic.return_value.messages.create.return_value = mock_response
        client = ClaudeClient(api_key="test-key")
        result = client.send_message([{"role": "user", "content": "hi"}])
        assert result["stop_reason"] == "end_turn"
        mock_anthropic.return_value.messages.create.assert_called_once()
```

## Pattern 2: Mock tool_use response
```python
mock_response.model_dump.return_value = {
    "content": [{
        "type": "tool_use",
        "id": "toolu_123",
        "name": "search_perfumes",
        "input": {"season": "summer"}
    }],
    "stop_reason": "tool_use"
}
# Then assert response["content"][0]["name"] == "search_perfumes"
```

## Pattern 3: API errors — assert they propagate (no wrapping)
```python
from anthropic import AuthenticationError, RateLimitError

def test_authentication_error():
    with patch('src.api.claude_client.Anthropic') as mock_anthropic:
        mock_anthropic.return_value.messages.create.side_effect = AuthenticationError(
            message="Invalid key", response=Mock(status_code=401), body={}
        )
        client = ClaudeClient(api_key="bad-key")
        with pytest.raises(AuthenticationError):
            client.send_message([{"role": "user", "content": "hi"}])
```

## Pattern 4: FastAPI endpoint tests (httpx + pytest-asyncio)
```python
import pytest
from httpx import AsyncClient
from api.endpoints import app

@pytest.mark.asyncio
async def test_chat_endpoint():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/chat", json={"message": "recomienda perfumes"})
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert "conversation_id" in data
```

## Pattern 5: DataLoader tests with tmp CSV (no mocking)
```python
def test_filter_by_brand(tmp_path):
    csv = tmp_path / "test.csv"
    csv.write_text("id,name,brand\n1,sauvage,dior\n2,no5,chanel\n")
    loader = DataLoader(str(csv))
    results = loader.filter_perfumes({"brand": "dior"})
    assert len(results) == 1
    assert results[0]["brand"] == "dior"
```

## Run commands
```bash
pytest tests/
pytest tests/test_claude_client.py -v
pytest tests/ -k "test_auth"
```

## Don't
- Don't patch `anthropic.Anthropic` — always patch `src.api.claude_client.Anthropic`
- Don't test Anthropic model behavior — only test how your code responds to various API states
- Don't use `asyncio.run()` in test functions — use `@pytest.mark.asyncio` (pytest-asyncio is installed)
- Don't assert on exact Claude response text — assert on structure: `stop_reason`, `content[0]["type"]`
- Don't test `ValueError` for malformed tools by calling the Anthropic SDK — validate in `ClaudeClient.send_message()` before the API call
