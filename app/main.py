

from typing import List, Optional
from importlib.resources import contents
from pydantic import BaseModel

from turtle import title
from random import randrange
from fastapi import FastAPI,Response,status,HTTPException,Depends
from fastapi.params import Body
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session 
from sqlalchemy.sql.functions import mode
from . import models
from .database import  engine,get_db
from .router import post,users,auth




models.Base.metadata.create_all(bind=engine)



while True:
    try:
        conn=psycopg2.connect(host='localhost',database='FastApi',user='postgres',password='01030262529',cursor_factory=RealDictCursor)
        cursor=conn.cursor()
        print("Database connection was succefull!!")
        break
    except Exception as error:
        print("connected to database failed ")
        print("the error was",error)
        time.sleep(2)

    My_Posts=[{"title":"title of post","content":"content of post 1", "id": 1 },{"title":"favourite food","content":"I like pizza","id":2   
    },
    {
    "title":"Profile",
    "content":"Facebook Profile",
    "id":3,
    "url":"https://www.facebook.com/khaled.ashraf.1865",
    "urlToImage":"https://media-exp1.licdn.com/dms/image/C4D03AQFP4v0cMMBtUA/profile-displayphoto-shrink_800_800/0/1627830998025?e=1666224000&v=beta&t=Xy5ZlPrOQNmZ766WzY-x30sgeRVSMtlzSdZwbUdK7r4"

}
]



app=FastAPI()
def find_index_post(id):
    for i,p in enumerate(My_Posts):
        if p['id']==id:
            return i
def find_posts(id):
    for p in My_Posts:
        if p["id"]==id:
            return p


app.include_router(post.router)
app.include_router(users.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"Hello": "Welcome to my Api!!!"}








# @app.get("/posts/latestPost")
# def get_latest_post():
#     post=My_Posts[len(My_Posts)-1]
#     return {"detail":post}






