"""
Tests para ClaudeClient.

DÍA 8: Implementarás estos tests para asegurar calidad del código.
"""

import pytest
from unittest.mock import Mock, patch


class TestClaudeClient:
    """Tests para el cliente de Claude."""

    def test_init(self):
        """
        Test de inicialización del cliente.

        TODO DÍA 8:
        1. Crear instancia de ClaudeClient con API key de prueba
        2. Verificar que se inicializa correctamente
        3. Verificar que guarda api_key y model
        """
        pass

    def test_send_message_simple(self):
        """
        Test de envío de mensaje simple.

        TODO DÍA 8:
        1. Mockear la respuesta de la API de Anthropic
        2. Crear ClaudeClient
        3. Enviar mensaje simple
        4. Verificar que la respuesta tiene el formato correcto
        5. Verificar que se llamó a la API con los parámetros correctos

        ¿Por qué mockear?
        No queremos hacer llamadas reales a la API en tests (cuesta dinero).
        Mocks simulan el comportamiento de la API.
        """
        pass

    def test_send_message_with_tools(self):
        """
        Test de envío de mensaje con tools.

        TODO DÍA 8:
        1. Mockear respuesta con tool_use
        2. Enviar mensaje con tools
        3. Verificar que la respuesta contiene tool_use
        4. Verificar formato del tool_use
        """
        pass

    def test_create_tool_result(self):
        """
        Test de creación de tool result.

        TODO DÍA 8:
        1. Crear tool result con create_tool_result()
        2. Verificar que tiene el formato correcto
        3. Verificar que contiene tool_use_id y content
        """
        pass

    def test_authentication_error(self):
        """
        Test de manejo de error de autenticación.

        TODO DÍA 8:
        1. Mockear respuesta de error 401
        2. Verificar que se lanza la excepción correcta
        3. Verificar mensaje de error
        """
        pass


# TODO DÍA 8: Agregar más tests según necesites
# - Test de rate limit
# - Test de timeout
# - Test de respuestas malformadas
