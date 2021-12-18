from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db

router = APIRouter()


@router.post("/users", status_code=201, response_model=schemas.UserData)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    user.password = utils.hash(user.password)

    new_user = models.User(**user.dict())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get(
    "/users/{id}",
    response_model=schemas.UserData,
)
async def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).get(id)

    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"No User with Id: {id}")
    return user
