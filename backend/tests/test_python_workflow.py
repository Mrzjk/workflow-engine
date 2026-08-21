from app.python.parser import PythonWorkflowParser
from app.python.generator import PythonWorkflowGenerator
def test_python_to_ir():
    ir=PythonWorkflowParser().parse('from workflow_studio import Workflow\nworkflow = Workflow("Demo")\na = workflow.llm(id="a", model="x")\nworkflow.connect("start", a)\nworkflow.connect(a, "end")')
    assert [n.id for n in ir.nodes]==['start','end','a']
def test_ir_to_python():
    ir=PythonWorkflowParser().parse('workflow = Workflow("Demo")')
    assert 'Workflow("Demo")' in PythonWorkflowGenerator().generate(ir)
