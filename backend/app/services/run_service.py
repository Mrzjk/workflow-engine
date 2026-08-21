from app.runtime.executor import WorkflowExecutor
from app.runtime.tracing import TraceRecorder
from app.repositories.run import RunRepository
class RunService:
    executor=WorkflowExecutor()
    def __init__(self, session): self.repository=RunRepository(session)
    async def run(self, workflow_id, version, workflow, input_text):
        run=await self.repository.create_run(workflow_id,version.id,input_text); trace=await self.repository.create_trace(workflow_id,run.id,{"input":input_text}); recorder=TraceRecorder()
        try:
            _,result,recorder=await self.executor.run(workflow,input_text,run.id,recorder)
            await self.repository.finalize(run,trace,result,recorder.spans); return run,trace,result
        except Exception as error:
            await self.repository.finalize(run,trace,{},recorder.spans,error); raise
