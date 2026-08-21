from .base import BaseNode
class StartNode(BaseNode):
    node_type="start"
    async def execute(self,state): return {"output":state.get("input","")}
