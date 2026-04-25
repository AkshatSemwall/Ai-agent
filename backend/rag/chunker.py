import re
from typing import List


def chunk_text(text: str, chunk_size: int = 350, chunk_overlap: int = 80) -> List[str]:
    clean_text = re.sub(r"\s+", " ", text).strip()
    words = clean_text.split(" ")

    if len(words) <= chunk_size:
        return [clean_text]

    chunks: List[str] = []
    start = 0
    while start < len(words):
        end = min(len(words), start + chunk_size)
        chunk = " ".join(words[start:end]).strip()
        if chunk:
            chunks.append(chunk)
        start += chunk_size - chunk_overlap
    return chunks
