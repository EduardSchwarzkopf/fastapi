from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


@app.get("/")
async def root():
    return {"message": "Hello, new stuff"}


@app.get("/posts")
async def get_posts():
    return {"data": "data"}


@app.post("/posts")
async def create_posts(payload: Post):
    return {"message": payload}
