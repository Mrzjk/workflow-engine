from app.runtime.state import AgentState
from app.nodes.registry import NODE_REGISTRY
class WorkflowCompileError(ValueError): pass
class WorkflowCompiler:
    def compile(self, workflow):
        try:
            from langgraph.graph import StateGraph, START, END
            builder=StateGraph(AgentState)
            for n in workflow.nodes: builder.add_node(n.id, NODE_REGISTRY[n.type](n.id,n.config).run)
            conditional_sources={n.id for n in workflow.nodes if n.type=="condition"}
            for e in workflow.edges:
                if e.source not in conditional_sources:
                    builder.add_edge(START if e.source=="start" else e.source, END if e.target=="end" else e.target)
            for node in workflow.nodes:
                if node.type=="condition":
                    children=[e.target for e in workflow.edges if e.source==node.id]
                    builder.add_conditional_edges(node.id, lambda state, children=children: state.get("node_outputs",{}).get(node.id,{}).get("branches",children), children)
            return builder.compile()
        except Exception as exc: raise WorkflowCompileError(str(exc)) from exc
