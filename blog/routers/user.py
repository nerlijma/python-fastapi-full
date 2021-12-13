from fastapi import APIRouter
from fastapi.security import OAuth2PasswordBearer
from ..encrypt import pwd_context
from typing import List
from fastapi import status, Response
from fastapi.exceptions import HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from .. import schemas
from ..database import get_db
from ..models import User


router = APIRouter(
    tags=["users"],
    prefix="/user"
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post('/', status_code=status.HTTP_201_CREATED)
def create(
        request: schemas.CreateUserDto,
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)):

    hashed_password = pwd_context.hash(request.password)
    new_user = User(username=request.username,
                    password=hashed_password,
                    email=request.email)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/{user_id}', status_code=status.HTTP_200_OK, response_model=schemas.UserResponse)
def get_by_id(
        user_id: int,
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)):

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        description = {'data': f'user with id \'{user_id}\' is not found'}
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=description)

    return user
