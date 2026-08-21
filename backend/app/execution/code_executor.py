class CodeExecutor:
    async def execute(self, code: str, context: dict) -> dict: raise NotImplementedError
class MockCodeExecutor(CodeExecutor):
    async def execute(self, code, context): return {"result":"Code execution is delegated to a configured sandbox.","code":code}
class DockerCodeExecutor(CodeExecutor): pass
class E2BCodeExecutor(CodeExecutor): pass
class DaytonaCodeExecutor(CodeExecutor): pass
class SandboxCodeExecutor(CodeExecutor): pass
