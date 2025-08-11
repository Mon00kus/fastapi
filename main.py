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


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/posts")
async def get_posts():
    return {"data": my_post_list}


# @app.post("/createpost")
@app.post("/posts")
# def createpost(payload: dict = Body(...)):
def createpost(post: Post):
    # print(payload)
    # return {"nes_post": f"title: {payload['title']} content: {payload['content']}"}
    # print(post.rating)
    #print(post)
    #print(post.dict())
    my_post_list.append(post.dict())
    return {"data": post}
