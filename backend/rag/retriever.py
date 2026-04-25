from backend.core.logger import logger
from backend.core.config import Config
from backend.rag.vectorstore import FaissVectorStore

_store: FaissVectorStore | None = None


def get_vectorstore() -> FaissVectorStore:
    global _store
    if _store is None:
        logger.info("Initializing FAISS vector store")
        _store = FaissVectorStore()
    return _store


def retrieve_context(query: str, top_k: int | None = None) -> list[dict]:
    store = get_vectorstore()
    results = store.search(query, top_k or Config.TOP_K)
    logger.info("Retrieved %d results for query", len(results))
    return results
