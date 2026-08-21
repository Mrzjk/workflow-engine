import json
from app.workflow.ir import WorkflowIR
class PythonWorkflowGenerator:
    def generate(self, ir: WorkflowIR) -> str:
        lines=["from workflow_studio import Workflow", "", f"workflow = Workflow({json.dumps(ir.metadata.name)})", ""]
        refs={}
        for node in ir.nodes:
            if node.type in {"start","end"}: continue
            method="tool" if node.type=="tool" else node.type
            args=", ".join(f"{k}={json.dumps(v)}" for k,v in node.config.items())
            lines.append(f"{node.id} = workflow.{method}(id={json.dumps(node.id)}{', ' if args else ''}{args})"); refs[node.id]=node.id
        lines.append("")
        for edge in ir.edges: lines.append(f"workflow.connect({json.dumps(edge.source)}, {json.dumps(edge.target)})")
        lines.extend(["", "app = workflow.compile()", ""])
        return "\n".join(lines)
