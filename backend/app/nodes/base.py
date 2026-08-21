import time
class NodeExecutionError(RuntimeError): pass
class BaseNode:
    node_type="base"
    def __init__(self,node_id,config): self.node_id=node_id; self.config=config; self.trace_recorder=None
    async def run(self,state):
        trace_input={"input":state.get("input"),"variables":state.get("variables",{}),"upstream_outputs":state.get("node_outputs",{})}
        span=self.trace_recorder.start(self.node_id,self.node_type,trace_input) if self.trace_recorder else None
        try:
            result=await self.execute(state)
            if span: self.trace_recorder.finish(span,result)
            return {"node_outputs":{self.node_id:result},"completed_nodes":[self.node_id],"current_node":self.node_id}
        except Exception as error:
            if span: self.trace_recorder.finish(span,error=error)
            raise NodeExecutionError(f"{self.node_id}: {error}") from error
    async def execute(self,state): raise NotImplementedError
