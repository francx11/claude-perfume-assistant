"""
Endpoints de la API REST con FastAPI.

Este módulo expone:
- Endpoint de chat
- Endpoint de OCR
- Endpoint de consulta de perfumes
- Health check

DÍA 5: Implementarás estos endpoints para exponer tu sistema vía HTTP.
"""

import logging
import os
import uuid
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.agents.orchestrator import OrchestratorAgent
from src.api.claude_client import ClaudeClient
from src.api.conversation_logger import ConversationLogger
from src.api.session_store import SessionStore
from src.data.loader import DataLoader
from src.ocr.document_processor import OCRProcessor
from src.rag.embeddings import EmbeddingsGenerator
from src.rag.faiss_retriever import FAISSRetriever
from src.storage.s3_client import S3Client
from src.tools.perfume_tools import PerfumeTools

_LOG_FORMAT = "%(asctime)s %(levelname)s %(name)s %(message)s"


def _configure_logging() -> None:
    """Configure root logger with INFO level and src.* loggers with DEBUG."""
    logging.basicConfig(level=logging.INFO, format=_LOG_FORMAT)
    logging.getLogger("src").setLevel(logging.DEBUG)


class ChatRequest(BaseModel):
    """Modelo de request para el endpoint de chat."""

    message: str
    conversation_id: Optional[str] = None
    client_id: Optional[str] = None


class ChatResponse(BaseModel):
    """Modelo de response para el endpoint de chat."""

    response: str
    perfumes: Optional[List[Dict[str, Any]]] = None
    conversation_id: str


# Crear aplicación FastAPI
app = FastAPI(title="PerfumeShop AI API", description="API para asistente conversacional de perfumes", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Initialize all application components and configure logging."""
    load_dotenv()
    _configure_logging()

    s3 = S3Client(bucket_name=os.getenv("S3_BUCKET_NAME"))
    csv_path = os.getenv("CSV_PATH")
    embeddings_path = "data/embeddings/perfumes.npy"
    if not os.path.exists(csv_path):
        s3.download_file("data/fragrantica.csv", csv_path)
    if not os.path.exists(embeddings_path):
        s3.download_file("embeddings/perfumes.npy", embeddings_path)

    claude_client = ClaudeClient(api_key=os.getenv("ANTHROPIC_API_KEY"))
    data_loader = DataLoader(csv_path=os.getenv("CSV_PATH"))

    embeddings_generator = EmbeddingsGenerator()
    rag_retriever = FAISSRetriever(embeddings_generator=embeddings_generator, data_loader=data_loader)
    rag_retriever.build_index(data_loader.get_all_perfumes(), csv_path=os.getenv("CSV_PATH"))

    perfume_tools = PerfumeTools(data_loader=data_loader, rag_retriever=rag_retriever)
    orchestrator = OrchestratorAgent(claude_client=claude_client, perfume_tools=perfume_tools)

    ocr_processor = OCRProcessor(tesseract_path=os.getenv("TESSERACT_PATH"))

    app.state.orchestrator = orchestrator
    app.state.data_loader = data_loader
    app.state.perfume_tools = perfume_tools
    app.state.ocr_processor = ocr_processor
    app.state.session_store = SessionStore()
    app.state.conversation_logger = ConversationLogger()


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, http_request: Request) -> ChatResponse:
    """
    Endpoint principal de chat.
    """
    try:
        conv_id = request.conversation_id or str(uuid.uuid4())
        session_store: SessionStore = http_request.app.state.session_store
        history = session_store.get(conv_id)
        result = http_request.app.state.orchestrator.process_query(request.message, conversation_history=history)
        session_store.save(conv_id, history)
        conv_logger: ConversationLogger = http_request.app.state.conversation_logger
        conv_logger.log(conv_id, "user", request.message, client_id=request.client_id)
        conv_logger.log(conv_id, "assistant", result["response"], client_id=request.client_id)
        return ChatResponse(
            response=result["response"],
            perfumes=result.get("perfumes"),
            conversation_id=conv_id,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/ocr/extract")
async def extract_text_from_image(file: UploadFile, http_request: Request) -> Dict[str, Any]:
    """
    Extrae texto de imagen subida.
    """
    ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png", "image/webp", "image/tiff", "image/bmp"}

    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Tipo no válido: '{file.content_type}'. Se esperaba jpeg, png, webp, tiff o bmp.",
        )

    try:
        image_bytes = await file.read()
        text = http_request.app.state.ocr_processor.extract_from_bytes(image_bytes)
        return {"filename": file.filename, "extracted_text": text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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


@app.get("/sessions")
async def list_sessions(http_request: Request, client_id: Optional[str] = None) -> List[Dict[str, Any]]:
    """Returns sessions for a client, ordered by most recent activity."""
    try:
        conv_logger: ConversationLogger = http_request.app.state.conversation_logger
        return conv_logger.list_sessions(client_id=client_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/sessions/{conversation_id}/history")
async def get_session_history(conversation_id: str, http_request: Request) -> List[Dict[str, Any]]:
    """Returns logged turns for a session in chronological order."""
    try:
        conv_logger: ConversationLogger = http_request.app.state.conversation_logger
        return conv_logger.get_history(conversation_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check() -> Dict[str, str]:
    """
    Health check del servicio.
    """
    try:
        _ = app.state.orchestrator
        return {"status": "ok", "message": "PerfumeShop AI API is running"}
    except AttributeError:
        return {"status": "error", "message": "Components not initialized"}


@app.post("/search")
async def search(
    brand: Optional[str] = None,
    season: Optional[str] = None,
    gender: Optional[str] = None,
    notes: Optional[str] = None,  # ej: "citrus,fresh" separado por comas
) -> List[Dict[str, Any]]:
    """Busca perfumes por marca, temporada, género y notas."""
    try:
        filters = {
            k: v
            for k, v in {
                "brand": brand,
                "notes": notes.split(",") if notes else None,
                "season": season,
                "gender": gender,
            }.items()
            if v is not None
        }
        results = app.state.data_loader.filter_perfumes(filters)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/perfumes")
async def get_all_perfumes() -> List[Dict[str, Any]]:
    """Retorna todos los perfumes del catálogo."""
    try:
        result = app.state.data_loader.get_all_perfumes()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/perfumes/{perfume_id}/similar")
async def get_similar_perfumes(perfume_id: str, top_k: int = 3) -> List[Dict[str, Any]]:
    """Retorna los top_k perfumes más similares al perfume dado."""
    try:
        result = app.state.perfume_tools.recommend_similar(perfume_id, top_k)
        if "error" in result:
            raise HTTPException(status_code=503, detail=result["error"])
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
