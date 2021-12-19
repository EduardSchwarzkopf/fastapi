from typing import List
from fastapi import Depends, APIRouter, Response, status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get(
    "/{id}",
    response_model=schemas.Post,
)
async def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).get(id)
    return post


@router.get("/", response_model=List[schemas.Post])
async def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@router.post("/", status_code=201, response_model=schemas.Post)
async def create_posts(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):

    new_post = models.Post(owner_id=current_user.id, **post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    post = db.query(models.Post).get(id)

    if post == None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, f"Could not find post with id: {id}"
        )

    if post.owner_id != current_user.id:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN, "Not authorized to perfom requested action"
        )

    db.delete(post)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
