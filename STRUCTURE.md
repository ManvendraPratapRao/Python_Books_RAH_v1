# Project Architecture & File Structure

This document explains the organization of the **1st RAG Project** and the purpose of each directory and file.

## 📂 Root Directory
*   `notebooks/`: **Experimentation & Prototyping**. Contains `01_data_pipeline.ipynb` where all extraction, cleaning, and RAG logic are first tested.
*   `data/`: **Raw Data Storage**. Contains the books (PDF, EPUB, MOBI) partitioned by format.
*   `qdrant_data/`: **Vector Database Storage**. Persistent storage for your Qdrant index (synced via Docker).
*   `app/`: **Frontend Application**. A Next.js/Tailwind workspace for building the user interface.
*   `requirements.txt`: Python dependencies (LlamaIndex, Qdrant, Ollama, etc.).

---

## 📂 Source Code (`src/`)
The `src/` directory is the **Production Engine**. It is designed to be modular and reusable.

### 🛠️ `pipeline/` (The Ingestion Flow)
*   `extractors.py`: Logic to convert PDF, EPUB, and MOBI into raw text.
*   `cleaners.py`: Universal text normalization (Unicode fixes, junk removal).
*   `chunkers.py`: Semantic splitting logic to break books into meaningful nodes.
*   `ingest.py` (Planned): The master script to run the whole flow from "File" to "Storable Node."

### 🧠 `engine/` (The RAG Logic)
*   `retriever.py`: Hybrid Search logic (Dense + Sparse) and BGE-Reranking.
*   `query_engine.py`: The final interface that connects the Retriever to the Ollama LLM.

### 🏢 `store/` (Database Management)
*   `qdrant_client.py`: Configuration and connection helpers for the Qdrant Docker container.

### 📈 `monitoring/` (Observability)
*   `phoenix_tracer.py`: Integration with **Arize Phoenix** for tracking query latency and retrieval accuracy.

---

## 🚀 Workflow
1.  **Develop** in `notebooks/`. 
2.  **Modularize** verified code into the corresponding `src/` files.
3.  **Deploy** via `app/` and the FastAPI backend.
