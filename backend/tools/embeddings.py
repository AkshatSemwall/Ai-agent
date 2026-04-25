import numpy as np
from sentence_transformers import SentenceTransformer
from backend.core.logger import logger


class EmbeddingModel:
    def __init__(self) -> None:
        logger.info("Loading sentence-transformers embedding model...")
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def embed(self, texts: list[str]) -> np.ndarray:
        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )
        if embeddings.dtype != np.float32:
            embeddings = embeddings.astype("float32")
        return embeddings


EMBEDDING_MODEL = EmbeddingModel()
