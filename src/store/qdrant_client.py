from qdrant_client import QdrantClient
from src.config import settings

def get_qdrant_client(url: str = None):
    if url is None:
        url = settings.QDRANT_URL
    """
    Initializes and returns a connection to the local Qdrant container.
    """
    return QdrantClient(url=url)

def create_collection_if_not_exists(client: QdrantClient, collection_name: str, force_recreate: bool = False):
    """
    Checks if a collection exists. If force_recreate is True, deletes it first.
    Note: LlamaIndex QdrantVectorStore handles the actual schema creation during indexing,
    but this can be used for manual management.
    """
    if client.collection_exists(collection_name):
        if force_recreate:
            print(f"Deleting existing collection: {collection_name}")
            client.delete_collection(collection_name)
        else:
            print(f"Collection {collection_name} already exists.")
    else:
        print(f"Collection {collection_name} does not exist yet. It will be created during indexing.")
