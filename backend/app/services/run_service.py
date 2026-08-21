from app.runtime import WorkflowExecutor
class RunService:
    executor=WorkflowExecutor()
*** Add File: agent-platform/backend/app/services/tool_service.py
from app.repositories.tool import ToolRepository
class ToolService:
    def __init__(self,s):self.repo=ToolRepository(s)
    async def list(self):return await self.repo.list()
