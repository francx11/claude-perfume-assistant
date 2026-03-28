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

        TODO DÍA 4 (cuando implementes tools):
        - Verificar que tools tenga el formato correcto antes de enviar
        - Manejar respuestas que contengan tool_use blocks

        Args:
            messages: Lista de mensajes en formato [{"role": "user", "content": "..."}]
            tools: Definiciones de tools para function calling (opcional)
            max_tokens: Máximo de tokens en la respuesta

        Returns:
            Diccionario con la respuesta de Claude

        Raises:
            AuthenticationError: Si la API key es inválida
            RateLimitError: Si se excede el rate limit
            APIError: Para otros errores de la API

        Ejemplo de uso:
            messages = [{"role": "user", "content": "Hola, ¿cómo estás?"}]
            response = client.send_message(messages)
            print(response["content"][0]["text"])
        """

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

        TODO DÍA 4:
        1. Retornar un diccionario con la estructura:
           {
               "role": "user",
               "content": [
                   {
                       "type": "tool_result",
                       "tool_use_id": tool_use_id,
                       "content": str(content)  # Convertir a string si no lo es
                   }
               ]
           }

        ¿Por qué necesitamos esto?
        Cuando Claude usa una tool, debemos enviarle el resultado en este formato
        específico para que pueda continuar la conversación.

        Args:
            tool_use_id: ID del tool_use block que generó Claude
            content: Resultado de ejecutar la tool

        Returns:
            Mensaje formateado para enviar a Claude
        """
        pass
