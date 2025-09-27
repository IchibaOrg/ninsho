from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from ninsho.db.base import BaseModel


class User(BaseModel):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True, init=False)
    username: Mapped[str] = mapped_column(String(50), unique=True,nullable=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)

