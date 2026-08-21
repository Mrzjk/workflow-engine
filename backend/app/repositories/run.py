from .base import Repository
from datetime import datetime
from app.db.models import WorkflowRun, NodeRun, WorkflowTrace, TraceSpan
class RunRepository(Repository):
    async def create_run(self, workflow_id, version_id, input_text):
        run=WorkflowRun(workflow_id=workflow_id,workflow_version_id=version_id,input=input_text,status="running",started_at=datetime.utcnow()); self.session.add(run); await self.session.flush(); return run
    async def create_trace(self, workflow_id, run_id, input_data):
        trace=WorkflowTrace(workflow_id=workflow_id,workflow_run_id=run_id,status="running",input=input_data); self.session.add(trace); await self.session.flush(); return trace
    async def finalize(self, run, trace, result, spans, error=None):
        finished=datetime.utcnow(); run.status="failed" if error else "success"; run.output=result if not error else None; run.finished_at=finished; trace.status=run.status; trace.output=result if not error else None; trace.error=str(error) if error else None; trace.finished_at=finished
        for span in spans:
            payload={"id":span.id,"trace_id":trace.id,"node_id":span.node_id,"node_type":span.node_type,"input":span.input,"output":span.output,"status":span.status,"error":span.error,"duration":span.duration,"started_at":span.started_at.replace(tzinfo=None),"finished_at":span.finished_at.replace(tzinfo=None) if span.finished_at else None}
            self.session.add(TraceSpan(**payload)); self.session.add(NodeRun(id=span.id,run_id=run.id,node_id=span.node_id,node_type=span.node_type,input=span.input,output=span.output,status=span.status,error=span.error,duration=span.duration,started_at=payload["started_at"],finished_at=payload["finished_at"]))
        await self.session.commit()
    async def get(self,id): return await self.session.get(WorkflowRun,id)
    async def nodes(self,id):
        from sqlalchemy import select
        return list((await self.session.scalars(select(NodeRun).where(NodeRun.run_id==id))).all())
    async def traces(self, workflow_id):
        from sqlalchemy import select
        return list((await self.session.scalars(select(WorkflowTrace).where(WorkflowTrace.workflow_id==workflow_id).order_by(WorkflowTrace.started_at.desc()))).all())
    async def trace(self, trace_id): return await self.session.get(WorkflowTrace,trace_id)
    async def spans(self, trace_id):
        from sqlalchemy import select
        return list((await self.session.scalars(select(TraceSpan).where(TraceSpan.trace_id==trace_id).order_by(TraceSpan.started_at))).all())
