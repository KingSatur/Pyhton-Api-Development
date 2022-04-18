from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session

from app.oauth import get_current_user
from .. import schema
from .. import models
from .. import util
from ..database import get_db

router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_user(vote: schema.VoteCreate, db: Session = Depends(get_db),  tokenData: schema.TokenData = Depends(get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post not found")
    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id, models.Vote.user_id == tokenData.id)
    found_vote = vote_query.first()
    if vote.direction == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"forbidden operation")
        vote_model = models.Vote(user_id=tokenData.id, post_id=vote.post_id)
        db.add(vote_model)
        db.commit()
        return {"message": "Vote has been created"}
    else:
        if found_vote is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Vote was deleted"}
