import os
import sys

# Ensure src is in the python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from llama_index.core import Document, StorageContext, VectorStoreIndex
from llama_index.vector_stores.qdrant import QdrantVectorStore

from src.pipeline.extractors import get_extractor_for_file
from src.pipeline.cleaners import clean_text
from src.pipeline.enrichers import enrich_document_metadata
from src.pipeline.chunkers import get_semantic_splitter, get_embed_model

from src.store.qdrant_client import get_qdrant_client, create_collection_if_not_exists

BASE_DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../data'))

def ingest_all_books(base_data_path: str = BASE_DATA_PATH) -> list:
    """Finds, extracts, cleans, and structures files into LlamaIndex Documents."""
    processed_docs = []
    
    format_folders = ["pdfs", "epubs", "mobis"]
    
    for folder in format_folders:
        folder_path = os.path.join(base_data_path, folder)
        
        if not os.path.exists(folder_path):
            print(f"Skipping {folder}: Folder not found at {folder_path}")
            continue

        files = [f for f in os.listdir(folder_path) if not f.startswith(".")]
        print(f"Processing {len(files)} files in {folder}...")

        for filename in files:
            file_path = os.path.join(folder_path, filename)

            try:
                # 1. Extraction
                extractor_func = get_extractor_for_file(filename)
                raw_text = extractor_func(file_path)
                
                # 2. Cleaning
                cleaned_text = clean_text(raw_text)
                
                # 3. Enrichment
                metadata = enrich_document_metadata(cleaned_text, file_path)
                
                # 4. Conversion to Document
                doc = Document(text=cleaned_text, metadata=metadata)
                processed_docs.append(doc)
                
                print(f"  ✓ Successfully processed: {filename} ({len(cleaned_text)} chars)")
            except Exception as e:
                print(f"  ✗ Error processing {filename}: {str(e)}")
                
    return processed_docs

from src.config import settings

def build_index(collection_name: str = None, force_recreate: bool = False):
    if collection_name is None:
        collection_name = settings.QDRANT_COLLECTION
    """
    Main orchestration function to run the ingestion pipeline.
    """
    # 1. Extract and Prep Documents
    llama_docs = ingest_all_books()
    if not llama_docs:
        print("No documents were processed. Exiting indexing.")
        return

    # 2. Setup Chunking
    embed_model = get_embed_model()
    splitter = get_semantic_splitter(embed_model=embed_model)
    
    # Perform the split for the ENTIRE library in one batch!
    print(f"Starting batch chunking for {len(llama_docs)} books...")
    final_chunks = splitter.get_nodes_from_documents(llama_docs, show_progress=True)
    print(f"\\n✅ Total Semantic Chunks Created: {len(final_chunks)}")

    # 3. Setup Qdrant Hybrid Storage
    client = get_qdrant_client()
    create_collection_if_not_exists(client, collection_name, force_recreate=force_recreate)
    
    vector_store = QdrantVectorStore(
        collection_name=collection_name, 
        client=client, 
        enable_hybrid=True,
        fastembed_sparse_model="prithivida/Splade_PP_en_v1", 
        batch_size=64
    )
    
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # 4. Populate Index
    print(f"🚀 Starting Hybrid Indexing for {len(final_chunks)} chunks...")
    index = VectorStoreIndex(
        final_chunks, 
        storage_context=storage_context, 
        embed_model=embed_model,
        show_progress=True
    )
    
    print(f"\\n✅ SUCCESS: Chunks are now in your Hybrid Database.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Run the RAG data ingestion pipeline.")
    parser.add_argument("--recreate", action="store_true", help="Force recreate collection in Qdrant")
    args = parser.parse_args()
    
    build_index(force_recreate=args.recreate)
