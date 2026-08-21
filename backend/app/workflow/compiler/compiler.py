from app.compiler.compiler import WorkflowCompiler as LangGraphWorkflowCompiler
from app.workflow.dsl import WorkflowMapper
class WorkflowCompiler:
    """Compiles the canonical IR; canvas objects are never runtime inputs."""
    def compile(self, ir): return LangGraphWorkflowCompiler().compile(WorkflowMapper.to_dsl(ir))
