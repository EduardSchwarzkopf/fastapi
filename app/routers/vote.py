from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from starlette.status import HTTP_404_NOT_FOUND
from .. import schemas, database, models, oauth2

router = APIRouter(prefix="/vote", tags=["Vote"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(
    vote: schemas.Vote,
    db: Session = Depends(database.get_db),
    current_user: int = Depends(oauth2.get_current_user),
):

    post = db.query(models.Post).get(vote.post_id)

    if not post:
        raise HTTPException(HTTP_404_NOT_FOUND, "Post not found")

    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id
    )
    found_vote = vote_query.first()
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status.HTTP_409_CONFLICT, "Vote already exists")

        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()

        return {"message": "vote added"}

    else:

        if not found_vote:
            raise HTTPException(HTTP_404_NOT_FOUND, "Vote not found")

        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "vote deleted"}
