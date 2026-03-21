from llama_index.core import VectorStoreIndex, StorageContext, Settings
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
import torch

import os
from dotenv import load_dotenv

load_dotenv()

def get_hybrid_retriever(
    client: QdrantClient,
    collection_name: str = None,
    embed_model_name: str = None,
    sparse_model_name: str = None,
    similarity_top_k: int = 10,
    alpha: float = 0.5
):
    if collection_name is None:
        collection_name = os.getenv("QDRANT_COLLECTION", "library_hybrid_v1")
    if embed_model_name is None:
        embed_model_name = os.getenv("EMBED_MODEL", "BAAI/bge-small-en-v1.5")
    if sparse_model_name is None:
        sparse_model_name = os.getenv("SPARSE_MODEL", "prithivida/Splade_PP_en_v1")
    """
    Sets up the hybrid retriever (Dense + Sparse) pointing to Qdrant.
    """
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    # 1. Ensure global embedding model is set (LlamaIndex relies on this for retrieval implicitly)
    Settings.embed_model = HuggingFaceEmbedding(
        model_name=embed_model_name, 
        device=device
    )

    # 2. Connect to the existing Qdrant Store
    vector_store = QdrantVectorStore(
        collection_name=collection_name, 
        client=client, 
        enable_hybrid=True,
        fastembed_sparse_model=sparse_model_name
    )
    
    # 3. Create Index object from the store
    index = VectorStoreIndex.from_vector_store(vector_store=vector_store)

    # 4. Generate the Retriever
    retriever = index.as_retriever(
        vector_store_query_mode="hybrid", 
        similarity_top_k=similarity_top_k,
        alpha=alpha 
    )
    
    return retriever
