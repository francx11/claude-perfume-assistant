# Día 8: Tests con pytest

## Conceptos de testing

### Qué es pytest

Framework de testing de Python. Equivalente a PHPUnit. Ejecuta funciones que empiezan por `test_` y verifica que el código funciona correctamente.

```bash
python -m pytest tests/ -v  # ejecutar todos los tests con detalle
python -m pytest tests/test_claude_client.py -v  # ejecutar un fichero concreto
```

### `assert`

Palabra clave para verificar condiciones en tests. Si la condición es falsa, el test falla:

```python
assert client.api_key == "test-key"       # como assertEquals de PHPUnit
assert "content" in response              # como assertArrayHasKey
assert response["stop_reason"] == "tool_use"
```

### `pytest.raises`

Verifica que un bloque de código lanza una excepción concreta. Equivalente a `$this->expectException()` en PHPUnit:

```python
with pytest.raises(AuthenticationError):
    client.send_message(messages)
```

---

## Mocks

### Qué es un Mock

Un objeto falso que simula el comportamiento de uno real sin ejecutar el código real. Se usa en tests para:

- Evitar llamadas reales a APIs (coste, velocidad, dependencias externas)
- Simular respuestas de error que son difíciles de reproducir
- Verificar que se llamó a un método con los parámetros correctos

### `Mock()`

Crea un objeto falso. Puedes configurar qué devuelve cuando se llama a sus métodos:

```python
mock_response = Mock()
mock_response.model_dump.return_value = {"content": [...]}  # qué devuelve model_dump()
mock_response.side_effect = AuthenticationError(...)        # que lance una excepción
```

### `patch`

Reemplaza temporalmente una clase o función por un Mock durante el test:

```python
with patch('src.api.claude_client.Anthropic') as mock_anthropic:
    # dentro del bloque, Anthropic está reemplazado por el mock
    client = ClaudeClient(api_key="test-key")
```

### Regla crítica del patch

Siempre parchea donde se USA la clase, no donde se define:

```python
# MAL: parchea el módulo original
with patch('anthropic.Anthropic'):

# BIEN: parchea donde ClaudeClient importa Anthropic
with patch('src.api.claude_client.Anthropic'):
```

Si parcheas el módulo original pero el código ya lo importó, el mock no tiene efecto.

### `assert_called_once()`

Verifica que un método del mock fue llamado exactamente una vez:

```python
mock_anthropic.return_value.messages.create.assert_called_once()
```

### `side_effect`

Hace que el mock lance una excepción en lugar de devolver un valor:

```python
mock.side_effect = RateLimitError(message="...", response=Mock(status_code=429), body={})
```

---

## Tipos de tests implementados

- `test_init`: verifica que el constructor guarda los atributos correctamente
- `test_send_message_simple`: verifica el flujo normal con respuesta de texto
- `test_send_message_with_tools`: verifica que se maneja correctamente una respuesta con tool_use
- `test_create_tool_result`: verifica el formato del mensaje de resultado de tool
- `test_authentication_error`: verifica que se propaga el error 401
- `test_rate_limit_error`: verifica que se propaga el error 429
- `test_timeout_error`: verifica que se propaga el timeout
- `test_malformed_tools_raises_value_error`: verifica la validación de tools

---

## Para entrevista

**¿Qué es un Mock y para qué sirve?**
Un objeto que simula el comportamiento de una dependencia real sin ejecutarla. Se usa para aislar la unidad bajo test, evitar efectos secundarios (llamadas a APIs, escritura en base de datos), y simular condiciones de error difíciles de reproducir en entorno real.

**¿Qué diferencia hay entre un Mock y un Stub?**
Un Stub solo devuelve valores predefinidos. Un Mock además verifica que se llamó con los parámetros correctos (`assert_called_once`, `assert_called_with`). En Python `unittest.mock.Mock` puede hacer ambas cosas.

**¿Por qué es importante el patch correcto?**
Python importa los módulos por referencia. Si un módulo ya importó `Anthropic`, parchear `anthropic.Anthropic` no afecta a la referencia que ya tiene. Hay que parchear la referencia en el módulo que la usa: `src.api.claude_client.Anthropic`.

**¿Qué es TDD (Test Driven Development)?**
Metodología donde escribes el test antes que el código. El ciclo es: Red (test falla) → Green (implementas lo mínimo para que pase) → Refactor (mejoras el código). Garantiza que el código es testeable por diseño.
