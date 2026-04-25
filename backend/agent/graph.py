import json
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph
from backend.agent.planner import plan_subtasks
from backend.agent.reasoning import generate_analysis
from backend.agent.formatter import format_to_json
from backend.agent.validator import validate_json
from backend.rag.retriever import retrieve_context
from backend.core.logger import logger


class AgentState(TypedDict, total=False):
    query: str
    sub_tasks: list[str]
    retrieved_context: list[str]
    analysis: str
    result_json: str


def planner_node(state: AgentState) -> dict:
    query = state.get("query", "")
    return {"sub_tasks": plan_subtasks(query)}


def retriever_node(state: AgentState) -> dict:
    query = state.get("query", "")
    hits = retrieve_context(query)
    context_snippets = [f"[{hit['source']}] {hit['text']}" for hit in hits]
    logger.info(f"Retriever node returned {len(context_snippets)} snippets")
    return {"retrieved_context": context_snippets}


def reasoning_node(state: AgentState) -> dict:
    query = state.get("query", "")
    context_snippets = state.get("retrieved_context", [])
    if not context_snippets:
        context_snippets = ["No relevant documents were retrieved. Use your domain knowledge to answer the query."]
    return {"analysis": generate_analysis(query, context_snippets)}


def formatter_node(state: AgentState) -> dict:
    query = state.get("query", "")
    analysis = state.get("analysis", "")
    return {"result_json": format_to_json(query, analysis)}


def validator_node(state: AgentState) -> dict:
    result = state.get("result_json", "")
    repaired = validate_json(result)
    return {"result_json": repaired}


def build_agent_graph() -> object:
    graph = StateGraph(state_schema=AgentState)
    graph.add_sequence(
        [
            ("planner", planner_node),
            ("retriever", retriever_node),
            ("reasoner", reasoning_node),
            ("formatter", formatter_node),
            ("validator", validator_node),
        ]
    )
    graph.set_entry_point("planner")
    graph.set_finish_point("validator")
    compiled = graph.compile()
    logger.info("LangGraph agent graph compiled successfully")
    return compiled


AGENT_GRAPH = build_agent_graph()


def run_graph(query: str) -> str:
    logger.info("Invoking LangGraph agent for query")
    result = AGENT_GRAPH.invoke({"query": query})
    return result.get("result_json", "")
