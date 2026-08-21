from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_session
from app.services.workflow_service import WorkflowService
from app.services.run_service import RunService
from app.repositories.workflow import WorkflowRepository
from app.schemas.workflow import WorkflowCreate,WorkflowSchema
from app.schemas.run import RunCreate
from app.runtime.streaming import event_stream
router=APIRouter(prefix="/api/workflows",tags=["workflows"])
@router.post("")
async def create(data:WorkflowCreate,s:AsyncSession=Depends(get_session)): return await WorkflowService(s).create(data)
@router.get("/{id}")
async def get(id:str,s:AsyncSession=Depends(get_session)):
    x=await WorkflowRepository(s).get(id)
    if not x: raise HTTPException(404,"workflow not found")
    return x
@router.post("/{id}/validate")
async def validate(id:str,s:AsyncSession=Depends(get_session)): return await WorkflowService(s).validate(id)
@router.post("/{id}/run")
async def run(id:str,data:RunCreate,s:AsyncSession=Depends(get_session)):
    v=await WorkflowRepository(s).latest(id)
    if not v: raise HTTPException(404,"workflow not found")
    run_id,result=await RunService.executor.run(WorkflowSchema.model_validate(v.graph_json),data.input); return {"run_id":run_id,"result":result}
@router.get("/{id}/runs/{run_id}/stream")
async def stream(id:str,run_id:str):
    bus=RunService.executor.runs.get(run_id)
    if not bus: raise HTTPException(404,"run not found")
    return event_stream(bus)
@router.get("/{id}/versions")
async def versions(id:str,s:AsyncSession=Depends(get_session)): return await WorkflowRepository(s).versions(id)
@router.post("/{id}/publish")
async def publish(id:str,s:AsyncSession=Depends(get_session)): return await WorkflowRepository(s).publish(id)
