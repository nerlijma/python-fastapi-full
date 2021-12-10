from typing import List
from fastapi import FastAPI, status, Response
from fastapi.exceptions import HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from . import schemas, models
from .database import engine
from .models import Blog
from blog import database
from .routers import user, blog

app = FastAPI()

models.Base.metadata.create_all(engine)


# Dependency
get_db = database.get_db

app.include_router(user.router)
app.include_router(blog.router)
