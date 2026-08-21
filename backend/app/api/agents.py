from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_session
from app.services.agent_service import AgentService
from app.schemas.agent import AgentCreate
router=APIRouter(prefix="/api/agents",tags=["agents"])
@router.post("")
async def create(data:AgentCreate,s:AsyncSession=Depends(get_session)): return await AgentService(s).create(data.model_dump())
@router.get("")
async def list_agents(s:AsyncSession=Depends(get_session)): return await AgentService(s).list()
@router.get("/{id}")
async def get(id:str,s:AsyncSession=Depends(get_session)):
    x=await AgentService(s).get(id)
    if not x: raise HTTPException(404,"agent not found")
    return x
