rag-platform/
│
├── app/
│   ├── api/
│   │   ├── routes.py
│   │   ├── dependencies.py
│   │   └── schemas.py
│   │
│   ├── ingestion/
│   │   ├── loader.py
│   │   ├── chunking.py
│   │   ├── entity_extraction.py
│   │   └── pipeline.py
│   │
│   ├── retrieval/
│   │   ├── vector_search.py
│   │   ├── bm25_search.py
│   │   ├── hybrid_search.py
│   │   └── reranker.py
│   │
│   ├── graph_rag/
│   │   ├── graph_builder.py
│   │   ├── graph_retriever.py
│   │   └── entity_linker.py
│   │
│   ├── query_processing/
│   │   ├── query_rewriter.py
│   │   ├── keyword_extractor.py
│   │   └── intent_detector.py
│   │
│   ├── llm/
│   │   ├── model_router.py
│   │   ├── openai_provider.py
│   │   ├── local_llm.py
│   │   └── prompt_builder.py
│   │
│   ├── evaluation/
│   │   ├── ragas_eval.py
│   │   ├── metrics.py
│   │   └── benchmark.py
│   │
│   ├── monitoring/
│   │   ├── logging.py
│   │   ├── tracing.py
│   │   └── metrics.py
│   │
│   ├── cache/
│   │   └── redis_cache.py
│   │
│   └── core/
│       ├── config.py
│       ├── settings.py
│       └── constants.py
│
├── tests/
│   ├── test_retrieval.py
│   ├── test_chunking.py
│   ├── test_reranker.py
│   └── test_api.py
│
├── scripts/
│   ├── ingest_documents.py
│   └── build_graph.py
│
├── docker/
│   └── Dockerfile
│
├── notebooks/
│   └── experiments.ipynb
│
├── requirements.txt
└── README.md


### Tests

Types of Tests You Should Have

| Test Type         | Example            |
| ----------------- | ------------------ |
| unit tests        | chunking logic     |
| integration tests | retrieval pipeline |
| API tests         | FastAPI endpoints  |
| evaluation tests  | RAG answer quality |
