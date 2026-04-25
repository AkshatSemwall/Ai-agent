import requests
from backend.core.config import Config
from backend.core.logger import logger


def call_groq(prompt: str, max_tokens: int = 700) -> str:
    if not Config.GROQ_API_KEY:
        raise ValueError("Missing GROQ_API_KEY in environment")

    payload = {
        "model": Config.GROQ_MODEL,
        "temperature": Config.TEMPERATURE,
        "max_tokens": max_tokens,
        "messages": [{"role": "user", "content": prompt}],
    }

    headers = {
        "Authorization": f"Bearer {Config.GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    logger.info("Calling Groq LLM")
    response = requests.post(
        Config.GROQ_ENDPOINT,
        headers=headers,
        json=payload,
        timeout=Config.API_TIMEOUT,
    )
    response.raise_for_status()
    body = response.json()
    choice = body.get("choices", [])[0]
    message = choice.get("message", {}) if isinstance(choice, dict) else {}
    if isinstance(message, dict):
        return message.get("content", "").strip()

    return str(body)
