from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session

from app.oauth import get_current_user
from .. import schema
from .. import models
from .. import util
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schema.UserResponse)
def create_user(user: schema.UserCreate, db: Session = Depends(get_db),  tokenData: schema.TokenData = Depends(get_current_user)):
    user.password = util.hash(user.password)
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/{id}', response_model=schema.UserResponse)
def get_user(id: int, db: Session = Depends(get_db),  tokenData: schema.TokenData = Depends(get_current_user)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id: {id} was not found")

    return user
