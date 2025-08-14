from ast import While
from typing import Optional
from fastapi import FastAPI, HTTPException, Response, status, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models 
from .database import engine, get_db

models.Base.metadata.create_all(bind = engine)

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    ##category: str
    published: bool = True
    
    # rating: Optional[int] = None
    
while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi',
                                user='postgres', password='123', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was succesfull !!!")
        break
      
    except Exception as error:
        print("Connecton to database failed !!!")
        print("Error: ", error)
        time.sleep(2)


my_post_list = [
    {"title": "title of post 1", "content": "content of post 1", "id": 1},
    {"title": "favorite foods", "content": "i like pizza", "id": 2},
]


def find_post(id):
  
    for post in my_post_list:
        if post["id"] == id:
            return post


def find_index_post(id):
  
    for i, post in enumerate(my_post_list):
        if post['id'] == id:
            return i


@app.get("/")
def root():
  
    return {"message": "Hello World"}


@app.get("/posts")
def get_posts():
  
    cursor.execute("""SELECT * FROM post""")
    posts = cursor.fetchall()
    print(posts)
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
  
    #cursor.execute(f"INSERT INTO post (title, content, published) VALUES ({post.title},{post.content}{post.published})") NEVER USE THIS IT CAN BE USE TO INJECT WEAR/MALICIOUS SQL COMMANDS INTO DATABASE
    cursor.execute("""INSERT INTO post (title, content, published) VALUES (%s,  %s, %s) RETURNING * """, (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}


@app.get("/posts/{id}")
def get_posts(id: int):
  
    cursor.execute("""SELECT * FROM post WHERE id = %s """, (str(id)))
    retrieve_one_post = cursor.fetchone()
    
    if not retrieve_one_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return {"post_detail": retrieve_one_post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int):
  
    cursor.execute("""DELETE FROM post WHERE id = %s RETURNING * """, (str(id),))
    delete_one_post = cursor.fetchone()
    
    conn.commit()
    
    if delete_one_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} does not exist")      
        
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    
    cursor.execute("""UPDATE post SET title = %s, content= %s, published= %s WHERE id= %s  RETURNING * """, (post.title, post.content, post.published, str(id) ))
        
    updated_post = cursor.fetchone()
    
    conn.commit()
    
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} does not exist")
        
    return {"data": updated_post}

@app.get("/sqlAlquemy")
def test_post(db: Session = Depends(get_db)): 

    return {"Status": "success"}