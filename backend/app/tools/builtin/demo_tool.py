from langchain_core.tools import tool
@tool
def demo_tool(input: str) -> str:
    """Return a deterministic demonstration response."""
    return f"demo result: {input}"
