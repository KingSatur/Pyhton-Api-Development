from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session

from app import oauth
from .. import schema
from .. import models
from ..database import get_db
from .. import util


router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post("/login", response_model=schema.UserLoginResponse)
def login(loginCommand: schema.UserLoginCommand, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(
        models.User.email == loginCommand.email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    if not util.verify(loginCommand.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")

    # Create token
    access_token = oauth.create_access_token(data={"user_id": user.id})
    return schema.UserLoginResponse(email=user.email, token=access_token)
