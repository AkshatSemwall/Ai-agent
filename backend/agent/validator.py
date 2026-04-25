import json
from backend.agent.prompt import build_validator_prompt
from backend.tools.llm import call_groq
from backend.core.logger import logger


def validate_json(raw_json: str) -> str:
    logger.info("Validator node: checking and repairing JSON output")
    try:
        parsed = json.loads(raw_json)
        if isinstance(parsed, dict):
            return json.dumps(parsed, indent=2)
    except json.JSONDecodeError as error:
        logger.warning(f"JSON validation failed: {error}")

    repair_prompt = build_validator_prompt(raw_json)
    return call_groq(repair_prompt)
