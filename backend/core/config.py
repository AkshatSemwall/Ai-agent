import os
from pathlib import Path
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parents[2]
load_dotenv(ROOT_DIR / ".env")


class Config:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
    GROQ_ENDPOINT = os.getenv(
        "GROQ_ENDPOINT",
        "https://api.groq.com/openai/v1/chat/completions",
    )
    GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.2"))
    API_TIMEOUT = int(os.getenv("API_TIMEOUT", "30"))
    DOCS_DIR = os.getenv("DOCS_DIR", str(ROOT_DIR / "data" / "docs"))
    VECTORSTORE_DIR = os.getenv(
        "VECTORSTORE_DIR", str(ROOT_DIR / "data" / "vectorstore")
    )
    TOP_K = int(os.getenv("TOP_K", "5"))
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "350"))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "80"))
