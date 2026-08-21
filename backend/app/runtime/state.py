from typing import TypedDict, Annotated
import operator
class AgentState(TypedDict, total=False):
    input: str; messages: Annotated[list, operator.add]; variables: dict; node_outputs: dict; execution_context: dict; current_node: str; completed_nodes: Annotated[list, operator.add]; error: str|None
