from backend.agent.prompt import build_reasoning_prompt
from backend.tools.llm import call_groq
from backend.core.logger import logger


def generate_analysis(query: str, context_snippets: list[str]) -> str:
    logger.info("Reasoning node: generating analysis from retrieved context")
    prompt = build_reasoning_prompt(query, context_snippets)
    return call_groq(prompt)
