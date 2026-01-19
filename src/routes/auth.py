from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from config.database import get_db
from schemas.user import UserCreate, AuthResponse, Token
from repositories.user_repository import (
    create_user,
    get_user_by_email,
    authenticate_user
)
from utils.security import create_access_token

router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])


@router.post(
    "/signup",
    response_model=AuthResponse,
    status_code=status.HTTP_201_CREATED
)
def signup(user_in: UserCreate, db: Session = Depends(get_db)):
    if get_user_by_email(db, user_in.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    user = create_user(db, user_in)

    access_token = create_access_token(
        data={"sub": user.email}
    )

    return {
        "user": user,
        "access_token": access_token,
        "token_type": "bearer"
    }



@router.post("/login", response_model=AuthResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    access_token = create_access_token(
        data={"sub": user.email}
    )

    return {
        "user": user,
        "access_token": access_token,
        "token_type": "bearer",
    }

