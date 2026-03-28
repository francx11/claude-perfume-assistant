"""
Orquestador del flujo conversacional.

Este módulo coordina:
- Interacción entre usuario y Claude
- Ejecución de tools
- Manejo de contexto conversacional
- Gestión de errores

DÍA 6: Implementarás este módulo para integrar todos los componentes.
"""

from typing import List, Dict, Any, Optional


class OrchestratorAgent:
    """Orquestador del asistente conversacional."""

    def __init__(self, claude_client, perfume_tools, ocr_processor=None):
        """
        Inicializa el orquestador.

        TODO DÍA 6:
        1. Guardar claude_client, perfume_tools, y ocr_processor como atributos
        2. Inicializar self.conversation_history = []

        Args:
            claude_client: Instancia de ClaudeClient
            perfume_tools: Instancia de PerfumeTools
            ocr_processor: Instancia de OCRProcessor (opcional, día 11)
        """
        pass

    def process_query(
        self,
        user_message: str,
        conversation_history: Optional[List[Dict]] = None
    ) -> Dict[str, Any]:
        """
        Procesa una consulta del usuario y retorna respuesta.

        TODO DÍA 6:
        1. Si conversation_history es None, usar lista vacía
        2. Agregar mensaje del usuario a la historia
        3. Construir system prompt con _build_system_prompt()
        4. Obtener definiciones de tools con perfume_tools.get_tools_definitions()
        5. Enviar mensaje a Claude con claude_client.send_message()
        6. Procesar respuesta:
           - Si contiene tool_use, ejecutar con _handle_tool_use()
           - Enviar resultado a Claude
           - Repetir hasta obtener respuesta de texto (máximo 5 iteraciones)
        7. Retornar diccionario con respuesta y perfumes mencionados

        ¿Qué es el tool_use loop?
        Claude puede pedir ejecutar una tool, luego otra, y así sucesivamente.
        Debemos manejar este flujo iterativo hasta que Claude dé una respuesta final.

        Args:
            user_message: Mensaje del usuario
            conversation_history: Historia previa (opcional)

        Returns:
            {
                "response": "Respuesta de Claude",
                "perfumes": [...],  # Si se mencionaron perfumes
                "conversation_id": "..."
            }
        """
        pass

    def _handle_tool_use(self, tool_use_block: Dict[str, Any]) -> Any:
        """
        Ejecuta una tool solicitada por Claude.

        TODO DÍA 6:
        1. Extraer tool_name y tool_input del tool_use_block
        2. Llamar a perfume_tools.execute_tool(tool_name, tool_input)
        3. Retornar el resultado
        4. Manejar errores y retornar mensaje de error si falla

        Args:
            tool_use_block: Bloque de tool_use de la respuesta de Claude

        Returns:
            Resultado de ejecutar la tool
        """
        pass

    def _build_system_prompt(self) -> str:
        """
        Construye el system prompt para Claude.

        TODO DÍA 6:
        1. Crear un prompt que explique el rol de Claude:
           - Eres un asistente experto en perfumes
           - Ayudas a usuarios a descubrir perfumes
           - Usas las tools disponibles para buscar información
           - Eres amable y conversacional
        2. Incluir instrucciones sobre cómo usar las tools
        3. Retornar el prompt como string

        ¿Por qué es importante el system prompt?
        Define el comportamiento y personalidad de Claude.
        Un buen prompt mejora mucho la calidad de las respuestas.

        Returns:
            System prompt como string
        """
        pass
