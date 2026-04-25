from typing import Iterable


def build_planner_prompt(query: str) -> str:
    return f"""
You are a research planner. Break the user question into 3 to 5 concise, actionable sub-tasks.
Return only valid JSON with this schema:
{
  "sub_tasks": ["...", "...", "..."]
}
User query: {query}
"""


def build_reasoning_prompt(query: str, context_snippets: Iterable[str]) -> str:
    context_text = "\n\n".join(context_snippets)
    return f"""
You are an expert research analyst.
Use the retrieved document snippets below to produce a factual research answer.

Context:
{context_text}

User query: {query}

Write a clear, evidence-based analysis that highlights the main findings, implications, and any caveats.
Do not output JSON in this step.
"""


def build_formatter_prompt(query: str, analysis: str) -> str:
    return f"""
You are a JSON formatter.
Convert the research analysis below into strictly valid JSON with this schema:
{
  "query": string,
  "summary": string,
  "key_points": [string],
  "confidence": number between 0 and 1
}

Analysis:
{analysis}

User query: {query}

Output only valid JSON. Do not include markdown, explanation, or extra text.
"""


def build_validator_prompt(raw_json: str) -> str:
    return f"""
You are a JSON repair assistant.
If the following text is already valid JSON, return it exactly as valid JSON.
If it is invalid, repair it and preserve all fields.

Expected schema:
{
  "query": string,
  "summary": string,
  "key_points": [string],
  "confidence": number between 0 and 1
}

Raw output:
{raw_json}
"""
