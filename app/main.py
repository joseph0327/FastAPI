# from typing import Optional, List

# from fastapi.params import Body
# from random import randrange
# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time
# from sqlalchemy.orm import Session

from fastapi import FastAPI, Response,status, HTTPException, Depends
from . import models, schemas, utils
from . database import engine, SessionLocal, get_db
from . routers import post, users, auth, vote
from pydantic_settings import BaseSettings
from . config import settings
from fastapi.middleware.cors import CORSMiddleware


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(post.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def get_all_post():
    return {"details":"hello"}
# -------------------------------------
#  FUNCTIONS
# -------------------------------------

# def find_post(id):
#     for p in my_post:
#         if p['id'] == id:
#             return p
        
# def find_index_post(id):
#     for i,p in enumerate(my_post):
#         if p['id'] == id:
#             return i

