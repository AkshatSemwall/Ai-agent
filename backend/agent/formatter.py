from backend.agent.prompt import build_formatter_prompt
from backend.tools.llm import call_groq
from backend.core.logger import logger


def format_to_json(query: str, analysis: str) -> str:
    logger.info("Formatter node: converting analysis into strict JSON")
    prompt = build_formatter_prompt(query, analysis)
    return call_groq(prompt)
