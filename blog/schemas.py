from typing import List
from pydantic import BaseModel

from blog.models import User


class CreateBlogDto(BaseModel):
    title: str
    body: str


class UpdateBlogDto(BaseModel):
    title: str
    body: str


class User(BaseModel):
    username: str
    email: str

    class Config():
        orm_mode = True


class Blog(BaseModel):
    title: str
    body: str

    class Config():
        orm_mode = True


class BlogResponse(Blog):
    user: User

    class Config():
        orm_mode = True


class UserResponse(User):
    blogs: List[Blog]

    class Config():
        orm_mode = True


class CreateUserDto(BaseModel):
    username: str
    email: str
    password: str
