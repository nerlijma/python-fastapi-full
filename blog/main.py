from fastapi import FastAPI, Response
from fastapi.security import OAuth2PasswordBearer
from fastapi.exceptions import HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from . import models
from .database import engine
from .models import Blog
from blog import database
from .routers import user, blog, auth
from blog.stock_Index.routers import stock_index
import pathlib

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

models.Base.metadata.create_all(engine)

# Dependency
get_db = database.get_db

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(blog.router)
app.include_router(blog.router)
app.include_router(stock_index.router)

print(__file__)
HERE = pathlib.Path(__file__)
print(HERE)
print(HERE.resolve())
