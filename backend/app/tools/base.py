from typing import Protocol
class ToolExecutionError(RuntimeError): pass
class ToolProvider(Protocol):
    async def ainvoke(self, args: dict): ...
