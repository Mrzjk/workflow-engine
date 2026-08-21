import time
class NodeExecutionError(RuntimeError): pass
class BaseNode:
    node_type="base"
    def __init__(self,node_id,config): self.node_id=node_id; self.config=config
    async def run(self,state):
        started=time.perf_counter(); result=await self.execute(state)
        return {"node_outputs":{self.node_id:result},"completed_nodes":[self.node_id],"current_node":self.node_id}
    async def execute(self,state): raise NotImplementedError
