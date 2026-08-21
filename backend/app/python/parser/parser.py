import ast
from app.workflow.ir import WorkflowIR,NodeIR,EdgeIR,MetadataIR
class PythonParseError(ValueError): pass
class UnsupportedPythonSyntaxError(PythonParseError):
    def __init__(self,message,node): super().__init__(f"UNSUPPORTED_PYTHON_SYNTAX at {node.lineno}:{node.col_offset}: {message}")
class PythonWorkflowParser:
    allowed={"llm","tool","condition","join","knowledge","code","connect","add_node","compile"}
    def parse(self, source: str) -> WorkflowIR:
        try: tree=ast.parse(source)
        except SyntaxError as e: raise PythonParseError(f"PYTHON_PARSE_ERROR at {e.lineno}:{e.offset}: {e.msg}") from e
        nodes=[NodeIR(id="start",type="start",name="Start"),NodeIR(id="end",type="end",name="End")]; edges=[]; name="Untitled Workflow"
        for stmt in tree.body:
            if isinstance(stmt,ast.Assign) and isinstance(stmt.value,ast.Call):
                call=stmt.value; attr=call.func.attr if isinstance(call.func,ast.Attribute) else None
                if attr=="Workflow" or (isinstance(call.func,ast.Name) and call.func.id=="Workflow"): name=ast.literal_eval(call.args[0]) if call.args else name; continue
                if attr in self.allowed-{"connect","compile","add_node"}:
                    config={kw.arg:ast.literal_eval(kw.value) for kw in call.keywords if kw.arg and isinstance(kw.value,(ast.Constant,ast.Dict,ast.List))}; ident=config.pop("id",stmt.targets[0].id if isinstance(stmt.targets[0],ast.Name) else attr); nodes.append(NodeIR(id=ident,type=attr,name=ident,config=config)); continue
            if isinstance(stmt,ast.Expr) and isinstance(stmt.value,ast.Call) and isinstance(stmt.value.func,ast.Attribute) and stmt.value.func.attr=="connect":
                args=stmt.value.args
                if len(args)!=2: raise UnsupportedPythonSyntaxError("connect requires two node identifiers",stmt)
                source_id=ast.literal_eval(args[0]) if isinstance(args[0],ast.Constant) else args[0].id; target_id=ast.literal_eval(args[1]) if isinstance(args[1],ast.Constant) else args[1].id; edges.append(EdgeIR(id=f"edge_{len(edges)+1}",source=source_id,target=target_id)); continue
            if isinstance(stmt,(ast.Import,ast.ImportFrom,ast.Pass)): continue
            if not (isinstance(stmt,ast.Assign) and isinstance(stmt.value,ast.Call)): raise UnsupportedPythonSyntaxError(type(stmt).__name__,stmt)
        return WorkflowIR(metadata=MetadataIR(name=name),nodes=nodes,edges=edges)
