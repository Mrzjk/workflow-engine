from app.schemas.workflow import WorkflowSchema
from app.workflow.dsl import WorkflowMapper
def test_dsl_ir_roundtrip_preserves_canvas_data():
    dsl=WorkflowSchema.model_validate({"metadata":{"name":"x"},"variables":{"score":{"type":"number"}},"nodes":[{"id":"start","type":"start","position":{"x":1,"y":2}},{"id":"end","type":"end","position":{"x":3,"y":4}}],"edges":[{"id":"e","source":"start","target":"end"}]})
    assert WorkflowMapper.to_dsl(WorkflowMapper.to_ir(dsl)).model_dump()==dsl.model_dump()
