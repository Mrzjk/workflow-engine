from fastapi import APIRouter
from app.core.config import settings
router=APIRouter(prefix="/api/models",tags=["models"])
@router.get("")
async def models(): return [{"provider":settings.default_llm_provider,"name":settings.default_llm_model}]
