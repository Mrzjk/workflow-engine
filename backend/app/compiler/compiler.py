from app.runtime.state import AgentState
from app.nodes.registry import NODE_REGISTRY
class WorkflowCompileError(ValueError): pass
class WorkflowCompiler:
    def compile(self, workflow):
        try:
            from langgraph.graph import StateGraph, START, END
            builder=StateGraph(AgentState)
            for n in workflow.nodes: builder.add_node(n.id, NODE_REGISTRY[n.type](n.id,n.config).run)
            for e in workflow.edges:
                builder.add_edge(START if e.source=="start" else e.source, END if e.target=="end" else e.target)
            return builder.compile()
        except Exception as exc: raise WorkflowCompileError(str(exc)) from exc
