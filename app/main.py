from fastapi import FastAPI
from . import models
from .database import engine
from .routers import users, posts, auth, vote

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
async def root():
    return {"message": "Hello, new stuff"}
