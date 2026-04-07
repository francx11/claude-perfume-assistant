"""
Tests para ClaudeClient.

DÍA 8: Implementarás estos tests para asegurar calidad del código.
"""

import pytest
from unittest.mock import Mock, patch
from anthropic import AuthenticationError, RateLimitError
from src.api.claude_client import ClaudeClient


class TestClaudeClient:
    """Tests para el cliente de Claude."""

    def test_init(self):
        """
        Test de inicialización del cliente.
        """
        client = ClaudeClient(api_key="test-key-123")
    
        assert client.api_key == "test-key-123"
        assert client.model == "claude-sonnet-4-6"

    def test_send_message_simple(self):
        """
        Test de envío de mensaje simple.
        """
        mock_response = Mock()
        mock_response.model_dump.return_value = {
            "content": [{"type": "text", "text": "Hola, soy Claude"}],
            "stop_reason": "end_turn"
        }

        with patch('src.api.claude_client.Anthropic') as mock_anthropic:
            mock_anthropic.return_value.messages.create.return_value = mock_response

            client = ClaudeClient(api_key="test-key")
            messages = [{"role": "user", "content": "Hola"}]
            response = client.send_message(messages)

            assert "content" in response
            assert response["content"][0]["text"] == "Hola, soy Claude"

            mock_anthropic.return_value.messages.create.assert_called_once()
        
    def test_send_message_with_tools(self):
        """
        Test de envío de mensaje con tools.

        TODO DÍA 8:
        1. Mockear respuesta con tool_use
        2. Enviar mensaje con tools
        3. Verificar que la respuesta contiene tool_use
        4. Verificar formato del tool_use
        """
        mock_response = Mock()
        mock_response.model_dump.return_value = {
            "content": [
                {
                    "type": "tool_use",
                    "id": "toolu_123",
                    "name": "search_perfumes",
                    "input": {"season": "summer"}
                }
            ],
            "stop_reason": "tool_use"
        }

        tools = [{"name": "search_perfumes", "description": "...", "input_schema": {"type": "object", "properties": {}}}]

        with patch('src.api.claude_client.Anthropic') as mock_anthropic:
            mock_anthropic.return_value.messages.create.return_value = mock_response

            client = ClaudeClient(api_key="test-key")
            messages = [{"role": "user", "content": "Busca perfumes de verano"}]
            response = client.send_message(messages, tools=tools)

            assert response["stop_reason"] == "tool_use"
            assert response["content"][0]["type"] == "tool_use"
            assert response["content"][0]["name"] == "search_perfumes"
            
    def test_create_tool_result(self):
        """
        Test de creación de tool result.
        """
        client = ClaudeClient(api_key="test-key")
    
        result = client.create_tool_result(
            tool_use_id="toolu_123",
            content={"perfumes": ["Sauvage", "Chanel No5"]}
        )
        
        assert result["role"] == "user"
        assert result["content"][0]["type"] == "tool_result"
        assert result["content"][0]["tool_use_id"] == "toolu_123"
        assert "Sauvage" in result["content"][0]["content"]

    def test_authentication_error(self):
        with patch('src.api.claude_client.Anthropic') as mock_anthropic:
            mock_anthropic.return_value.messages.create.side_effect = AuthenticationError(
                message="Invalid API key",
                response=Mock(status_code=401),
                body={}
            )

            client = ClaudeClient(api_key="invalid-key")
            messages = [{"role": "user", "content": "Hola"}]

            with pytest.raises(AuthenticationError):
                client.send_message(messages)

    def test_rate_limit_error(self):
        with patch('src.api.claude_client.Anthropic') as mock_anthropic:
            mock_anthropic.return_value.messages.create.side_effect = RateLimitError(
                message="Rate limit exceeded",
                response=Mock(status_code=429),
                body={}
            )

            client = ClaudeClient(api_key="test-key")
            messages = [{"role": "user", "content": "Hola"}]

            with pytest.raises(RateLimitError):
                client.send_message(messages)

    def test_timeout_error(self):
        with patch('src.api.claude_client.Anthropic') as mock_anthropic:
            mock_anthropic.return_value.messages.create.side_effect = TimeoutError("Request timed out")

            client = ClaudeClient(api_key="test-key")
            messages = [{"role": "user", "content": "Hola"}]

            with pytest.raises(TimeoutError):
                client.send_message(messages)

    def test_malformed_tools_raises_value_error(self):
        with patch('src.api.claude_client.Anthropic'):
            client = ClaudeClient(api_key="test-key")
            messages = [{"role": "user", "content": "Hola"}]
            bad_tools = [{"description": "sin nombre ni input_schema"}]

            with pytest.raises(ValueError):
                client.send_message(messages, tools=bad_tools)
