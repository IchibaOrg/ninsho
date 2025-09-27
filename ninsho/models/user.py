from pydantic import BaseModel, EmailStr


class RegisterUserRequest(BaseModel):
    username: str
    email: EmailStr
    password: str


class RegisterResponse(BaseModel):
    message: str
    user: dict