from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils, oauth2

router = APIRouter(tags=["Authentication"])


@router.post("/login")
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db),
):

    user = (
        db.query(models.User)
        .filter(models.User.email == user_credentials.username)
        .first()
    )

    if not user or not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    user_data = {"user_id": user.id}
    access_token = oauth2.create_access_token(data=user_data)

    return {"access_token": access_token, "token_type": "bearer"}
