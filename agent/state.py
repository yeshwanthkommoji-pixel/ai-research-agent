from typing import TypedDict, List, Optional, Annotated
import operator


class Source(TypedDict):
    url: str
    title: str
    content: str
    credibility_score: float


class AgentState(TypedDict):
    query: str                                          # Original user question
    search_queries: List[str]                           # Planned search queries
    sources: Annotated[List[Source], operator.add]      # Accumulated sources
    iterations: int                                     # Search loop count
    sufficient: bool                                    # Enough info gathered?
    synthesis: str                                      # Claude's synthesized findings
    report: str                                         # Final formatted report
    error: Optional[str]                                # Error message if any