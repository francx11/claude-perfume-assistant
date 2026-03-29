"""
Cliente para interactuar con la API de Claude (Anthropic).

Este módulo gestiona la comunicación con Claude, incluyendo:
- Autenticación con API key
- Envío de mensajes
- Manejo de tools (function calling)
- Gestión de errores de API

DÍA 1: Implementarás este cliente para tu primera conexión con un LLM.
"""

from typing import List, Dict, Any, Optional
from anthropic import Anthropic


class ClaudeClient:

    """Cliente para la API de Claude de Anthropic."""

    def __init__(self, api_key: str, model: str = "claude-sonnet-4-6"):
        """
        Inicializa el cliente de Claude.
        """
        self.api_key = api_key
        self.model = model

        self.client = Anthropic(api_key=api_key)

    def send_message(
        self,
        messages: List[Dict[str, str]],
        tools: Optional[List[Dict[str, Any]]] = None,
        max_tokens: int = 1024
    ) -> Dict[str, Any]:
        """
        Envía un mensaje a Claude y retorna la respuesta.
        """

        if tools is not None:
             for tool in tools:
                if 'name' not in tool or 'input_schema' not in tool:
                    raise ValueError(f"Tool mal formateada, falta 'name' o 'input_schema': {tool}")

        msg = self.client.messages.create(
            model=self.model,
            messages=messages,
            max_tokens=max_tokens,
            **({"tools": tools} if tools is not None else {})
        )

        return msg.model_dump()

    def create_tool_result(self, tool_use_id: str, content: Any) -> Dict[str, Any]:
        """
        Crea un mensaje de resultado de tool para enviar a Claude.
        """
        
        return {
            "role": "user",
            "content": [
                {
                    "type": "tool_result",
                    "tool_use_id": tool_use_id,
                    "content": str(content)
                }
            ]
        }

    
