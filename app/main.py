from array import array
from http import HTTPStatus
from typing import Optional
from fastapi import Body, Depends, FastAPI, Response, HTTPException, status
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


while True:
    try:
        conn = psycopg2.connect(host="localhost", database="fastapi",
                                user="postgres", password="root", port="5433", cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successfully")
        break
    except Exception as error:
        print('There was an error connecting to the database')
        print('Error: ', error)
        time.sleep(2)


myPosts: array = [{"title": "Post title 1",
                   "content": "Post 1 content", "id": 1},
                  {"title": "Post title 2",
                   "content": "Post 2 content", "id": 2},
                  {"title": "Post title 3",
                   "content": "Post 3 content", "id": 3}]


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


@app.get("/")
def root():
    return {"message": "Hellow papi"}


@app.get('/posts')
def get_posts(db: Session = Depends(get_db)):
    # Query directly to the db
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()

    # Query using sqlalchemy
    posts = db.query(models.Post).all()
    return {"data": posts}


@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_posts(post: Post, db: Session = Depends(get_db)):

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
    return {"data": new_post}


@app.get('/posts/{id}')
def get_post(id: int, response: Response, db: Session = Depends(get_db)):

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


@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):

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


@app.put('/posts/{id}')
def update_post(id: int, post: Post,  db: Session = Depends(get_db)):
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


@app.get('/test')
def test(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    print(posts)

    return {"data": posts}
