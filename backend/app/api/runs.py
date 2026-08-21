from fastapi import APIRouter,Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_session
from app.repositories.run import RunRepository
router=APIRouter(prefix="/api/runs",tags=["runs"])
@router.get("/{id}")
async def get(id:str,s:AsyncSession=Depends(get_session)): return await RunRepository(s).get(id)
@router.get("/{id}/nodes")
async def nodes(id:str,s:AsyncSession=Depends(get_session)): return await RunRepository(s).nodes(id)
