from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


class UserCreate(BaseModel):
    name: str = Field(..., min_length=2)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=256)



class UserLogin(BaseModel):
    email: EmailStr
    password: str

# schemas/user.py

# schemas/user.py

class AuthResponse(BaseModel):
    user: UserResponse
    access_token: str
    token_type: str = "bearer"




class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
