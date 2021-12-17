from typing import Optional
from fastapi import FastAPI, Response, status
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
async def get_post(id: int, response: Response):
    response.status_code = status.HTTP_404_NOT_FOUND
    return {"data": f"post_id: {id}"}


@app.get("/posts")
async def get_posts():
    return {"data": "data"}


@app.post("/posts")
async def create_posts(payload: Post):
    return {"message": payload}
