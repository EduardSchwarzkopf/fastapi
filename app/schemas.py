from pydantic import BaseModel, EmailStr


class Base(BaseModel):
    class Config:
        orm_mode = True


class Post(Base):
    id: int
    title: str
    content: str
    published: bool = True


class UserBase(Base):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserData(UserBase):
    id: int
