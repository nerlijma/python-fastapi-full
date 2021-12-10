from typing import List
from fastapi import FastAPI, status, Response
from fastapi.exceptions import HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from . import schemas, models
from .database import SessionLocal, engine
from .models import Blog, User

app = FastAPI()

models.Base.metadata.create_all(engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Dependency


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/blog', status_code=status.HTTP_201_CREATED, tags=['blogs'])
def create(request: schemas.CreateBlogDto, db: Session = Depends(get_db)):
    new_blog = Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get('/blog', response_model=List[schemas.BlogResponse], tags=['blogs'])
def get_all(db: Session = Depends(get_db)):
    blogs = db.query(Blog).all()
    return blogs


@app.get('/blog/{blog_id}', status_code=status.HTTP_200_OK, tags=['blogs'])
def get_by_id(blog_id: int, response: Response, db: Session = Depends(get_db)):
    blog = db.query(Blog).filter(Blog.id == blog_id).first()
    if not blog:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'data': f'blog with id \'{blog_id}\' is not found'}
        description = {'data': f'blog with id \'{blog_id}\' is not found'}
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=description)

    return blog


@app.delete('/blog/{blog_id}', status_code=status.HTTP_200_OK, tags=['blogs'])
def delete(blog_id: int, db: Session = Depends(get_db)):
    blog = db.query(Blog).filter(Blog.id == blog_id).first()
    if not blog:
        description = {'data': f'blog with id \'{blog_id}\' is not found'}
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=description)

    # Delete de blog
    db.delete(blog)
    db.commit()
    description = {'data': f'blog with id \'{blog_id}\' has been deleted'}
    return {'data': description}


@app.put('/blog/{blog_id}', status_code=status.HTTP_202_ACCEPTED, tags=['blogs'])
def update(blog_id: int, request: schemas.UpdateBlogDto, db: Session = Depends(get_db)):
    blog = db.query(Blog).filter(Blog.id == blog_id)
    if not blog.first():
        description = {'data': f'blog with id \'{blog_id}\' is not found'}
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=description)

    # Update the blog
    blog.update({Blog.title: request.title, Blog.body: request.body})
    db.commit()

    return {'data': f'blog with id \'{blog_id}\' has been updated'}


# USER CRUD

@app.post('/user', status_code=status.HTTP_201_CREATED, tags=['users'])
def create(request: schemas.CreateUserDto, db: Session = Depends(get_db)):

    hashed_password = pwd_context.hash(request.password)
    new_user = User(username=request.username,
                    password=hashed_password,
                    email=request.email)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get('/user/{user_id}', status_code=status.HTTP_200_OK, response_model=schemas.UserResponse, tags=['users'])
def get_by_id(user_id: int, response: Response, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        description = {'data': f'user with id \'{user_id}\' is not found'}
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=description)

    return user
