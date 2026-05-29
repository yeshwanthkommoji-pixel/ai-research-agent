import os
import json
from typing import List
from groq import Groq
from agent.state import AgentState, Source
from tools.search import tavily_search
from tools.scraper import extract_article_content
from utils.credibility import score_source
from utils.report import generate_report

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MAX_ITERATIONS = int(os.getenv("MAX_SEARCH_ITERATIONS", 3))


def plan_searches(state: AgentState) -> AgentState:
    """Groq decides what search queries to run for the given topic."""
    print(f"\n📋 Planning searches for: {state['query']}")

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=500,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a research planner. Given a research question, generate 3 specific "
                    "web search queries that together will gather comprehensive information. "
                    "Return ONLY a JSON array of strings. Example: [\"query 1\", \"query 2\", \"query 3\"]"
                )
            },
            {"role": "user", "content": f"Research question: {state['query']}"}
        ],
    )

    raw = response.choices[0].message.content.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    queries = json.loads(raw.strip())
    print(f"   Planned queries: {queries}")

    return {**state, "search_queries": queries, "iterations": 0, "sources": []}


def web_search(state: AgentState) -> AgentState:
    """Run Tavily searches and collect raw results."""
    iteration = state["iterations"]
    queries = state["search_queries"]

    if iteration == 0:
        current_queries = queries
    else:
        print(f"\n🔄 Iteration {iteration + 1}: searching for more depth...")
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            max_tokens=200,
            messages=[
                {
                    "role": "system",
                    "content": "Generate 1 additional search query to fill gaps in research. Return ONLY the query string, no quotes."
                },
                {
                    "role": "user",
                    "content": (
                        f"Original question: {state['query']}\n"
                        f"Already searched: {state['search_queries']}\n"
                        "What else should I search?"
                    ),
                }
            ],
        )
        new_query = response.choices[0].message.content.strip()
        current_queries = [new_query]
        queries = queries + [new_query]

    new_sources: List[Source] = []
    for q in current_queries:
        print(f"   🔍 Searching: {q}")
        results = tavily_search(q)
        for r in results:
            content = extract_article_content(r["url"])
            score = score_source(r["url"], content)
            if score >= 0.4:
                new_sources.append(
                    Source(
                        url=r["url"],
                        title=r.get("title", ""),
                        content=content or r.get("content", ""),
                        credibility_score=score,
                    )
                )

    return {
        **state,
        "search_queries": queries,
        "sources": state["sources"] + new_sources,
        "iterations": iteration + 1,
    }


def evaluate_sources(state: AgentState) -> AgentState:
    """Groq decides if we have enough information or need more searches."""
    sources_summary = "\n".join(
        [f"- [{s['title']}]({s['url']}): {s['content'][:200]}..." for s in state["sources"]]
    )

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=100,
        messages=[
            {
                "role": "system",
                "content": "You evaluate research completeness. Reply with ONLY 'sufficient' or 'insufficient'."
            },
            {
                "role": "user",
                "content": f"Question: {state['query']}\n\nSources found:\n{sources_summary}",
            }
        ],
    )

    verdict = response.choices[0].message.content.strip().lower()
    sufficient = "sufficient" in verdict or state["iterations"] >= MAX_ITERATIONS
    print(f"\n📊 Source evaluation: {'✅ Sufficient' if sufficient else '🔄 Need more'} ({len(state['sources'])} sources)")

    return {**state, "sufficient": sufficient}


def synthesize_findings(state: AgentState) -> AgentState:
    """Groq synthesizes all gathered sources into structured findings."""
    print("\n🧠 Synthesizing findings with Groq...")

    sources_text = "\n\n".join(
        [
            f"SOURCE [{i+1}]: {s['title']}\nURL: {s['url']}\n{s['content'][:1500]}"
            for i, s in enumerate(state["sources"])
        ]
    )

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=2000,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a research analyst. Synthesize the provided sources into clear, factual findings. "
                    "Use inline citations like [1], [2] referring to source numbers. "
                    "Structure your synthesis with: Key Findings, Analysis, and Implications. "
                    "Be objective and note any conflicting information across sources."
                )
            },
            {
                "role": "user",
                "content": f"Research question: {state['query']}\n\n{sources_text}",
            }
        ],
    )

    synthesis = response.choices[0].message.content
    return {**state, "synthesis": synthesis}


def write_report(state: AgentState) -> AgentState:
    """Generate the final structured Markdown report."""
    print("\n📄 Writing final report...")
    report = generate_report(
        query=state["query"],
        synthesis=state["synthesis"],
        sources=state["sources"],
    )
    return {**state, "report": report}