# Día 1: Conexión básica con Claude API

## Lo que aprendí

### Python básico

- **Atributos de instancia**: se guardan en `__init__` usando `self.atributo = valor`, accesibles desde cualquier método de la clase
- **`pass`**: placeholder para bloques vacíos, se reemplaza con la implementación real
- **`None` checks**: usar `if x is not None` es más preciso que `if x` porque distingue entre `None` y lista vacía `[]`
- **Kwargs dinámicos**: con `**{"key": value}` puedes pasar argumentos opcionales a una función en una sola línea

### Entorno y configuración

- **Entorno virtual**: aisla las dependencias del proyecto del sistema global
- **`python-dotenv`**: carga variables del `.env` como variables de entorno, evitando hardcodear credenciales en el código
- **`.env` en `.gitignore`**: las credenciales nunca van al repositorio

### Claude API

- La librería `anthropic` expone `client.messages.create()` para enviar mensajes
- Los mensajes tienen formato `[{"role": "user", "content": "..."}]`
- La respuesta es un objeto que se convierte a dict con `.model_dump()`
- El texto de la respuesta está en `response["content"][0]["text"]`

## Código implementado

`src/api/claude_client.py` → métodos `__init__` y `send_message`

## Problemas resueltos

- Conflicto de versiones `anthropic` + `httpx` → solución: `pip install httpx==0.27.0`
- Modelo no disponible en la cuenta → usar el modelo correcto de los disponibles en tu API key
