from fastapi import APIRouter

from typing import List
from fastapi import status, Response
from fastapi.exceptions import HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from .. import schemas
from ..database import get_db
from ..models import User

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# USER CRUD


@router.post('/user', status_code=status.HTTP_201_CREATED, tags=['users'])
def create(request: schemas.CreateUserDto, db: Session = Depends(get_db)):

    hashed_password = pwd_context.hash(request.password)
    new_user = User(username=request.username,
                    password=hashed_password,
                    email=request.email)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/user/{user_id}', status_code=status.HTTP_200_OK, response_model=schemas.UserResponse, tags=['users'])
def get_by_id(user_id: int, response: Response, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        description = {'data': f'user with id \'{user_id}\' is not found'}
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=description)

    return user
