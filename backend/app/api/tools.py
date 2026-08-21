from fastapi import APIRouter,Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_session
from app.services.tool_service import ToolService
router=APIRouter(prefix="/api/tools",tags=["tools"])
@router.get("")
async def tools(s:AsyncSession=Depends(get_session)):return await ToolService(s).list()
