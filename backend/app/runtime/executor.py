import uuid
from .state import AgentState
from .event_bus import EventBus
from .events import RuntimeEvent
from app.compiler import WorkflowValidator, WorkflowCompiler
from app.workflow.dsl import WorkflowMapper
from app.workflow.compiler import WorkflowCompiler as IRWorkflowCompiler
from .tracing import TraceRecorder
class WorkflowExecutor:
    def __init__(self): self.runs={}
    async def run(self, workflow, input_text: str, run_id: str | None = None, recorder: TraceRecorder | None = None):
        WorkflowValidator().validate(workflow); run_id=run_id or str(uuid.uuid4()); bus=EventBus(); recorder=recorder or TraceRecorder(); self.runs[run_id]=bus
        await bus.publish(RuntimeEvent(run_id,"workflow_started",data={"input":input_text}))
        ir=WorkflowMapper.to_ir(workflow)
        try:
            result=await IRWorkflowCompiler().compile(ir,recorder).ainvoke({"input":input_text,"messages":[],"variables":{},"node_outputs":{},"completed_nodes":[]})
            await bus.publish(RuntimeEvent(run_id,"workflow_finished",data={"output":result})); return run_id, result, recorder
        except Exception as error:
            await bus.publish(RuntimeEvent(run_id,"workflow_error",data={"error":str(error)})); raise
