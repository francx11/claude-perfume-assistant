"""
Procesador OCR para extraer texto de imágenes.

Este módulo implementa:
- Extracción de texto con pytesseract
- Preprocesamiento de imágenes
- Limpieza de texto extraído

DÍA 11: Implementarás este módulo para expandir las capacidades del sistema.
"""

from typing import Dict, Any, Optional


class OCRProcessor:
    """Procesador OCR para documentos de perfumes."""

    def __init__(self, tesseract_path: Optional[str] = None):
        """
        Inicializa el procesador OCR.

        TODO DÍA 11:
        1. Si tesseract_path se proporciona, configurar pytesseract:
           import pytesseract
           pytesseract.pytesseract.tesseract_cmd = tesseract_path
        2. Verificar que tesseract esté instalado

        Args:
            tesseract_path: Ruta al ejecutable de tesseract (opcional)
        """
        pass

    def extract_text(self, image_path: str, lang: str = 'eng') -> str:
        """
        Extrae texto de una imagen.

        TODO DÍA 11:
        1. Cargar imagen con PIL: from PIL import Image
        2. Preprocesar imagen con preprocess_image()
        3. Aplicar OCR: pytesseract.image_to_string(image, lang=lang)
        4. Limpiar texto extraído
        5. Retornar texto

        Args:
            image_path: Ruta a la imagen
            lang: Idioma para OCR (default: inglés)

        Returns:
            Texto extraído
        """
        pass

    def extract_from_bytes(self, image_bytes: bytes, lang: str = 'eng') -> str:
        """
        Extrae texto de bytes de imagen.

        TODO DÍA 11:
        1. Convertir bytes a imagen PIL: Image.open(io.BytesIO(image_bytes))
        2. Aplicar mismo proceso que extract_text()
        3. Retornar texto

        ¿Por qué necesitamos esto?
        Para procesar imágenes subidas vía API sin guardarlas en disco.

        Args:
            image_bytes: Bytes de la imagen
            lang: Idioma para OCR

        Returns:
            Texto extraído
        """
        pass

    def preprocess_image(self, image):
        """
        Preprocesa imagen para mejorar OCR.

        TODO DÍA 11:
        1. Convertir a escala de grises
        2. Aumentar contraste
        3. Aplicar threshold (binarización)
        4. Redimensionar si es muy pequeña
        5. Retornar imagen procesada

        ¿Por qué preprocesar?
        OCR funciona mejor con imágenes en blanco y negro con buen contraste.

        Args:
            image: Imagen PIL

        Returns:
            Imagen preprocesada
        """
        pass

    def extract_structured_data(self, image_path: str) -> Dict[str, Any]:
        """
        Extrae y estructura datos de documentos de perfumes.

        TODO DÍA 11:
        1. Extraer texto con extract_text()
        2. Intentar identificar campos estructurados:
           - Marca
           - Nombre del perfume
           - Tamaño
           - Tipo (EDT, EDP, etc)
        3. Retornar diccionario con datos estructurados

        Args:
            image_path: Ruta a la imagen

        Returns:
            Diccionario con datos extraídos
        """
        pass
