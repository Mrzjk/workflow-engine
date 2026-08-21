from app.repositories.agent import AgentRepository
class AgentService:
    def __init__(self,s): self.repo=AgentRepository(s)
    async def create(self,data): return await self.repo.create(data)
    async def list(self): return await self.repo.list()
    async def get(self,id): return await self.repo.get(id)
