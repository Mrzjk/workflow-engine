from datetime import datetime,timedelta,timezone
import jwt
from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from pwdlib import PasswordHash
from app.db.session import get_session
from app.db.models import User
from app.schemas.auth import RegisterRequest,LoginRequest,TokenResponse
router=APIRouter(prefix="/api/auth",tags=["auth"]); hasher=PasswordHash.recommended(); SECRET="replace-with-env-secret"
def token(user): return jwt.encode({"sub":user.id,"role":user.role,"exp":datetime.now(timezone.utc)+timedelta(hours=12)},SECRET,algorithm="HS256")
@router.post('/register',response_model=TokenResponse)
async def register(data:RegisterRequest,s:AsyncSession=Depends(get_session)):
    if await s.scalar(select(User).where(User.email==data.email)): raise HTTPException(409,'email already registered')
    user=User(email=data.email,password_hash=hasher.hash(data.password));s.add(user);await s.commit();return {"access_token":token(user)}
@router.post('/login',response_model=TokenResponse)
async def login(data:LoginRequest,s:AsyncSession=Depends(get_session)):
    user=await s.scalar(select(User).where(User.email==data.email))
    if not user or not hasher.verify(data.password,user.password_hash): raise HTTPException(401,'invalid credentials')
    return {"access_token":token(user)}
