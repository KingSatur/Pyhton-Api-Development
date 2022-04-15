from array import array
from http import HTTPStatus
from typing import Optional
from fastapi import Body, FastAPI, Response, HTTPException, status
from pydantic import BaseModel
from random import randrange

app = FastAPI()


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
def get_posts():
    return {"data": myPosts}


@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dic = post.dict()
    post_dic['id'] = randrange(0, 10000000)
    myPosts.append(post_dic)
    return {"data": post_dic}


@app.get('/posts/{id}')
def get_post(id: int, response: Response):
    post_search = next(filter(lambda post: post['id'] == id, myPosts), None)
    if not post_search:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
#         response.status_code = HTTPStatus.NOT_FOUND
#         return {"message": "the post was not found"}

    return post_search


@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = next((i for i, post in enumerate(
        myPosts) if post['id'] == id), None)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    myPosts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put('/posts/{id}')
def update_post(id: int, post: Post):
    index = next((i for i, post in enumerate(
        myPosts) if post['id'] == id), None)

    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    post_dict = post.dict()
    post_dict['id'] = id
    myPosts[index] = post_dict
    return {"data": post_dict}
