from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    username: str
    email: str
    api_key: str
    api_secret: str

    class Config:
        orm_mode = True

class IDCardRequest(BaseModel):
    name: str
    output_format: str  # "pdf" or "image"
    user_id: int

class IDCardResponse(BaseModel):
    file_path: str
    output_format: str
    timestamp: str

    class Config:
        orm_mode = True
