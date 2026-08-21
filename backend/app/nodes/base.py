import time
class NodeExecutionError(RuntimeError): pass
class BaseNode:
    node_type="base"
    def __init__(self,node_id,config): self.node_id=node_id; self.config=config
    async def run(self,state):
        started=time.perf_counter(); result=await self.execute(state)
        outputs=dict(state.get("node_outputs",{})); outputs[self.node_id]=result
        return {"node_outputs":outputs,"completed_nodes":[self.node_id],"current_node":self.node_id}
    async def execute(self,state): raise NotImplementedError
