from app.repositories.workflow import WorkflowRepository
from app.schemas.workflow import WorkflowSchema
from app.compiler import WorkflowValidator
class WorkflowService:
    def __init__(self,s): self.repo=WorkflowRepository(s)
    async def create(self,data): return await self.repo.create({"agent_id":data.agent_id,"name":data.name,"description":data.description},data.graph.model_dump())
    async def validate(self,id):
        v=await self.repo.latest(id); WorkflowValidator().validate(WorkflowSchema.model_validate(v.graph_json)); return {"valid":True}
