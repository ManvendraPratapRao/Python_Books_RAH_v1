import os
from typing import Dict, Any

def get_base_metadata(filepath: str) -> Dict[str, Any]:
    """
    Generates base metadata for a given file path.
    """
    filename = os.path.basename(filepath)
    folder = os.path.basename(os.path.dirname(filepath))
    extension = os.path.splitext(filename)[1].lower()
    
    return {
        "filename": filename,
        "extension": extension,
        "source_folder": folder
    }

def enrich_document_metadata(text, filepath: str) -> Dict[str, Any]:
    """
    Enriches the document with additional metadata.
    Currently computes character count, but can be expanded to extract
    authors, titles, or other metadata using LLMs or regex.
    """
    metadata = get_base_metadata(filepath)
    metadata["char_count"] = len(text)
    
    # Add more enrichers here in the future
    return metadata
