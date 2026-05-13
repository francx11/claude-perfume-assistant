"""
Orquestador del flujo conversacional.

Este módulo coordina:
- Interacción entre usuario y Claude
- Ejecución de tools
- Manejo de contexto conversacional
- Gestión de errores

DÍA 6: Implementarás este módulo para integrar todos los componentes.
"""

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class OrchestratorAgent:
    """Orquestador del asistente conversacional."""

    def __init__(self, claude_client, perfume_tools, ocr_processor=None):
        """
        Inicializa el orquestador.
        """
        self.claude_client = claude_client
        self.perfume_tools = perfume_tools
        self.ocr_processor = ocr_processor

        self.conversation_history = []

    def process_query(self, user_message: str, conversation_history: Optional[List[Dict]] = None) -> Dict[str, Any]:
        """
        Procesa una consulta del usuario y retorna respuesta.

        ¿Qué es el tool_use loop?
        Claude puede pedir ejecutar una tool, luego otra, y así sucesivamente.
        Debemos manejar este flujo iterativo hasta que Claude dé una respuesta final.
        """
        if conversation_history is None:
            conversation_history = []

        conversation_history.append({"role": "user", "content": user_message})

        system_prompt = self._build_system_prompt()

        tools_definitions = self.perfume_tools.get_tools_definitions()
        response = self.claude_client.send_message(
            messages=conversation_history, tools=tools_definitions, max_tokens=1024, system=system_prompt
        )

        iteration = 0

        while response["stop_reason"] == "tool_use" and iteration < 5:
            conversation_history.append({"role": "assistant", "content": response["content"]})

            # Procesar TODOS los tool_use blocks del mensaje
            tool_use_blocks = [b for b in response["content"] if b["type"] == "tool_use"]
            tool_results_content = []

            for tool_use_block in tool_use_blocks:
                tool_result = self._handle_tool_use(tool_use_block)
                tool_results_content.append(
                    {"type": "tool_result", "tool_use_id": tool_use_block["id"], "content": str(tool_result)}
                )

            conversation_history.append({"role": "user", "content": tool_results_content})

            response = self.claude_client.send_message(
                messages=conversation_history, tools=tools_definitions, max_tokens=1024, system=system_prompt
            )

            iteration += 1

        final_text = next(
            (b["text"] for b in response["content"] if b["type"] == "text"), "No se pudo generar una respuesta"
        )

        perfumes_mentioned = []
        for msg in conversation_history:
            if msg["role"] == "user":
                for block in msg.get("content") or []:
                    if isinstance(block, dict) and block.get("type") == "tool_result":
                        import json

                        try:
                            result = json.loads(block["content"])
                            if isinstance(result, list):
                                perfumes_mentioned.extend(result)
                        except (json.JSONDecodeError, KeyError):
                            pass

        return {"response": final_text, "perfumes": perfumes_mentioned if perfumes_mentioned else None}

    def _handle_tool_use(self, tool_use_block: Dict[str, Any]) -> Any:
        """
        Ejecuta una tool solicitada por Claude.
        """
        tool_name = tool_use_block["name"]
        tool_input = tool_use_block["input"]

        try:
            logger.info("tool_call", extra={"tool": tool_name, "input": tool_input})
            result = self.perfume_tools.execute_tool(tool_name=tool_name, tool_input=tool_input)
            logger.debug("tool_result", extra={"tool": tool_name, "result": result})
            return result
        except Exception as e:
            logger.error("tool_error", exc_info=True, extra={"tool": tool_name})
            return {"error": f"Error ejecutando tool {tool_name}: {str(e)}"}

    def _build_system_prompt(self) -> str:
        """
        Construye el system prompt para Claude.
        """
        return (
            "Eres un asistente experto en perfumes y fragancias. "
            "Tu objetivo es ayudar a los usuarios a descubrir y elegir perfumes "
            "que se adapten a sus gustos y necesidades.\n\n"
            "Tienes acceso a un catálogo de perfumes con el que puedes:\n"
            "- Buscar perfumes por marca, notas olfativas, temporada o género (search_perfumes)\n"
            "- Obtener detalles completos de un perfume específico (get_perfume_details)\n"
            "- Recomendar perfumes similares a uno de referencia (recommend_similar)\n\n"
            "Instrucciones:\n"
            "- Usa las tools disponibles para buscar información real del catálogo antes de responder\n"
            "- SOLO recomienda perfumes que encuentres en el catálogo — "
            "nunca uses conocimiento externo al contexto recuperado\n"
            "- Sé amable, conversacional y apasionado por los perfumes\n"
            "- Cuando recomiendes perfumes, explica por qué crees que le gustarán al usuario\n"
            "- Si no encuentras resultados, sugiere alternativas o pide más información al usuario\n"
            "- Responde siempre en el idioma del usuario\n\n"
            "Antes de actuar, razona internamente qué necesita el usuario y qué tool es más adecuada. "
            "Sigue este patrón:\n\n"
            "<example>\n"
            'Usuario: "busco algo fresco para el verano"\n'
            "Razonamiento: El usuario quiere frescura y ligereza para clima cálido. "
            "Implica notas acuáticas, cítricas o verdes. "
            "No especifica género ni marca — busco en el catálogo por notas y temporada.\n"
            'Acción: search_perfumes con query "fresco verano acuático cítrico ligero"\n'
            "Respuesta: Presento los resultados explicando qué notas los hacen frescos "
            "y por qué funcionan en verano.\n"
            "</example>\n\n"
            "<example>\n"
            'Usuario: "quiero un perfume similar al Acqua di Gio pero más duradero"\n'
            "Razonamiento: El usuario tiene un perfume de referencia conocido y pide similitud + "
            "mayor duración. Mayor duración implica concentración más alta (EDP sobre EDT). "
            "Lo correcto es buscar similares al perfume de referencia, no hacer búsqueda genérica. "
            "Luego verifico detalles de los candidatos.\n"
            "Acción: recommend_similar con el perfume de referencia → "
            "get_perfume_details para verificar concentración de los candidatos top\n"
            "Respuesta: Explico qué comparten con Acqua di Gio y cuál tiene mayor duración y por qué.\n"
            "</example>"
        )
