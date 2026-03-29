from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserOut


class PhotoCreate(BaseModel):
    title: str
    description: Optional[str] = None


class PhotoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


class PhotoOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    image_url: str
    uploaded_at: datetime
    user_id: int

    class Config:
        from_attributes = True
