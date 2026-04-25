import json
from backend.agent.prompt import build_planner_prompt
from backend.tools.llm import call_groq
from backend.core.logger import logger


def parse_subtasks(raw_response: str) -> list[str]:
    try:
        payload = json.loads(raw_response)
        if isinstance(payload, dict) and "sub_tasks" in payload:
            return [str(item).strip() for item in payload["sub_tasks"] if item]
    except json.JSONDecodeError:
        pass

    subtasks = []
    for line in raw_response.splitlines():
        normalized = line.strip(" \t-•")
        if normalized:
            subtasks.append(normalized)
    return subtasks[:5] if subtasks else ["Research the query and summarize the findings"]


def plan_subtasks(query: str) -> list[str]:
    logger.info("Planner node: generating sub-tasks for query")
    prompt = build_planner_prompt(query)
    raw = call_groq(prompt)
    subtasks = parse_subtasks(raw)
    logger.info(f"Planner produced {len(subtasks)} sub-tasks")
    return subtasks
