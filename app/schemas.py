from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional

from pydantic.types import conint


class Base(BaseModel):
    class Config:
        orm_mode = True


class UserBase(Base):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserData(UserBase):
    id: int


class UserLogin(UserCreate):
    pass


class PostBase(Base):
    title: str
    content: str
    published: bool = True


class Post(PostBase):
    id: int
    created_at: datetime
    owner: UserData


class PostResult(Base):
    Post: Post
    vote: int


class PostCreate(PostBase):
    pass


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str]


class Vote(BaseModel):
    post_id: int
    dir: conint(ge=0, le=1)
