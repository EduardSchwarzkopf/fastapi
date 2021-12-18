from pydantic import BaseModel, EmailStr
from typing import Optional


class Base(BaseModel):
    class Config:
        orm_mode = True


class PostBase(Base):
    title: str
    content: str
    published: bool = True


class Post(PostBase):
    id: int


class PostCreate(PostBase):
    pass


class UserBase(Base):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserData(UserBase):
    id: int


class UserLogin(UserCreate):
    pass


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str]
