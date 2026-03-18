# RAG Project

A robust Retrieval-Augmented Generation (RAG) system with a FastAPI backend and Next.js frontend, designed to handle multiple file types (PDF, EPUB, MOBI) and run locally using tools like LlamaIndex/LangChain, Qdrant, and Ollama.

## Project Structure

```text
rag-project/
├── data/                       # Raw input files (DO NOT commit)
│   ├── pdfs/
│   ├── epubs/
│   └── mobis/
├── notebooks/                  # Jupyter Lab environment for experimentation
│   └── 01_data_pipeline.ipynb  # Pipeline experimentation
├── src/                        # Core Python Backend
│   ├── pipeline/               # Data Ingestion & Processing
│   │   ├── extractors.py       # PDF/EbookLib/Mobi logic
│   │   ├── cleaners.py         # BeautifulSoup4 & regex cleaning
│   │   ├── chunkers.py         # SemanticSplitterNodeParser logic
│   │   └── enrichers.py        # Ollama metadata tagging
│   ├── store/                  # Vector Database
│   │   └── qdrant_client.py    # Qdrant connection and Hybrid Search
│   ├── engine/                 # RAG Query Logic
│   │   ├── retriever.py        # Dense + Sparse search execution
│   │   └── reranker.py         # Cross-Encoder (e.g., BAAI/bge-reranker-base)
│   ├── monitoring/             # Telemetry
│   │   └── phoenix_tracer.py   # Arize Phoenix integration
│   └── api/                    # FastAPI Application
│       ├── main.py             # FastAPI entry point
│       ├── routes.py           # /query, /ingest endpoints
│       └── models.py           # Pydantic schemas (requests/responses)
├── app/                        # Next.js Frontend
│   ├── src/
│   │   ├── components/         # React/Shadcn Components
│   │   └── app/                # Next.js pages/routing
│   ├── package.json
│   └── tailwind.config.js
├── requirements.txt            # Python dependencies
└── README.md
```

## Setup Instructions

*Instructions for setting up the environment, installing requirements, and running the project will be added here.*
