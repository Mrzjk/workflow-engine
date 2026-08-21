from .base import BaseNode
class EndNode(BaseNode):
    node_type="end"
    async def execute(self,state): return {"output":state.get("node_outputs",{})}
