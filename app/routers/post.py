from fastapi import Depends, FastAPI, Response, HTTPException, status, APIRouter
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from typing import List
from app.oauth import get_current_user
from .. import schema
from .. import models
from ..database import get_db


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get("/", response_model=List[schema.PostResponse])
def get_posts(db: Session = Depends(get_db),
              tokenData: schema.TokenData = Depends(get_current_user)):
    # Query directly to the db
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    # Query using sqlalchemy
    posts = db.query(models.Post).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.PostResponse,)
def create_posts(post: schema.PostCreate, db: Session = Depends(get_db),  tokenData: schema.TokenData = Depends(get_current_user)):

    # Query directly to the db
    # we use this way instad f formating, for avoid sql injection
    # cursor.execute("""INSERT INTO posts (title, content, published, rating) VALUES (%s,%s,%s,%s) RETURNING *""",
    # (post.title, post.content, post.published, post.rating))
    #newPost = cursor.fetchone()
    # conn.commit()

    # Query using sqlalchemy
    # **post.dict() is like ...obj in javascript
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get('/{id}', response_model=schema.PostResponse)
def get_post(id: int, response: Response, db: Session = Depends(get_db), tokenData: schema.TokenData = Depends(get_current_user)):

    # Query directly to the db
    #cursor.execute("""SELECT * FROM posts WHERE posts.id = %s""", (str(id)))
    #post = cursor.fetchone()

    # Using sqlalchemy
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
#         response.status_code = HTTPStatus.NOT_FOUND
#         return {"message": "the post was not found"}

    return post


@router.delete('/', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),  tokenData: schema.TokenData = Depends(get_current_user)):

    # Query directly to the db
    # cursor.execute(
    #    """DELETE FROM posts WHERE posts.id = %s RETURNING *""", (str(id)))
    #deleted_post = cursor.fetchone()
    # conn.commit()

    # Using sqlalchemy
    query = db.query(models.Post).filter(models.Post.id == id)

    if query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")

    query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{id}', response_model=schema.PostResponse, )
def update_post(id: int, post: schema.PostCreate,  db: Session = Depends(get_db),  tokenData: schema.TokenData = Depends(get_current_user)):
    # Query directly to the db
    # cursor.execute(
    #    """UPDATE posts SET title = %s, content = %s, published = %s, rating = %s  WHERE id = %s RETURNING *""", (
    #        post.title, post.content, post.published, post.rating,  str(id),
    #    ))
    #updated_post = cursor.fetchone()
    # conn.commit()

    # Using sqlalchemny
    query = db.query(models.Post).filter(models.Post.id == id)

    if query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")

    query.update(post.dict(), synchronize_session=False)
    db.commit()
    return {"data": query.first()}
