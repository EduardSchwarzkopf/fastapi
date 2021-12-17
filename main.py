from fastapi import FastAPI
from fastapi.params import Body


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello, new stuff"}


@app.post("/create")
async def create(payload: dict = Body(...)):
    return {"message": payload}
