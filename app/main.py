from typing import Optional
from fastapi import FastAPI, HTTPException, status
from fastapi.params import Body
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="fastapi",
            user="postgres",
            password="postgres",
            cursor_factory=RealDictCursor,
        )

        print("Connecting to database!")
        break

    except Exception as e:
        print("Could not connect to Database")
        print("Error: " + e.message)
        time.sleep(3)


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
