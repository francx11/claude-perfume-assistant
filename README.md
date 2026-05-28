# PerfumeShop AI

Conversational perfume recommendation system powered by Claude API, RAG, and a Fragrantica catalog.

## What it does

- Understands natural language queries ("fresh summer perfume", "something like Dior Sauvage")
- Searches and filters a Fragrantica catalog using semantic embeddings (FAISS + ChromaDB + HyDE)
- Returns personalized recommendations via Claude's reasoning and tool use
- Extracts perfume data from images using OCR
- Persists conversation sessions with SQLite logging
- Syncs CSV and embeddings from AWS S3 on startup

## Architecture

```
React Frontend (Vite + TypeScript)
        ↓ HTTP
FastAPI  (api/endpoints.py)
        ↓
OrchestratorAgent  (tool-use loop, max 5 iter)
        ↓                          ↓
ClaudeClient               PerfumeTools
(src/api)                  (src/tools)
                                   ↓
                      FAISSRetriever / ChromaRetriever / HyDERetriever
                                   ↓
                      EmbeddingsGenerator (sentence-transformers)
                                   ↓
                            DataLoader → Fragrantica CSV
                                   ↓
                              S3Client (CSV + embeddings sync)
```

Session state: `SessionStore` (in-memory) + `ConversationLogger` (SQLite at `db/chat.db`)

## Tech Stack

| Technology | Purpose |
|---|---|
| Claude API (`anthropic`) | NLU, generation, tool use |
| FastAPI + uvicorn | REST API layer |
| sentence-transformers | Semantic embeddings |
| FAISS | Vector index for similarity search |
| ChromaDB | Alternative vector store |
| HyDE | Hypothetical document embeddings retrieval |
| SQLite | Conversation history persistence |
| AWS S3 (boto3) | Remote storage for CSV and embeddings |
| React + Vite + TypeScript | Frontend chat UI |
| Zustand | Frontend state management |
| pytesseract + Pillow | OCR for image-based perfume data |
| pytest | Unit and integration tests |
| Terraform | Infrastructure as code |
| Kubernetes | Container orchestration manifests |

## Project Structure

```
perfumeshop-ai/
├── api/
│   └── endpoints.py         # FastAPI app, routes, startup
├── src/
│   ├── agents/
│   │   └── orchestrator.py  # Tool-use loop, conversation driver
│   ├── api/
│   │   ├── claude_client.py
│   │   ├── session_store.py        # In-memory session history
│   │   └── conversation_logger.py  # SQLite turn logging
│   ├── data/
│   │   └── loader.py        # Fragrantica CSV loading and filtering
│   ├── rag/
│   │   ├── embeddings.py
│   │   ├── faiss_retriever.py
│   │   ├── chroma_retriever.py
│   │   ├── hyde_retriever.py
│   │   └── retriever.py     # Base class
│   ├── ocr/
│   │   └── document_processor.py
│   ├── storage/
│   │   └── s3_client.py
│   └── tools/
│       └── perfume_tools.py # Claude tool definitions + dispatch
├── frontend/
│   └── src/
│       ├── components/      # ChatInput, ChatWindow, MessageList,
│       │                    #   MessageBubble, PerfumeCard,
│       │                    #   Sidebar, TypingIndicator
│       ├── services/
│       │   └── api.ts
│       └── store/
│           └── chatStore.ts
├── data/
│   ├── raw/                 # Fragrantica CSV (not committed)
│   └── embeddings/          # .npy + FAISS index (generated)
├── db/
│   └── chat.db              # SQLite conversation log
├── infra/
│   └── main.tf              # Terraform (AWS)
├── k8s/                     # Kubernetes manifests
├── tests/
├── study-plan/              # Phase-based study docs
├── progress/
│   └── tracker.md
└── notas/                   # Learning notes (Spanish, days 1–11)
```

## Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+ (for frontend)
- Anthropic API key — [console.anthropic.com](https://console.anthropic.com)
- Tesseract installed (for OCR)
- AWS credentials configured (for S3 sync)

### Backend

```bash
# 1. Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate          # Windows PowerShell
source .venv/bin/activate       # macOS / Linux

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Set ANTHROPIC_API_KEY, CSV_PATH, S3_BUCKET_NAME, TESSERACT_PATH

# 4. Start API
python main.py
# or
uvicorn api.endpoints:app --reload
```

API docs: `http://localhost:8000/docs`

### Frontend

```bash
cd frontend
npm install   # or pnpm install
npm run dev
```

Frontend: `http://localhost:5173`

## API Endpoints

| Method | Path | Description |
|---|---|---|
| `POST` | `/chat` | Send a message, returns recommendation + session id |
| `POST` | `/ocr/extract` | Upload image, returns extracted text |
| `GET` | `/perfumes/{id}` | Lookup a perfume by id |
| `GET` | `/sessions` | List sessions (optional `?client_id=`) |
| `GET` | `/sessions/{id}/history` | Get turns for a session |
| `GET` | `/health` | Health check |

## Development

```bash
pytest tests/                      # run all tests
pytest tests/ -v -k "test_name"    # single test
```

## Roadmap

- [x] Day 1 — Claude API basic connection
- [x] Day 3 — Fragrantica CSV loading and cleaning
- [x] Day 4 — Claude tools (search, filter, recommend)
- [x] Day 5 — FastAPI endpoints
- [x] Day 6 — Conversational orchestrator
- [x] Day 7 — Embeddings and semantic search (RAG / FAISS)
- [x] Day 8 — pytest test suite
- [x] Day 11 — OCR pipeline
- [x] Session persistence (in-memory + SQLite logging)
- [x] React frontend with sidebar and session history
- [x] ChromaDB and HyDE retrieval strategies
- [x] AWS S3 integration (CSV + embeddings sync)
- [x] Terraform + Kubernetes infra

## License

MIT
