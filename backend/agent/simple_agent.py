import json
from backend.agent.graph import run_graph
from backend.core.logger import logger
from backend.core.schemas import AnalyzeResponse


def run_agent(query: str) -> dict:
    logger.info("Agent execution started")
    raw_output = run_graph(query)
    logger.info("Agent execution completed, validating output")

    try:
        parsed = json.loads(raw_output)
        return AnalyzeResponse.model_validate(parsed).model_dump()
    except Exception as error:
        logger.warning("Agent output was not valid JSON, attempting repair")

    from backend.agent.prompt import build_validator_prompt
    from backend.tools.llm import call_groq

    repair_prompt = build_validator_prompt(raw_output)
    repaired = call_groq(repair_prompt)

    try:
        parsed = json.loads(repaired)
        return AnalyzeResponse.model_validate(parsed).model_dump()
    except Exception:
        logger.error("Repair attempt failed, returning safe fallback")
        return {
            "query": query,
            "summary": raw_output[:200].strip(),
            "key_points": ["Unable to produce fully valid structured output."],
            "confidence": 0.25,
        }
