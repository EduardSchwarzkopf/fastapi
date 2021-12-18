from typing import Optional
from fastapi import FastAPI, HTTPException, status
from fastapi.params import Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


@app.get("/")
async def root():
    return {"message": "Hello, new stuff"}


@app.get("/posts/{id}")
async def get_post(id: int, db: Session = Depends(get_db)):
    raise HTTPException(status.HTTP_404_NOT_FOUND, detail="nothing found")
    return {"data": f"post_id: {id}"}


@app.get("/posts")
async def get_posts():
    return {"data": "data"}


@app.post("/posts", status_code=201)
async def create_posts(post: Post, db: Session = Depends(get_db)):

    new_post = models.Post(**post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {"data": new_post}
