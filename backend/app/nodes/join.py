from .base import BaseNode
class JoinNode(BaseNode):
    node_type="join"
    async def execute(self,state): return {"output":state.get("node_outputs",{}),"mode":"all"}
