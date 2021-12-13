from datetime import timedelta
from typing import Optional
from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.params import Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session

from blog.database import get_db
from blog.models import User
from ..auth import ACCESS_TOKEN_EXPIRE_MINUTES, INVALID_CREDENTIALS_EXCEPTION, Token, authenticate_user, create_access_token

router = APIRouter(
    tags=["auth"]
)


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise INVALID_CREDENTIALS_EXCEPTION

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
