from .base import Repository
from app.tools import ToolRegistry
class ToolRepository(Repository):
    async def list(self): return [{"id":name,"name":name,"description":getattr(tool,"description",None)} for name,tool in ToolRegistry.all().items()]
