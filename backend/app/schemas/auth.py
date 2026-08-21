from pydantic import BaseModel, EmailStr
class RegisterRequest(BaseModel): email: EmailStr; password: str
class LoginRequest(RegisterRequest): pass
class TokenResponse(BaseModel): access_token: str; token_type: str="bearer"
