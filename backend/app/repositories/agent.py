from sqlalchemy import select
from .base import Repository
from app.db.models import Agent
class AgentRepository(Repository):
    async def create(self,data): obj=Agent(**data); self.session.add(obj); await self.session.commit(); await self.session.refresh(obj); return obj
    async def list(self): return list((await self.session.scalars(select(Agent))).all())
    async def get(self,id): return await self.session.get(Agent,id)
