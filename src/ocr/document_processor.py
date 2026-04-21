"""
Procesador OCR para extraer texto de imagenes.

Este modulo implementa:
- Extraccion de texto con pytesseract
- Preprocesamiento de imagenes
- Limpieza de texto extraido

DIA 11: Implementaras este modulo para expandir las capacidades del sistema.
"""

import io
import re
from typing import Dict, Any, Optional
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract


class OCRProcessor:
    """Procesador OCR para documentos de perfumes."""

    def __init__(self, tesseract_path: Optional[str] = None):
        """
        Inicializa el procesador OCR.

        Args:
            tesseract_path: Ruta al ejecutable de tesseract (opcional)
        """
        if tesseract_path:
            pytesseract.pytesseract.tesseract_cmd = tesseract_path

        try:
            pytesseract.get_tesseract_version()
        except pytesseract.TesseractNotFoundError:
            raise RuntimeError(
                "Tesseract no esta instalado o no se encuentra en el PATH. "
                "Instalalo desde https://github.com/tesseract-ocr/tesseract "
                "o proporciona la ruta con tesseract_path."
            )

        self.pytesseract = pytesseract

    def extract_text(self, image_path: str, lang: str = 'eng') -> str:
        """
        Extrae texto de una imagen.

        Args:
            image_path: Ruta a la imagen
            lang: Idioma para OCR (default: ingles)

        Returns:
            Texto extraido
        """
        image = Image.open(image_path)
        image = self.preprocess_image(image)
        raw_text = self.pytesseract.image_to_string(image, lang=lang)
        return raw_text.strip()

    def extract_from_bytes(self, image_bytes: bytes, lang: str = 'eng') -> str:
        """
        Extrae texto de bytes de imagen.

        Args:
            image_bytes: Bytes de la imagen
            lang: Idioma para OCR

        Returns:
            Texto extraido
        """
        image = Image.open(io.BytesIO(image_bytes))
        image = self.preprocess_image(image)
        raw_text = self.pytesseract.image_to_string(image, lang=lang)
        return raw_text.strip()

    def preprocess_image(self, image):
        """
        Preprocesa imagen para mejorar OCR.

        Args:
            image: Imagen PIL

        Returns:
            Imagen preprocesada
        """
        # 1. Convertir a escala de grises
        image = image.convert("L")

        # 2. Aumentar contraste
        image = ImageEnhance.Contrast(image).enhance(2.0)

        # 3. Binarizacion con threshold
        image = image.point(lambda x: 255 if x > 128 else 0)

        # 4. Redimensionar si es muy pequeña (minimo 300px de ancho)
        if image.width < 300:
            scale = 300 / image.width
            image = image.resize(
                (int(image.width * scale), int(image.height * scale)),
                Image.LANCZOS
            )

        return image

    def extract_structured_data(self, image_path: str) -> Dict[str, Any]:
        """
        Extrae y estructura datos de documentos de perfumes.

        Args:
            image_path: Ruta a la imagen

        Returns:
            Diccionario con datos extraidos
        """
        text = self.extract_text(image_path)
        lines = [l.strip() for l in text.splitlines() if l.strip()]

        TIPOS = ["parfum", "edp", "eau de parfum", "edt", "eau de toilette", "edc", "eau de cologne"]

        result: Dict[str, Any] = {
            "raw_text": text,
            "brand": None,
            "name": None,
            "size": None,
            "type": None,
        }

        for line in lines:
            line_lower = line.lower()

            if result["type"] is None:
                for tipo in TIPOS:
                    if tipo in line_lower:
                        result["type"] = line
                        break

            if result["size"] is None:
                match = re.search(r'\d+(\.\d+)?\s*(ml|oz)', line_lower)
                if match:
                    result["size"] = match.group(0)

        if lines:
            result["brand"] = lines[0]
        if len(lines) > 1:
            result["name"] = lines[1]

        return result
