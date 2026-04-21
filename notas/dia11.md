# Día 11: OCR con Tesseract y pytesseract

## Qué es OCR

OCR (Optical Character Recognition) es la tecnología que extrae texto de imágenes. En lugar de leer un archivo de texto, analiza píxeles y reconoce caracteres.

Casos de uso en este proyecto: leer etiquetas de frascos de perfume, cajas, facturas o cualquier documento físico para incorporarlo al sistema.

---

## Tesseract vs pytesseract

Son dos cosas distintas que trabajan juntas:

- **Tesseract**: el motor OCR, un ejecutable de C++ desarrollado por HP y mantenido por Google. Es el que realmente procesa las imágenes.
- **pytesseract**: wrapper de Python que llama al ejecutable de Tesseract. Sin Tesseract instalado, pytesseract no funciona.

```bash
pip show pytesseract   # comprueba si el wrapper Python está instalado
where tesseract        # comprueba si el ejecutable está en el PATH
tesseract --version    # comprueba la versión del ejecutable
```

### Instalación en Windows

1. Descargar el instalador desde https://github.com/UB-Mannheim/tesseract/wiki
2. Añadir `C:\Program Files\Tesseract-OCR` al PATH del sistema
3. O bien configurar la ruta directamente en el código:

```python
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe"
```

---

## PIL / Pillow

Librería de Python para manipulación de imágenes. Necesaria para cargar y preprocesar imágenes antes de pasarlas a Tesseract.

```python
from PIL import Image, ImageEnhance, ImageFilter

image = Image.open("foto.jpg")          # cargar desde archivo
image = Image.open(io.BytesIO(bytes))   # cargar desde bytes (útil en APIs)
image = image.convert("L")             # convertir a escala de grises
```

### Por qué `io.BytesIO`

Cuando recibes una imagen vía API (upload), llega como bytes en memoria. `io.BytesIO` convierte esos bytes en un objeto que PIL puede leer como si fuera un archivo, sin necesidad de guardarlo en disco.

```python
import io
image = Image.open(io.BytesIO(image_bytes))
```

---

## Preprocesamiento de imágenes para OCR

Tesseract funciona mejor con imágenes en blanco y negro, alto contraste y buena resolución. El preprocesamiento mejora significativamente los resultados:

```python
from PIL import ImageEnhance

# 1. Escala de grises
image = image.convert("L")

# 2. Aumentar contraste (2.0 = doble de contraste)
image = ImageEnhance.Contrast(image).enhance(2.0)

# 3. Binarización: cada píxel pasa a blanco o negro
image = image.point(lambda x: 255 if x > 128 else 0)

# 4. Redimensionar si es muy pequeña
if image.width < 300:
    scale = 300 / image.width
    image = image.resize(
        (int(image.width * scale), int(image.height * scale)),
        Image.LANCZOS
    )
```

### Por qué el threshold en 128

El rango de grises va de 0 (negro) a 255 (blanco). El valor 128 es el punto medio — píxeles más oscuros se vuelven negros, más claros se vuelven blancos. Se puede ajustar según la imagen.

### Limitaciones del OCR tradicional

Tesseract funciona bien con documentos planos (facturas, libros escaneados). Tiene dificultades con:

- Texto sobre fondos con reflejos o gradientes (frascos de perfume)
- Texto en superficies curvas
- Fuentes decorativas o muy pequeñas

Para estos casos, la visión de Claude (multimodal) es mucho más robusta.

---

## Concentraciones de perfume (EDT, EDP, etc.)

Términos que aparecen en etiquetas y que el OCR debe reconocer:

| Sigla  | Nombre completo   | Concentración | Duración |
| ------ | ----------------- | ------------- | -------- |
| EDC    | Eau de Cologne    | ~3%           | 2-3h     |
| EDT    | Eau de Toilette   | 5-15%         | 3-4h     |
| EDP    | Eau de Parfum     | 15-20%        | 5-8h     |
| Parfum | Extrait de Parfum | 20-30%        | 8h+      |

---

## Extracción de datos estructurados con regex

Una vez extraído el texto, se puede parsear con expresiones regulares para identificar campos concretos:

```python
import re

# Detectar tamaño: "100ml", "50 ml", "1.7 oz"
match = re.search(r'\d+(\.\d+)?\s*(ml|oz)', texto.lower())
if match:
    size = match.group(0)

# Detectar tipo de concentración
TIPOS = ["parfum", "edp", "eau de parfum", "edt", "eau de toilette", "edc", "eau de cologne"]
for tipo in TIPOS:
    if tipo in texto.lower():
        tipo_encontrado = tipo
        break
```

---

## Imports en Python: buenas prácticas

Los imports siempre van al principio del fichero, no dentro de funciones o métodos. Esto es una convención de estilo (PEP8) y mejora la legibilidad:

```python
# Correcto
import io
import re
from PIL import Image
import pytesseract

class OCRProcessor:
    def extract_text(self, path):
        image = Image.open(path)  # ya disponible
```

La única excepción aceptada es cuando la importación es opcional o muy costosa y solo se necesita en casos específicos, pero debe estar justificada.

---

## Para entrevista

**¿Qué es OCR?**
Optical Character Recognition. Tecnología que analiza píxeles de una imagen para identificar y extraer caracteres de texto. Tesseract es el motor open source de referencia, mantenido por Google.

**¿Por qué preprocesar la imagen antes del OCR?**
Tesseract está optimizado para texto negro sobre fondo blanco con buen contraste. El preprocesamiento (escala de grises, aumento de contraste, binarización) elimina ruido visual y mejora la tasa de reconocimiento, especialmente en imágenes de baja calidad.

**¿Cuándo usar Tesseract vs visión multimodal (Claude, GPT-4V)?**
Tesseract es rápido, gratuito y funciona offline. Es ideal para documentos planos y estructurados (facturas, formularios escaneados). Los modelos multimodales son más robustos para texto en contextos complejos (superficies curvas, fondos con ruido, fuentes decorativas) pero tienen coste por llamada a API y requieren conexión.

**¿Qué es `io.BytesIO` y para qué sirve?**
Es un buffer en memoria que simula un archivo. Permite trabajar con datos binarios (como bytes de una imagen recibida por API) usando la misma interfaz que si fuera un archivo en disco, sin necesidad de escritura temporal.

**¿Cómo expones OCR en una API REST?**
Con FastAPI, el endpoint recibe un `UploadFile`, validas el `content_type` para asegurarte de que es una imagen, lees los bytes con `await file.read()` y los pasas al procesador. Nunca guardas el archivo en disco si no es necesario.
