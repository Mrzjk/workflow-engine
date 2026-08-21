from .base import BaseNode
from app.execution.code_executor import MockCodeExecutor
class CodeNode(BaseNode):
    node_type="code"
    async def execute(self,state): return await MockCodeExecutor().execute(self.config.get("code",""),state)
