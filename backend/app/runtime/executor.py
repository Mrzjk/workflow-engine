import uuid
from .state import AgentState
from .event_bus import EventBus
from .events import RuntimeEvent
from app.compiler import WorkflowValidator, WorkflowCompiler
from app.workflow.dsl import WorkflowMapper
from app.workflow.compiler import WorkflowCompiler as IRWorkflowCompiler
class WorkflowExecutor:
    def __init__(self): self.runs={}
    async def run(self, workflow, input_text: str):
        WorkflowValidator().validate(workflow); run_id=str(uuid.uuid4()); bus=EventBus(); self.runs[run_id]=bus
        await bus.publish(RuntimeEvent(run_id,"workflow_started",data={"input":input_text}))
        ir=WorkflowMapper.to_ir(workflow)
        result=await IRWorkflowCompiler().compile(ir).ainvoke({"input":input_text,"messages":[],"variables":{},"node_outputs":{},"completed_nodes":[]})
        await bus.publish(RuntimeEvent(run_id,"workflow_finished",data={"output":result})); return run_id, result
