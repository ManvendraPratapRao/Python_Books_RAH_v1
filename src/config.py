import os
from dotenv import load_dotenv

# Automatically load environment variables from .env
load_dotenv()

class Config:
    """Central configuration class mapping .env values."""
    LLM_MODEL = os.getenv("LLM_MODEL", "ministral-3:3b")
    CONTEXT_WINDOW = int(os.getenv("CONTEXT_WINDOW", "4096"))
    
    EMBED_MODEL = os.getenv("EMBED_MODEL", "BAAI/bge-small-en-v1.5")
    SPARSE_MODEL = os.getenv("SPARSE_MODEL", "prithivida/Splade_PP_en_v1")
    RERANK_MODEL = os.getenv("RERANK_MODEL", "BAAI/bge-reranker-base")
    
    QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
    QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION", "library_hybrid_v1")

settings = Config()
