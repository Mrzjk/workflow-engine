from app.core.constants import NODE_TYPES
class WorkflowValidationError(ValueError): pass
class WorkflowValidator:
    def validate(self, graph):
        ids=[n.id for n in graph.nodes]
        errors=[]
        if ids.count("start")!=1: errors.append("exactly one start node required")
        if ids.count("end")<1: errors.append("end node required")
        if len(ids)!=len(set(ids)): errors.append("duplicate node id")
        for n in graph.nodes:
            if n.type not in NODE_TYPES: errors.append(f"invalid node type: {n.type}")
            if n.type=="condition" and not n.config.get("branches"): errors.append(f"invalid condition: {n.id}")
            if n.type=="join" and n.config.get("mode","all")!="all": errors.append(f"invalid join mode: {n.id}")
        known=set(ids)
        for e in graph.edges:
            if e.source not in known or e.target not in known: errors.append(f"edge references missing node: {e.id}")
        from .graph_analyzer import GraphAnalyzer
        a=GraphAnalyzer(graph)
        if a.detect_cycles(): errors.append("cycles are not allowed")
        if "start" in known:
            for n in ids:
                if not a.is_reachable("start",n): errors.append(f"unreachable node: {n}")
        if errors: raise WorkflowValidationError("workflow validation failed: "+"; ".join(errors))
        return True
