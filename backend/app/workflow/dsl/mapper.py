"""Lossless mapping between persisted DSL and canonical Workflow IR."""
from app.schemas.workflow import WorkflowSchema
from app.workflow.ir import WorkflowIR, NodeIR, EdgeIR, MetadataIR, VariableIR
class WorkflowMapper:
    @staticmethod
    def to_ir(dsl: WorkflowSchema) -> WorkflowIR:
        return WorkflowIR(version=dsl.version, metadata=MetadataIR.model_validate(dsl.metadata), variables={k:VariableIR.model_validate({"name":k,**v}) for k,v in dsl.variables.items()}, nodes=[NodeIR(id=n.id,type=n.type,name=n.config.get("name",n.id),config=n.config,position=n.position.model_dump()) for n in dsl.nodes], edges=[EdgeIR(id=e.id,source=e.source,target=e.target,condition=e.condition) for e in dsl.edges])
    @staticmethod
    def to_dsl(ir: WorkflowIR) -> WorkflowSchema:
        return WorkflowSchema.model_validate({"version":ir.version,"metadata":ir.metadata.model_dump(),"variables":{k:v.model_dump(exclude={"name"}) for k,v in ir.variables.items()},"nodes":[{"id":n.id,"type":n.type,"position":n.position or {"x":0,"y":0},"config":n.config} for n in ir.nodes],"edges":[{"id":e.id,"source":e.source,"target":e.target,"condition":e.condition.model_dump() if e.condition else None} for e in ir.edges]})
