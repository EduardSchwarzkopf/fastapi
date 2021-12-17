from typing import Optional
from fastapi import FastAPI, HTTPException, status
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


@app.get("/posts/{id}")
async def get_post(id: int):
    raise HTTPException(status.HTTP_404_NOT_FOUND, detail="nothing found")
    return {"data": f"post_id: {id}"}


@app.get("/posts")
async def get_posts():
    return {"data": "data"}


@app.post("/posts", status_code=201)
async def create_posts(payload: Post):
    return {"message": payload}
