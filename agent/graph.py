from langgraph.graph import StateGraph, END
from agent.state import AgentState
from agent.nodes import (
    plan_searches,
    web_search,
    evaluate_sources,
    synthesize_findings,
    write_report,
)


def should_continue(state: AgentState) -> str:
    """Edge condition: loop back to search or move to synthesis."""
    if state.get("sufficient") or state.get("iterations", 0) >= 3:
        return "synthesize"
    return "search_more"


def build_graph() -> StateGraph:
    graph = StateGraph(AgentState)

    # Add nodes
    graph.add_node("plan", plan_searches)
    graph.add_node("search", web_search)
    graph.add_node("evaluate", evaluate_sources)
    graph.add_node("synthesize", synthesize_findings)
    graph.add_node("report", write_report)

    # Define edges
    graph.set_entry_point("plan")
    graph.add_edge("plan", "search")
    graph.add_edge("search", "evaluate")

    # Conditional loop: search more or move to synthesis
    graph.add_conditional_edges(
        "evaluate",
        should_continue,
        {
            "search_more": "search",
            "synthesize": "synthesize",
        },
    )

    graph.add_edge("synthesize", "report")
    graph.add_edge("report", END)

    return graph.compile()


# Singleton compiled graph
research_agent = build_graph()