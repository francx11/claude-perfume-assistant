"""
Cliente para interactuar con la API de Claude (Anthropic).

Este módulo gestiona la comunicación con Claude, incluyendo:
- Autenticación con API key
- Envío de mensajes
- Manejo de tools (function calling)
- Gestión de errores de API

DÍA 1: Implementarás este cliente para tu primera conexión con un LLM.
"""

import random
import time
from typing import Any, Callable, Dict, List, Optional

from anthropic import Anthropic, RateLimitError

CLOSED = "closed"
OPEN = "open"
HALF_OPEN = "half_open"


class CircuitBreaker:
    """Protege llamadas a servicios externos cortando el circuito tras fallos consecutivos."""

    def __init__(self, max_fallos: int = 5, tiempo_reset: float = 60.0):
        """Inicializa el circuit breaker con umbral de fallos y tiempo de reset."""
        self.max_fallos = max_fallos
        self.tiempo_reset = tiempo_reset
        self.estado = CLOSED
        self.fallos = 0
        self.tiempo_apertura: Optional[float] = None

    def call(self, func: Callable) -> Any:
        """Ejecuta func respetando el estado del circuito."""
        if self.estado == OPEN:
            if time.time() - self.tiempo_apertura >= self.tiempo_reset:
                self.estado = HALF_OPEN
            else:
                raise RuntimeError("Circuit breaker OPEN: servicio no disponible")

        try:
            resultado = func()
            self._on_success()
            return resultado
        except Exception:
            self._on_failure()
            raise

    def _on_success(self) -> None:
        """Resetea el contador de fallos y cierra el circuito."""
        self.fallos = 0
        self.estado = CLOSED

    def _on_failure(self) -> None:
        """Incrementa fallos y abre el circuito si se alcanza el umbral."""
        self.fallos += 1
        if self.fallos >= self.max_fallos:
            self.estado = OPEN
            self.tiempo_apertura = time.time()


class ClaudeClient:
    """Cliente para la API de Claude de Anthropic."""

    def __init__(self, api_key: str, model: str = "claude-sonnet-4-6"):
        """
        Inicializa el cliente de Claude.
        """
        self.api_key = api_key
        self.model = model
        self.client = Anthropic(api_key=api_key)
        self.circuit_breaker = CircuitBreaker()

    def send_message(
        self,
        messages: List[Dict[str, str]],
        tools: Optional[List[Dict[str, Any]]] = None,
        max_tokens: int = 1024,
        system: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Envía un mensaje a Claude y retorna la respuesta.
        """

        if tools is not None:
            for tool in tools:
                if "name" not in tool or "input_schema" not in tool:
                    raise ValueError(f"Tool mal formateada, falta 'name' o 'input_schema': {tool}")

        MAX_REINTENTOS = 3
        for intento in range(MAX_REINTENTOS):
            try:

                def _call():
                    return self.client.messages.create(
                        model=self.model,
                        messages=messages,
                        max_tokens=max_tokens,
                        **({"tools": tools} if tools is not None else {}),
                        **({"system": system} if system is not None else {}),
                    )

                msg = self.circuit_breaker.call(_call)
                return msg.model_dump()
            except RateLimitError:
                if intento == MAX_REINTENTOS - 1:
                    raise
                espera = 2**intento + random.random()
                time.sleep(espera)
            except RuntimeError:
                raise

    def create_tool_result(self, tool_use_id: str, content: Any) -> Dict[str, Any]:
        """
        Crea un mensaje de resultado de tool para enviar a Claude.
        """

        return {
            "role": "user",
            "content": [{"type": "tool_result", "tool_use_id": tool_use_id, "content": str(content)}],
        }
