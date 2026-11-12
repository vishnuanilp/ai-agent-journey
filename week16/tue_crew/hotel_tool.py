from crewai.tools import tool
from store import search

TOOL_LOG = []


@tool("search_hotel_policy")
def search_hotel_policy(query: str) -> str:
    """Search the hotel's policy documents for a guest question.
    Returns the matching policy text, or NOT FOUND if nothing matches."""
    hits = search(query)
    TOOL_LOG.append((query, [round(d, 3) for _, d in hits]))
    return "\n\n".join(t for t, _ in hits) if hits else "NOT FOUND"