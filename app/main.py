from typing import List
from fastapi import FastAPI, HTTPException, status
from fastapi.params import Depends
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello, new stuff"}


@app.get(
    "/posts/{id}",
    response_model=schemas.Post,
)
async def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).get(id)
    return post


@app.get("/posts", response_model=List[schemas.Post])
async def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@app.post("/posts", status_code=201, response_model=schemas.Post)
async def create_posts(post: schemas.Post, db: Session = Depends(get_db)):

    new_post = models.Post(**post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post
