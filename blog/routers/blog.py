from fastapi import APIRouter

from typing import List
from fastapi import status, Response
from fastapi.exceptions import HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from .. import schemas
from ..database import get_db
from ..models import Blog

router = APIRouter()


@router.post('/blog', status_code=status.HTTP_201_CREATED, tags=['blogs'])
def create(request: schemas.CreateBlogDto, db: Session = Depends(get_db)):
    new_blog = Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@router.get('/blog', response_model=List[schemas.BlogResponse], tags=['blogs'])
def get_all(db: Session = Depends(get_db)):
    blogs = db.query(Blog).all()
    return blogs


@router.get('/blog/{blog_id}', status_code=status.HTTP_200_OK, tags=['blogs'])
def get_by_id(blog_id: int, response: Response, db: Session = Depends(get_db)):
    blog = db.query(Blog).filter(Blog.id == blog_id).first()
    if not blog:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'data': f'blog with id \'{blog_id}\' is not found'}
        description = {'data': f'blog with id \'{blog_id}\' is not found'}
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=description)

    return blog


@router.delete('/blog/{blog_id}', status_code=status.HTTP_200_OK, tags=['blogs'])
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


@router.put('/blog/{blog_id}', status_code=status.HTTP_202_ACCEPTED, tags=['blogs'])
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
