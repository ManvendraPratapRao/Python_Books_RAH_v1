from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse
import time
import json

from src.api.models import QueryRequest, QueryResponse, SourceNode, ChatMessage, HistoryResponse
from src.api.security import verify_api_key, check_rate_limit

from src.store.qdrant_client import get_qdrant_client
from src.engine.retriever import get_hybrid_retriever
from src.engine.reranker import get_reranker
from src.engine.query_engine import get_query_engine

# API Router with global dependencies to secure every route here
router = APIRouter(
    dependencies=[Depends(verify_api_key), Depends(check_rate_limit)]
)

# Global variables to hold State (Volatile memory for this phase)
query_engine = None
chat_history = []

def init_engine():
    """ Called by main.py startup event to pre-load models into VRAM """
    global query_engine
    client = get_qdrant_client()
    retriever = get_hybrid_retriever(client)
    reranker = get_reranker()
    query_engine = get_query_engine(retriever, reranker)

@router.get("/history", response_model=HistoryResponse)
async def get_history():
    """ Fetch the current volatile chat session. """
    return HistoryResponse(messages=chat_history)

@router.delete("/history")
async def clear_history():
    """ Refreshes the chat context. """
    chat_history.clear()
    return {"message": "Chat history cleared successfully."}

@router.post("/query", response_model=QueryResponse)
async def query_rag(request: QueryRequest):
    """ Wait for the full AI response and return JSON. """
    if not query_engine:
        raise HTTPException(status_code=500, detail="Initialize Engine First.")
        
    chat_history.append(ChatMessage(role="user", content=request.query, timestamp=time.time()))
    
    start_time = time.time()
    try:
        response = query_engine.query(request.query)
        
        sources = []
        for node in response.source_nodes:
            # We truncate text for the API response size limits
            clean_text = node.text[:300].replace('\n', ' ') + "..."
            filename = node.metadata.get('filename', 'Unknown Source')
            sources.append(SourceNode(text=clean_text, filename=filename, score=node.score))
            
        answer = str(response)
        
        chat_history.append(ChatMessage(role="assistant", content=answer, timestamp=time.time()))
        
        perf = {"total_time_seconds": round(time.time() - start_time, 2)}
        return QueryResponse(answer=answer, sources=sources, performance=perf)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def stream_generator(query: str):
    """ Assistant Generator for Server-Sent Events """
    response = query_engine.query(query)
    full_answer = ""
    for text in response.response_gen:
        full_answer += text
        # SSE Format
        yield f"data: {json.dumps({'content': text})}\n\n"
        
    chat_history.append(ChatMessage(role="assistant", content=full_answer, timestamp=time.time()))
    yield "data: [DONE]\n\n"

@router.post("/stream")
async def stream_rag(request: QueryRequest):
    """ Stream AI response chunk-by-chunk using Server-Sent Events. """
    if not query_engine:
        raise HTTPException(status_code=500, detail="Initialize Engine First.")
        
    chat_history.append(ChatMessage(role="user", content=request.query, timestamp=time.time()))
    return StreamingResponse(stream_generator(request.query), media_type="text/event-stream")
