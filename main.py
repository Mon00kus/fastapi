from typing import Optional
from fastapi import FastAPI
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

# Just for demotraiting porpurse
#@app.get("/post/latest")
#def get_latest_post():
    #post = my_post_list[len(my_post_list)-1]
    #return {"detail": post}

@app.get("/posts/{id}")
def create_posts(id: int):
    # print(id)
    post = find_post(id)
    return {"post_detail": post}
