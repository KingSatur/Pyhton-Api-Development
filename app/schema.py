from pydantic import BaseModel, EmailStr, conint
from typing import Optional
from datetime import datetime

from app.models import Post


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


class PostEmbedded(PostBase):
    id: int
    created_at: datetime
    owner: UserResponse

    class Config:
        orm_mode = True


class PostResponse(BaseModel):
    Post: PostEmbedded
    votes: int

    class Config:
        orm_mode = True


class VoteCreate(BaseModel):
    post_id: int
    direction: conint(le=1)
