from typing import List
from fastapi import FastAPI, HTTPException, status
from fastapi.params import Depends
from sqlalchemy.orm import Session
from . import models, schemas
from .utils import hash
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


@app.get("/users", response_model=List[schemas.UserData])
async def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


@app.post("/users", status_code=201, response_model=schemas.UserData)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    user.password = hash(user.password)

    new_user = models.User(**user.dict())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@app.get(
    "/users/{id}",
    response_model=schemas.UserData,
)
async def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).get(id)
    return user
