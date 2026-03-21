from pydantic import BaseModel, Field
from typing import List, Optional

class QueryRequest(BaseModel):
    query: str = Field(..., example="What are the best practices for LLMs in production?")
    collection_name: Optional[str] = Field(None, description="Qdrant collection to query")
    top_k: int = Field(10, description="Initial retrieval count")
    top_n: int = Field(3, description="Final reranked count")

class SourceNode(BaseModel):
    text: str
    filename: str
    score: float

class QueryResponse(BaseModel):
    answer: str
    sources: List[SourceNode]
    performance: Optional[dict] = None

class ChatMessage(BaseModel):
    role: str # 'user' or 'assistant'
    content: str
    timestamp: Optional[float] = None

class HistoryResponse(BaseModel):
    messages: List[ChatMessage]
