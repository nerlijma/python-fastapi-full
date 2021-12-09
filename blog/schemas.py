from pydantic import BaseModel


class CreateBlogDto(BaseModel):
    title: str
    body: str


class UpdateBlogDto(BaseModel):
    title: str
    body: str


class BlogResponse(BaseModel):
    title: str
    body: str

    class Config():
        orm_mode = True


class CreateUserDto(BaseModel):
    username: str
    email: str
    password: str
