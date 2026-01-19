from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from authlib.integrations.starlette_client import OAuth
from starlette.responses import RedirectResponse

from config.database import get_db
from config.google_oauth import (
    GOOGLE_CLIENT_ID,
    GOOGLE_CLIENT_SECRET,
    GOOGLE_CALLBACK_URL
)
from repositories.user_repository import (
    get_user_by_google_id,
    create_google_user
)
from utils.security import create_access_token
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from authlib.integrations.starlette_client import OAuth
from starlette.responses import RedirectResponse

from config.database import get_db
from config.google_oauth import (
    GOOGLE_CLIENT_ID,
    GOOGLE_CLIENT_SECRET,
    GOOGLE_CALLBACK_URL
)
from repositories.user_repository import (
    get_user_by_google_id,
    create_google_user
)
from utils.security import create_access_token
from schemas.user import UserResponse
from dependencies.auth import get_current_user

router = APIRouter(
    prefix="/api/v1/auth/google",
    tags=["Auth"]
)

oauth = OAuth()

oauth.register(
    name="google",
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={
        "scope": "openid email profile"
    }
)







router = APIRouter(
    prefix="/api/v1/auth/google",
    tags=["Auth"]
)

oauth = OAuth()

oauth.register(
    name="google",
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={
        "scope": "openid email profile"
    }
)


@router.get("/login")
async def google_login(request: Request):
    redirect_uri = GOOGLE_CALLBACK_URL
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/callback")
async def google_callback(
    request: Request,
    db: Session = Depends(get_db)
):
    token = await oauth.google.authorize_access_token(request)
    user_info = token.get("userinfo")

    if not user_info:
        raise HTTPException(status_code=400, detail="Google auth failed")

    google_id = user_info["sub"]
    email = user_info["email"]
    name = user_info.get("name", email)

    user = get_user_by_google_id(db, google_id)
    if not user:
        user = create_google_user(
            db,
            google_id=google_id,
            email=email,
            name=name
        )

    access_token = create_access_token(
        data={"sub": user.email}
    )

    frontend_url = (
        f"http://localhost:5173/auth/google/callback"
        f"?token={access_token}"
    )

    return RedirectResponse(frontend_url)


@router.get("/me", response_model=UserResponse)
def get_me(current_user = Depends(get_current_user)):
    return current_user

