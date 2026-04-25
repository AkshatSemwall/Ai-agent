def build_prompt(query: str) -> str:
    return f"""
You are a strict AI backend system.

You MUST return ONLY valid JSON.

Schema:
{{
  "query": string,
  "summary": string,
  "key_points": array of strings (3-6 items),
  "confidence": number between 0 and 1
}}

RULES:
- No explanation
- No markdown
- No extra text
- Output must be valid JSON

User Query:
{query}
"""