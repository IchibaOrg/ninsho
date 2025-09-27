from fastapi import APIRouter, Form, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from datetime import timedelta

from sqlalchemy import select

from ninsho.api.dependency import get_current_user
from ninsho.api.utils import verify_password, create_access_token, hash_password
from ninsho.db.base import get_db_session
from ninsho.db.user import User
from ninsho.models.user import RegisterUserRequest

router = APIRouter()


@router.post("/auth/token")
async def login(username: str = Form(...), password: str = Form(...)):
    async with get_db_session() as session:
        query = select(User).where(User.username == username)
        user = (await session.execute(query)).scalar_one_or_none()

        if not user or not verify_password(password, user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

        token = create_access_token({"sub": str(user.id)}, timedelta(minutes=30))

        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "access_token": token,
                "message": "user logged in!"
            }
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
