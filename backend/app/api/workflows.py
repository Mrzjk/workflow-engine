from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_session
from app.services.workflow_service import WorkflowService
from app.services.run_service import RunService
from app.repositories.workflow import WorkflowRepository
from app.schemas.workflow import WorkflowCreate,WorkflowSchema
from app.schemas.run import RunCreate
from app.runtime.streaming import event_stream
from app.workflow.dsl import WorkflowMapper
from app.python.generator import PythonWorkflowGenerator
from app.python.parser import PythonWorkflowParser, PythonParseError
from app.repositories.run import RunRepository
from pydantic import BaseModel
router=APIRouter(prefix="/api/workflows",tags=["workflows"])
class PythonSource(BaseModel): source: str
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
    run,trace,result=await RunService(s).run(id,v,WorkflowSchema.model_validate(v.graph_json),data.input); return {"run_id":run.id,"trace_id":trace.id,"result":result}
@router.get("/{id}/runs/{run_id}/stream")
async def stream(id:str,run_id:str):
    bus=RunService.executor.runs.get(run_id)
    if not bus: raise HTTPException(404,"run not found")
    return event_stream(bus)
@router.get("/{id}/versions")
async def versions(id:str,s:AsyncSession=Depends(get_session)): return await WorkflowRepository(s).versions(id)
@router.post("/{id}/publish")
async def publish(id:str,s:AsyncSession=Depends(get_session)): return await WorkflowRepository(s).publish(id)
@router.get("/{id}/traces")
async def traces(id:str,s:AsyncSession=Depends(get_session)): return await RunRepository(s).traces(id)
@router.get("/{id}/export")
async def export_json(id:str,s:AsyncSession=Depends(get_session)):
    v=await WorkflowRepository(s).latest(id)
    if not v: raise HTTPException(404,"workflow not found")
    return v.graph_json
@router.get("/{id}/export/python")
async def export_python(id:str,s:AsyncSession=Depends(get_session)):
    v=await WorkflowRepository(s).latest(id)
    if not v: raise HTTPException(404,"workflow not found")
    return {"source":PythonWorkflowGenerator().generate(WorkflowMapper.to_ir(WorkflowSchema.model_validate(v.graph_json)))}
@router.post("/import/python")
async def import_python(data:PythonSource):
    try: return WorkflowMapper.to_dsl(PythonWorkflowParser().parse(data.source))
    except PythonParseError as error: raise HTTPException(422,{"code":"UNSUPPORTED_PYTHON_SYNTAX","message":str(error),"details":{}})
