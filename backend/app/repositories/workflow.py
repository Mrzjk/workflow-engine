from sqlalchemy import select
from .base import Repository
from app.db.models import Workflow, WorkflowVersion
class WorkflowRepository(Repository):
    async def create(self,data,graph):
        w=Workflow(**data); self.session.add(w); await self.session.flush(); self.session.add(WorkflowVersion(workflow_id=w.id,version=1,graph_json=graph)); await self.session.commit(); return w
    async def get(self,id): return await self.session.get(Workflow,id)
    async def latest(self,id): return (await self.session.scalars(select(WorkflowVersion).where(WorkflowVersion.workflow_id==id).order_by(WorkflowVersion.version.desc()))).first()
    async def versions(self,id): return list((await self.session.scalars(select(WorkflowVersion).where(WorkflowVersion.workflow_id==id))).all())
    async def publish(self,id):
        v=await self.latest(id); v.status="published"; await self.session.commit(); return v
