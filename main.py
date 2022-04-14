from typing import Optional
from fastapi import Body, FastAPI
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


@app.get("/")
async def root():
    return {"message": "Hellow papi"}


@app.get('/posts')
def get_posts():
    return []


@app.post('/posts')
def create_posts(post: Post):
    print(post.title)
    print(post.dict())
    return {"data": post}
