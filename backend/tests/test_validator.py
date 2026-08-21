from app.compiler import WorkflowValidator
from app.schemas.workflow import WorkflowSchema
def test_valid_workflow(): assert WorkflowValidator().validate(WorkflowSchema.model_validate({'nodes':[{'id':'start','type':'start','position':{'x':0,'y':0}},{'id':'end','type':'end','position':{'x':1,'y':1}}],'edges':[{'id':'e','source':'start','target':'end'}]}))
