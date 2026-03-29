# Día 4: Tools para Claude (Function Calling)

## Lo que aprendí

### Qué son las Tools de un agente

Las tools son funciones externas que un modelo de IA puede invocar para extender sus capacidades más allá del texto. Un LLM por sí solo solo puede razonar sobre lo que sabe, pero con tools puede:

- Buscar en bases de datos reales
- Hacer llamadas a APIs externas
- Ejecutar cálculos precisos
- Leer o escribir archivos
- Interactuar con el mundo real

La relación entre tools y modelo es la siguiente:

```
Modelo (Claude)
    ↓ decide qué tool usar y con qué parámetros
Tool (tu código Python)
    ↓ ejecuta la lógica real y devuelve datos
Modelo (Claude)
    ↓ usa esos datos para generar una respuesta en lenguaje natural
```

El modelo nunca ejecuta código directamente. Solo dice "quiero llamar a esta función con estos parámetros" y tú eres quien la ejecuta. Esto es importante por seguridad y control.

Un agente es un sistema donde el modelo puede usar tools de forma autónoma en múltiples pasos para resolver una tarea compleja. Por ejemplo:

1. Claude recibe "recomiéndame un perfume similar al Sauvage pero más barato"
2. Llama a `get_perfume_details("dior-sauvage")` para obtener sus notas
3. Llama a `search_perfumes(notes=["bergamot", "pepper"])` para buscar similares
4. Genera una respuesta comparando los resultados

### Qué es Function Calling

Es una funcionalidad de los LLMs que les permite "pedir" ejecutar funciones de tu código en lugar de responder con texto directamente.

El flujo completo:

```
1. Envías mensaje + definiciones de tools a Claude
2. Claude responde con stop_reason="tool_use" y un bloque tool_use
3. Tú ejecutas la función con los parámetros que Claude eligió
4. Envías el resultado de vuelta a Claude
5. Claude genera la respuesta final en lenguaje natural
```

### JSON Schema

Estándar universal para describir la forma de un objeto JSON. Anthropic lo usa para que Claude entienda qué parámetros acepta cada tool:

- `type`: tipo del parámetro (string, integer, array, object)
- `description`: para que Claude entienda cuándo y cómo usarlo
- `enum`: restringe los valores posibles
- `required`: lista de parámetros obligatorios

### Python nuevo

- **Dict comprehension con filtro**: `{k: v for k, v in d.items() if v is not None}` — crea un dict filtrando valores None en una línea
- **`match/case`**: equivalente al switch/case de PHP, disponible desde Python 3.10
- **`**dict`**: desempaqueta un diccionario como argumentos nombrados. `func(\*\*{"a": 1})`es igual que`func(a=1)`
- **Slice de lista**: `lista[:n]` devuelve los primeros n elementos

### Estructura de una tool en Anthropic

```python
{
    "name": "nombre_en_snake_case",
    "description": "Qué hace la tool (Claude lee esto para decidir cuándo usarla)",
    "input_schema": {
        "type": "object",
        "properties": {
            "param1": {"type": "string", "description": "..."},
            "param2": {"type": "array", "items": {"type": "string"}}
        },
        "required": ["param1"]  # parámetros obligatorios
    }
}
```

### Formato de tool_result

Cuando Claude usa una tool, hay que devolverle el resultado en este formato exacto:

```python
{
    "role": "user",
    "content": [
        {
            "type": "tool_result",
            "tool_use_id": "id_del_tool_use",
            "content": "resultado como string"
        }
    ]
}
```

## Código implementado

- `src/tools/perfume_tools.py` → clase `PerfumeTools` completa
- `src/api/claude_client.py` → método `create_tool_result` + validación de tools en `send_message`

## Para entrevista

**¿Qué es Function Calling?**
Es un mecanismo que permite a un LLM invocar funciones externas de forma estructurada. El modelo no ejecuta código, sino que devuelve un JSON con el nombre de la función y los parámetros que quiere usar. El desarrollador ejecuta la función y devuelve el resultado al modelo para que genere la respuesta final.

**¿Por qué usar tools en lugar de pedir a Claude que genere el JSON directamente?**
Las tools garantizan que los parámetros tengan el tipo y formato correcto (validación por JSON Schema), y Claude sabe exactamente cuándo y cómo usarlas gracias a las descripciones. Es más robusto que parsear texto libre.
