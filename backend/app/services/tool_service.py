from app.repositories.tool import ToolRepository

class ToolService:
    def __init__(self, session): self.repo = ToolRepository(session)
    async def list(self): return await self.repo.list()
