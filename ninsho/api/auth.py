from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from sqlalchemy import select

from ninsho.api.dependency import get_current_user
from ninsho.api.utils import verify_password, create_access_token, hash_password
from ninsho.db.base import get_db_session
from ninsho.db.user import User
from ninsho.models.user import RegisterUserRequest, Token

router = APIRouter()

ACCESS_TOKEN_EXPIRE_MINUTES = 30

@router.post("/auth/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()])-> Token:
    async with get_db_session() as session:
        query = select(User).where(User.username == form_data.username)
        user = (await session.execute(query)).scalar_one_or_none()

        if not user or not verify_password(form_data.password, user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

        token = create_access_token({"sub": str(user.id)}, timedelta(ACCESS_TOKEN_EXPIRE_MINUTES))

        return Token(
                access_token=token,
                token_type="bearer",
                message="user logged in!",
        )


@router.post("/auth/sign-up", status_code=status.HTTP_201_CREATED)
async def register(request: RegisterUserRequest):
    async with get_db_session() as session:
        existing_user = await session.execute(
            select(User).where(User.username == request.username)
        )

        if existing_user.scalar_one_or_none():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")


        hashed_password = hash_password(request.password)
        user = User(username=request.username, email=request.email, password=hashed_password)

        session.add(user)
        await session.commit()

        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "message": "User registered successfully",
                "user": {"username": user.username, "email": user.email},
            }
        )


@router.get("/users/me")
def read_me(current_user: str = Depends(get_current_user)):
    return {"user": current_user}
