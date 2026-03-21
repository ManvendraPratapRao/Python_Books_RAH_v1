# Final V1 Roadmap: Advanced Local RAG System (PDF, EPUB, MOBI)

This plan outlines the end-to-end robust, production-ready local RAG system using LlamaIndex, Qdrant, FastAPI, and Next.js.

## V1 Architecture Additions & Explanations

> [!NOTE]
> **What is a Schema in RAG?**
> A "Schema" defines the structure of the data and metadata stored in your Vector DB. For books, our schema will include: `chunk_text`, `book_title`, `author`, `chapter`, `page_number`, and `chunk_id`. This allows us to do exact metadata filtering (e.g., "Only search within books by Author X") alongside semantic search. Yes, we are fully incorporating this into Qdrant!

> [!TIP]
> **Hardware & Performance (16GB RAM, RTX 4050 6GB VRAM)**:
> We will utilize your GPU by offloading Ollama (LLM & Embeddings) to the RTX 4050. To maximize throughput during ingestion, we will implement **Batch Processing**, processing multiple chunks simultaneously rather than one by one.

> [!IMPORTANT]
> **Hybrid Search**: Qdrant supports Hybrid Search out of the box. We will retrieve documents using a combination of **Dense Vectors** (Semantic Meaning via Ollama embeddings) and **Sparse Vectors** (BM25 Keyword Search). This is crucial for finding specific names or terms in books.

> [!IMPORTANT]
> **Missing Component Added**: To connect your Python RAG pipeline to a Next.js frontend, we *must* have an API layer. I have added **FastAPI** to the stack to serve the backend.

> [!TIP]
> **Logging & Monitoring**: We will integrate **Arize Phoenix** (or Langfuse) to trace every RAG query step (Retrieve, Rerank, Generate). Phoenix provides a local, built-in dashboard to monitor LLM performance, hallucination rates, and pipeline health.

## Proposed Changes (Final V1 Stack)

### 1. Advanced Data Pipeline (`src/pipeline/`)
- **Cleaning & Deduplication**: Removing extra whitespace, artifacts, and noise. Hashing-based removal.
- **Smart Chunking**: Implementing `SemanticSplitterNodeParser`.
- **Enrichment**: Using Ollama to summarize chunks or tag metadata (Schema).
- **Batch Processing**: Parallelizing the embedding generation to utilize the RTX 4050.
- **Quality Checks**: Implementing `Ragas` for Faithfulness and Relevancy checks.

### 2. Vector Storage & Search (`src/store/`)
- **Qdrant**: Local Qdrant instance.
- **Hybrid Search**: Dense + Sparse (BM25) search techniques.
- **Metadata Filters**: Utilizing our Book Schema.

### 3. API & Telemetry (`src/api/` & `src/monitoring/`)
- **FastAPI**: Endpoints for `/ingest`, `/query`, and `/health`.
- **Arize Phoenix**: Local instrumentation and dashboard to trace pipeline latency and quality.

### 4. Frontend (`app/`)
- **Next.js**: A modern dashboard to query books and view pipeline metrics if desired.
- **UI Framework**: Tailwind CSS + Shadcn UI.

## Final V1 Roadmap
1. **Jupyter Lab Phase**: Develop the Advanced Data Pipeline (Cleaning -> Chunking -> Enrichment -> Qdrant Ingestion).
2. **Backend Engine Phase**: Wrap the pipeline and retrieval Engine in a FastAPI service.
3. **Telemetry Phase**: Attach Arize Phoenix for pipeline tracing and monitoring.
4. **Frontend Phase**: Build the Next.js UI to interact with the FastAPI backend.
5. **Deployment Phase**: Package the system for local "ws" deployment (Web Server / Web Socket).
## Verification Plan

### Automated Tests
1. **Pipeline Test**: A script to verify that cleaning, chunking, and enrichment work on a subset of the books.
2. **Store Test**: Verify that Qdrant is correctly indexing and retrieving with metadata filters.

### Manual Verification
1. **User Evaluation**: Run the initial Jupyter Lab notebook to inspect the quality of the cleaned and chunked data before indexing the full library.
2. **Next.js App**: Verify the UI connects to the local Python backend.
