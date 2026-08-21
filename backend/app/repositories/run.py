from .base import Repository
from app.db.models import WorkflowRun, NodeRun
class RunRepository(Repository):
    async def get(self,id): return await self.session.get(WorkflowRun,id)
    async def nodes(self,id):
        from sqlalchemy import select
        return list((await self.session.scalars(select(NodeRun).where(NodeRun.run_id==id))).all())
