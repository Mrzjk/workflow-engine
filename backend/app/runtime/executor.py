import uuid
from .state import AgentState
from .event_bus import EventBus
from .events import RuntimeEvent
from app.compiler import WorkflowValidator, WorkflowCompiler
class WorkflowExecutor:
    def __init__(self): self.runs={}
    async def run(self, workflow, input_text: str):
        WorkflowValidator().validate(workflow); run_id=str(uuid.uuid4()); bus=EventBus(); self.runs[run_id]=bus
        await bus.publish(RuntimeEvent(run_id,"workflow_started",data={"input":input_text}))
        result=await WorkflowCompiler().compile(workflow).ainvoke({"input":input_text,"messages":[],"variables":{},"node_outputs":{},"completed_nodes":[]})
        await bus.publish(RuntimeEvent(run_id,"workflow_finished",data={"output":result})); return run_id, result
