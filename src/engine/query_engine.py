from llama_index.llms.ollama import Ollama
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core import Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
import torch
from src.config import settings

def get_query_engine(retriever, reranker=None, model_name=None, context_window=None, request_timeout=120.0):
    if model_name is None:
        model_name = settings.LLM_MODEL
    if context_window is None:
        context_window = settings.CONTEXT_WINDOW
    """
    Combines the Retriever, Reranker, and Ollama LLM into a fully functional Query Engine.
    """
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    # Needs to be set explicitly for LlamaIndex components that do implicit embedding
    Settings.embed_model = HuggingFaceEmbedding(
        model_name="BAAI/bge-small-en-v1.5", 
        device=device
    )
    
    # Set the local LLM with an explicitly smaller context window to prevent massive RAM/VRAM allocation
    Settings.context_window = context_window
    Settings.llm = Ollama(
        model=model_name, 
        request_timeout=request_timeout,
        additional_kwargs={"num_ctx": context_window}
    )
    
    # Configure Postprocessors (Reranker)
    node_postprocessors = []
    if reranker is not None:
        node_postprocessors.append(reranker)
        
    # Build the Engine
    engine = RetrieverQueryEngine.from_args(
        retriever=retriever,
        node_postprocessors=node_postprocessors,
        streaming=True
    )
    
    return engine
