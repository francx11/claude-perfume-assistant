"""
Script de prueba para Día 11: OCR (Document Processor)
"""
import os
from dotenv import load_dotenv
load_dotenv()

from src.ocr.document_processor import OCRProcessor

print("=== Prueba OCR Día 11 ===\n")

# Inicializar procesador
tesseract_path = os.getenv("TESSERACT_PATH")  # None si está en el PATH
processor = OCRProcessor(tesseract_path=tesseract_path)
print("OCRProcessor inicializado correctamente\n")

# Ruta a una imagen de prueba (ajusta según tengas disponible)
IMAGE_PATH = "data/raw/test_image.jpg"

if not os.path.exists(IMAGE_PATH):
    print(f"AVISO: No se encontró imagen en '{IMAGE_PATH}'.")
    print("Coloca una imagen de prueba en esa ruta para ejecutar los tests.\n")
else:
    # 1. Extracción de texto
    print("=== Extracción de texto ===")
    texto = processor.extract_text(IMAGE_PATH)
    print(f"Texto extraído:\n{texto}\n")

    # 2. Extracción desde bytes
    print("=== Extracción desde bytes ===")
    with open(IMAGE_PATH, "rb") as f:
        image_bytes = f.read()
    texto_bytes = processor.extract_from_bytes(image_bytes)
    print(f"Texto extraído desde bytes:\n{texto_bytes}\n")

    # 3. Datos estructurados
    print("=== Datos estructurados ===")
    datos = processor.extract_structured_data(IMAGE_PATH)
    print(f"Marca:  {datos['brand']}")
    print(f"Nombre: {datos['name']}")
    print(f"Tamaño: {datos['size']}")
    print(f"Tipo:   {datos['type']}")
    print(f"Texto raw:\n{datos['raw_text']}")
