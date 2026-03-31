"""
Endpoints de la API REST con FastAPI.

Este módulo expone:
- Endpoint de chat
- Endpoint de OCR
- Endpoint de consulta de perfumes
- Health check

DÍA 5: Implementarás estos endpoints para exponer tu sistema vía HTTP.
"""
import os 
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, HTTPException, Request
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

from src.api.claude_client import ClaudeClient
from src.data.loader import DataLoader
from src.tools.perfume_tools import PerfumeTools
from src.agents.orchestrator import OrchestratorAgent


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

@app.on_event("startup")
async def startup_event():
    load_dotenv()

    claude_client = ClaudeClient(api_key=os.getenv("ANTHROPIC_API_KEY"))
    data_loader = DataLoader(csv_path=os.getenv("CSV_PATH"))
    perfume_tools = PerfumeTools(data_loader=data_loader)
    orchestrator = OrchestratorAgent(
        claude_client=claude_client,
        perfume_tools=perfume_tools
    )

    app.state.orchestrator = orchestrator
    app.state.data_loader = data_loader
    app.state.perfume_tools = perfume_tools

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, http_request: Request) -> ChatResponse:
    """
    Endpoint principal de chat.
    """
    try:
        result = http_request.app.state.orchestrator.process_query(request.message)
        return ChatResponse(
            response=result["response"],
            perfumes=result.get("perfumes"),
            conversation_id=request.conversation_id or "default"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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
    """
    try:
        result = app.state.data_loader.get_perfume_by_id(perfume_id)
        if result is None:
            raise HTTPException(status_code=404, detail=f"Perfume '{perfume_id}' no encontrado")
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check() -> Dict[str, str]:
    """
    Health check del servicio.
    """
    try:
        orchestrator = app.state.orchestrator
        data_loader = app.state.data_loader
        return {"status": "ok", "message": "PerfumeShop AI API is running"}
    except AttributeError:
        return {"status": "error", "message": "Components not initialized"}

@app.post("/search")
async def search(
    brand: Optional[str] = None,
    season: Optional[str] = None,
    gender: Optional[str] = None,
    notes: Optional[str] = None  # ej: "citrus,fresh" separado por comas
) -> List[Dict[str, Any]]:
    try:
        filters = {
            k: v for k, v in {
                "brand": brand,
                "notes": notes.split(",") if notes else None,
                "season": season,
                "gender": gender
            }.items() if v is not None
        }
        results = app.state.data_loader.filter_perfumes(filters)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/perfumes")
async def get_all_perfumes() -> List[Dict[str, Any]]:
    try:
        result = app.state.data_loader.get_all_perfumes()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/perfumes/{perfume_id}/similar")
async def get_similar_perfumes(perfume_id: str, top_k: int = 3) -> List[Dict[str, Any]]:
    try:
        result = app.state.perfume_tools.recommend_similar(perfume_id, top_k)
        if "error" in result:
            raise HTTPException(status_code=503, detail=result["error"])
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
