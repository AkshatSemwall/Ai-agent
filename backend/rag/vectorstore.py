import json
from pathlib import Path
import faiss
from backend.core.config import Config
from backend.core.logger import logger
from backend.rag.chunker import chunk_text
from backend.tools.embeddings import EMBEDDING_MODEL


class FaissVectorStore:
    def __init__(self) -> None:
        self.index_path = Path(Config.VECTORSTORE_DIR) / "faiss.index"
        self.meta_path = Path(Config.VECTORSTORE_DIR) / "metadata.json"
        self.index = None
        self.metadata = []
        self._prepare_store()

    def _prepare_store(self) -> None:
        Path(Config.VECTORSTORE_DIR).mkdir(parents=True, exist_ok=True)
        if self.index_path.exists() and self.meta_path.exists():
            self._load_store()
        else:
            self._build_store()

    def _load_store(self) -> None:
        self.index = faiss.read_index(str(self.index_path))
        with open(self.meta_path, "r", encoding="utf-8") as handle:
            self.metadata = json.load(handle)
        logger.info("Loaded FAISS index with %d chunks", len(self.metadata))

    def _build_store(self) -> None:
        docs = sorted(Path(Config.DOCS_DIR).glob("**/*.*"))
        texts = []
        metadata = []

        for path in docs:
            content = path.read_text(encoding="utf-8", errors="ignore").strip()
            if not content:
                continue
            chunks = chunk_text(content, Config.CHUNK_SIZE, Config.CHUNK_OVERLAP)
            for index, chunk in enumerate(chunks):
                texts.append(chunk)
                metadata.append(
                    {
                        "id": f"{path.name}-{index}",
                        "source": path.name,
                        "chunk_id": index,
                        "text": chunk,
                    }
                )

        if not texts:
            raise RuntimeError(
                f"No documents were found in {Config.DOCS_DIR}. Add research files to continue."
            )

        embeddings = EMBEDDING_MODEL.embed(texts)
        dim = embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dim)
        self.index.add(embeddings)

        self.index_path.parent.mkdir(parents=True, exist_ok=True)
        faiss.write_index(self.index, str(self.index_path))
        with open(self.meta_path, "w", encoding="utf-8") as handle:
            json.dump(metadata, handle, indent=2)

        self.metadata = metadata
        logger.info("Built FAISS index with %d chunks", len(self.metadata))

    def search(self, query: str, top_k: int = None) -> list[dict]:
        if self.index is None:
            raise RuntimeError("Vector store is not initialized")

        query_embedding = EMBEDDING_MODEL.embed([query])
        count = min(top_k or Config.TOP_K, len(self.metadata))
        distances, ids = self.index.search(query_embedding, count)

        results = []
        for score, idx in zip(distances[0], ids[0]):
            if idx < 0:
                continue
            entry = self.metadata[int(idx)].copy()
            entry["score"] = float(score)
            results.append(entry)
        return results
