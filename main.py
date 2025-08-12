from ast import While
from typing import Optional
from fastapi import FastAPI, HTTPException, Response, status
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    category: str
    published: bool = True
    rating: Optional[int] = None


my_post_list = [
    {"title": "title of post 1", "content": "content of post 1", "id": 1},
    {"title": "favorite foods", "content": "i like pizza", "id": 2},
]


def find_post(id):
    for post in my_post_list:
        if post["id"] == id:
            return post


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/posts")
def get_posts():
    return {"data": my_post_list}


@app.post("/posts")
def create_post(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000000)
    my_post_list.append(post_dict)
    return {"data": post_dict}


@app.get("/posts/{id}")
def create_posts(id: int, response: Response):
    post = find_post(id)
    if not post:      
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                          detail=f"post with id: {id} was not found")
    return {"post_detail": post}