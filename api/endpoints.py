"""
Endpoints de la API REST con FastAPI.

Este módulo expone:
- Endpoint de chat
- Endpoint de OCR
- Endpoint de consulta de perfumes
- Health check

DÍA 5: Implementarás estos endpoints para exponer tu sistema vía HTTP.
"""

from fastapi import FastAPI, UploadFile, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

# TODO DÍA 5: Importar tus módulos
# from src.api.claude_client import ClaudeClient
# from src.data.loader import DataLoader
# from src.tools.perfume_tools import PerfumeTools
# from src.agents.orchestrator import OrchestratorAgent


class ChatRequest(BaseModel):
    """Modelo de request para el endpoint de chat."""
    message: str
    conversation_id: Optional[str] = None


class ChatResponse(BaseModel):
    """Modelo de response para el endpoint de chat."""
    response: str
    perfumes: Optional[List[Dict[str, Any]]] = None
    conversation_id: str


# Crear aplicación FastAPI
app = FastAPI(
    title="PerfumeShop AI API",
    description="API para asistente conversacional de perfumes",
    version="1.0.0"
)


# TODO DÍA 5: Inicializar componentes al inicio de la aplicación
# @app.on_event("startup")
# async def startup_event():
#     """Inicializa componentes al arrancar la API."""
#     # 1. Cargar variables de entorno
#     # 2. Inicializar ClaudeClient
#     # 3. Inicializar DataLoader
#     # 4. Inicializar PerfumeTools
#     # 5. Inicializar OrchestratorAgent
#     # 6. Guardar en app.state para acceso global
#     pass


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """
    Endpoint principal de chat.

    TODO DÍA 5:
    1. Obtener orchestrator desde app.state
    2. Llamar a orchestrator.process_query(request.message)
    3. Construir ChatResponse con el resultado
    4. Retornar respuesta

    Args:
        request: ChatRequest con mensaje del usuario

    Returns:
        ChatResponse con respuesta del asistente

    Raises:
        HTTPException: Si hay error en el procesamiento
    """
    # TODO: Implementar
    raise HTTPException(status_code=501, detail="Endpoint no implementado aún")


@app.post("/ocr/extract")
async def extract_text_from_image(file: UploadFile) -> Dict[str, Any]:
    """
    Extrae texto de imagen subida.

    TODO DÍA 11 (no día 5):
    1. Validar que file sea una imagen
    2. Leer bytes del archivo
    3. Llamar a ocr_processor.extract_from_bytes()
    4. Retornar texto extraído

    Args:
        file: Archivo de imagen subido

    Returns:
        Diccionario con texto extraído

    Raises:
        HTTPException: Si el archivo no es válido o hay error en OCR
    """
    # TODO: Implementar en día 11
    raise HTTPException(status_code=501, detail="Endpoint no implementado aún")


@app.get("/perfumes/{perfume_id}")
async def get_perfume(perfume_id: str) -> Dict[str, Any]:
    """
    Obtiene detalles de un perfume.

    TODO DÍA 5:
    1. Obtener data_loader desde app.state
    2. Llamar a data_loader.get_perfume_by_id(perfume_id)
    3. Si no existe, lanzar HTTPException 404
    4. Retornar datos del perfume

    Args:
        perfume_id: ID del perfume

    Returns:
        Diccionario con datos del perfume

    Raises:
        HTTPException: Si el perfume no existe
    """
    # TODO: Implementar
    raise HTTPException(status_code=501, detail="Endpoint no implementado aún")


@app.get("/health")
async def health_check() -> Dict[str, str]:
    """
    Health check del servicio.

    TODO DÍA 5:
    1. Verificar que componentes estén inicializados
    2. Retornar status "ok" si todo está bien
    3. Retornar status "error" si algo falla

    Returns:
        Diccionario con status del servicio
    """
    return {"status": "ok", "message": "PerfumeShop AI API is running"}


# TODO DÍA 5: Agregar más endpoints según necesites
# Ejemplos:
# - POST /search: Búsqueda de perfumes
# - GET /perfumes: Listar todos los perfumes
# - POST /recommend: Recomendaciones personalizadas
