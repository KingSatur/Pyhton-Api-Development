from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


class PostCreate(PostBase):
    pass


class UserBase(BaseModel):
    firstName: str
    lastName: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class UserLoginCommand(BaseModel):
    email: EmailStr
    password: str


class UserLoginResponse(BaseModel):
    email: EmailStr
    token: str


class TokenData(BaseModel):
    id: Optional[int]


class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner: UserResponse

    class Config:
        orm_mode = True
