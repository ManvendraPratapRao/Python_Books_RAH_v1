from llama_index.core.postprocessor import SentenceTransformerRerank
from src.config import settings

def get_reranker(model_name: str = None, top_n: int = 3):
    if model_name is None:
        model_name = settings.RERANK_MODEL
    """
    Initializes and returns the cross-encoder reranker model.
    """
    return SentenceTransformerRerank(
        model=model_name,
        top_n=top_n
    )
