from .base import Repository
from app.db.models import AgentRun, NodeRun
class RunRepository(Repository):
    async def get(self,id): return await self.session.get(AgentRun,id)
    async def nodes(self,id):
        from sqlalchemy import select
        return list((await self.session.scalars(select(NodeRun).where(NodeRun.run_id==id))).all())
