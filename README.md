# PerfumeShop AI

An intelligent conversational assistant that helps users discover and get perfume recommendations from a Fragrantica catalog. Built with Claude API, RAG, Function Calling, and OCR.

## What it does

- Understands natural language queries like "I'm looking for a fresh summer perfume"
- Searches and filters a perfume catalog semantically using embeddings
- Returns personalized recommendations via Claude's reasoning
- Extracts perfume data from images using OCR

## Tech Stack

| Technology                                            | Purpose                                       |
| ----------------------------------------------------- | --------------------------------------------- |
| [Claude API](https://www.anthropic.com)               | Natural language understanding and generation |
| [FastAPI](https://fastapi.tiangolo.com)               | REST API layer                                |
| [sentence-transformers](https://www.sbert.net)        | Semantic embeddings for RAG                   |
| [pytesseract](https://github.com/madmaze/pytesseract) | OCR for document processing                   |
| pandas                                                | Data loading and filtering                    |

## Architecture

```
User → FastAPI → Orchestrator Agent → Claude API
                        ↓                  ↓
                  Perfume Tools       Function Calling
                        ↓
                  RAG Retriever → Embeddings → Vector Search
                        ↓
                   Data Loader → Fragrantica CSV
```

## Project Structure

```
perfumeshop-ai/
├── src/
│   ├── api/          # Claude API client
│   ├── agents/       # Conversational orchestrator
│   ├── tools/        # Claude tools (search, filter, recommend)
│   ├── rag/          # Embeddings + semantic retriever
│   ├── data/         # CSV loader and data management
│   └── ocr/          # Document processing with pytesseract
├── api/              # FastAPI endpoints
├── data/raw/         # Fragrantica catalog (CSV)
├── tests/            # Unit and integration tests
└── notas/            # Learning notes (Spanish)
```

## Getting Started

### Prerequisites

- Python 3.10+
- An [Anthropic API key](https://console.anthropic.com)
- Tesseract installed (for OCR features)

### Installation

> **New to Python?** Here's what you need to know first:
>
> - **pip** is Python's package manager, like npm for Node.js. It installs libraries your project depends on.
> - **venv** (virtual environment) is an isolated Python installation per project, so dependencies don't conflict between projects. Always use one.

```bash
# 1. Clone the repo
git clone https://github.com/your-username/perfumeshop-ai.git
cd perfumeshop-ai

# 2. Create a virtual environment (isolated Python sandbox for this project)
python -m venv .venv

# 3. Activate it — you must do this every time you open a new terminal
source .venv/bin/activate        # macOS / Linux
.venv\Scripts\activate           # Windows (PowerShell)
.venv\Scripts\activate.bat       # Windows (CMD)

# You'll know it's active when you see (.venv) at the start of your terminal prompt

# 4. Install all dependencies listed in requirements.txt
pip install -r requirements.txt

# 5. Fix a known version conflict between anthropic and httpx
pip install httpx==0.27.0

# 6. Configure environment variables
cp .env.example .env
# Open .env and replace the placeholder with your real Anthropic API key
# Get one at: https://console.anthropic.com
```

### Run the API

```bash
python main.py
# or
uvicorn api.endpoints:app --reload
```

API docs available at `http://localhost:8000/docs`

## Development Roadmap

- [x] Day 1 — Claude API basic connection
- [ ] Day 3 — Fragrantica CSV loading and cleaning
- [ ] Day 4 — Claude tools (search, filter, recommend)
- [ ] Day 5 — FastAPI endpoints
- [ ] Day 6 — Conversational orchestrator
- [ ] Day 7 — Embeddings and semantic search (RAG)
- [ ] Day 8 — pytest test suite
- [ ] Day 11 — OCR pipeline

## License

MIT
