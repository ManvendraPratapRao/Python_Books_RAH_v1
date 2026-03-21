from llama_index.core.node_parser import SemanticSplitterNodeParser
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Document
from typing import List
from src.config import settings

def get_embed_model(model_name: str = None, batch_size: int = 32):
    if model_name is None:
        model_name = settings.EMBED_MODEL
    """Initializes and returns the HuggingFace embedding model."""
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device for embeddings: {device.upper()}")
    
    return HuggingFaceEmbedding(
        model_name=model_name,
        device=device,
        embed_batch_size=batch_size
    )

def get_semantic_splitter(embed_model=None, buffer_size: int = 1, breakpoint_percentile_threshold: int = 90):
    """Initializes and returns the Semantic Splitter."""
    if embed_model is None:
        embed_model = get_embed_model()
        
    return SemanticSplitterNodeParser(
        buffer_size=buffer_size,
        breakpoint_percentile_threshold=breakpoint_percentile_threshold,
        embed_model=embed_model
    )

def chunk_documents(documents: List[Document], splitter=None):
    """
    Takes a list of LlamaIndex Document objects and splits them 
    semantically using the provided splitter.
    """
    if splitter is None:
        splitter = get_semantic_splitter()
        
    print(f"Starting batch chunking for {len(documents)} documents...")
    nodes = splitter.get_nodes_from_documents(documents, show_progress=True)
    print(f"✅ Total Semantic Chunks Created: {len(nodes)}")
    
    return nodes
