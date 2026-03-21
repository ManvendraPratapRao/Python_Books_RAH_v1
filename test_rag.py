import os
import sys

# Ensure src is in the python path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from src.store.qdrant_client import get_qdrant_client
from src.engine.retriever import get_hybrid_retriever
from src.engine.reranker import get_reranker
from src.engine.query_engine import get_query_engine

import time
import torch

def test_existing_rag():
    """
    Tests the RAG pipeline using the existing data stored in the Qdrant database.
    Does NOT extract or chunk documents again.
    """
    print("--- PyTorch Environment Check ---")
    if torch.cuda.is_available():
        print(f"✅ PyTorch is using GPU: {torch.cuda.get_device_name(0)}")
    else:
        print("❌ PyTorch is using CPU. (Ensure CUDA is correctly configured if you want GPU acceleration)")
    print("---------------------------------\n")
    
    print("1. Connecting to your existing Qdrant Database...")
    client = get_qdrant_client()
    
    # Check if the collection actually exists
    if not client.collection_exists("library_hybrid_v1"):
        print("❌ Error: The collection 'library_hybrid_v1' was not found in Qdrant.")
        print("Did you restart the docker container but bind the wrong volume? Or did the indexer fail?")
        return
        
    print("2. Setting up the Hybrid Retriever (Dense + Sparse)...")
    retriever = get_hybrid_retriever(
        client=client, 
        collection_name="library_hybrid_v1", 
        similarity_top_k=10
    )
    
    print("3. Connecting the Cross-Encoder Reranker...")
    reranker = get_reranker(top_n=3)
    
    print("4. Building the Query Engine with Ollama...")
    from src.config import settings
    llm_model = settings.LLM_MODEL
    query_engine = get_query_engine(
        retriever=retriever, 
        reranker=reranker, 
        model_name=llm_model
    )
    
    print("\n✅ RAG Engine Ready! Let's ask a question.")
    
    question = "What are the best practices for building an LLM for production?"
    print(f"\n🧐 Question: '{question}'")
    print(f"🤖 AI RESPONSE (Model: {llm_model}):")
    print("-" * 50)
    
    try:
        start_time = time.time()
        response = query_engine.query(question)
        
        first_token_time = None
        full_text = ""
        ttft = 0.0
        
        for text in response.response_gen:
            if first_token_time is None:
                first_token_time = time.time()
                ttft = first_token_time - start_time
                print(f"[TTFT: {ttft:.2f}s] ", end="", flush=True)
                
            print(text, end="", flush=True)
            full_text += text
            
        end_time = time.time()
        generation_time = end_time - first_token_time
        
        # Estimate tokens (roughly 4 chars per token)
        estimated_tokens = len(full_text) / 4
        tps = estimated_tokens / generation_time if generation_time > 0 else 0
        
        print("\n\n" + "-" * 50)
        print(f"⏱️ Performance:")
        print(f"  - Total Time: {end_time - start_time:.2f}s")
        print(f"  - Time to First Token: {ttft:.2f}s")
        print(f"  - Generation Speed (Est): {tps:.2f} tokens/sec")
        
        # Print the source nodes used for the answer
        print("\n📚 Sources used:")
        for i, node in enumerate(response.source_nodes):
            filename = node.metadata.get('filename', 'Unknown source')
            print(f"[{i+1}] {filename} (Score: {node.score:.4f})")
            
    except Exception as e:
        print(f"\n\n❌ An error occurred during generation: {e}")
        if "more system memory" in str(e).lower() or "500" in str(e):
            print(f"\n💡 Tip: Your system ran out of RAM for the LLM. Try changing `LLM_MODEL` in your `.env` file to a smaller model.")

if __name__ == "__main__":
    test_existing_rag()
