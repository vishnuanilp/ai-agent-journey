from pydantic import BaseModel
from crewai.tools import BaseTool
from store import search
from hotel_tool import TOOL_LOG


class PolicyQuery(BaseModel):
    query: str


class HotelPolicyTool(BaseTool):
    name: str = "search_hotel_policy"
    description: str = (
        "Search the hotel's policy documents for a guest question.\n"
        "Returns the matching policy text, or NOT FOUND if nothing matches."
    )
    args_schema: type[BaseModel] = PolicyQuery

    def _run(self, query: str) -> str:
        print("  TOOL:     class tool ran", flush=True)
        hits = search(query)
        TOOL_LOG.append((query, [round(d, 3) for _, d in hits]))
        return "\n\n".join(t for t, _ in hits) if hits else "NOT FOUND"


policy_tool = HotelPolicyTool()
