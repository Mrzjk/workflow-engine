from typing import TypedDict, Annotated
import operator
def merge_outputs(current: dict, update: dict) -> dict:
    """Merge distinct node keys returned by concurrently scheduled graph nodes."""
    return {**(current or {}), **(update or {})}
class AgentState(TypedDict, total=False):
    input: str; messages: Annotated[list, operator.add]; variables: dict; node_outputs: Annotated[dict, merge_outputs]; execution_context: dict; current_node: str; completed_nodes: Annotated[list, operator.add]; error: str|None
