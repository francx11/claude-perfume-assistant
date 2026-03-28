# Día 3: Carga y limpieza del CSV de Fragrantica

## Lo que aprendí

### Pandas básico

- **`pd.read_csv(path)`**: carga un CSV en un DataFrame
- **`df.dropna(subset=[...])`**: elimina filas con nulos en columnas específicas
- **`df.drop_duplicates()`**: elimina filas duplicadas
- **`df['col'].str.strip().str.lower()`**: normaliza strings (quita espacios y pasa a minúsculas). `.str` da acceso a métodos de string sobre toda la columna
- **`df.set_index('col')`**: convierte una columna en índice del DataFrame, haciendo búsquedas por ese campo mucho más rápidas
- **`df.to_dict('records')`**: convierte un DataFrame a lista de diccionarios, uno por fila
- **`df.loc[key]`**: busca una fila por su índice
- **`df[df['col'].isin(lista)]`**: filtra filas cuyo valor esté en una lista
- **`df['col'].str.contains('a|b', case=False)`**: filtra filas que contengan alguno de los valores (el `|` es OR en regex)

### Manejo de errores

- **`raise`**: lanza una excepción con un mensaje claro. Mejor que dejar que Python falle con un error genérico
- El orden importa: validar columnas ANTES de intentar limpiarlas, si no el error ocurre en el lugar equivocado
- **`try/except`**: captura errores esperados (como `FileNotFoundError`) para relanzarlos con mensajes útiles

### Diseño de clases

- El `__init__` debe ser ligero: guardar atributos y delegar la lógica pesada a métodos (`load_data()`)
- Separar responsabilidades: un método carga, otro filtra, otro busca por ID

### Estructura del CSV de Fragrantica

- El campo `notes` es un **string separado por comas**, no una lista. Hay que hacer `.split(',')` o `.str.contains()` para trabajar con él
- `season` y `gender` son campos categóricos con valores fijos
- Usar `id` como índice del DataFrame acelera las búsquedas del RAG

## Código implementado

`src/data/loader.py` → clase `DataLoader` completa con todos sus métodos

## Conceptos clave para entrevista

**¿Qué es un DataFrame?**
Una estructura de datos tabular de pandas, similar a una hoja de cálculo o tabla SQL, con filas y columnas indexadas. Permite operaciones vectorizadas sobre columnas enteras sin bucles.

**¿Por qué normalizar los datos al cargar?**
Para garantizar consistencia en las búsquedas. Si un perfume tiene `brand = "DIOR"` y el usuario busca `"dior"`, sin normalización no habría match. Normalizar en la carga evita tener que hacerlo en cada consulta.

**¿Por qué usar `set_index`?**
Convierte una columna en el índice del DataFrame. Las búsquedas con `.loc[id]` son O(1) en lugar de O(n), lo que importa cuando el catálogo tiene miles de perfumes.
