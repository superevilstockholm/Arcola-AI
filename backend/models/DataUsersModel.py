from pydantic import BaseModel, Field, EmailStr
from typing import Literal

class CreateDataUsersModel(BaseModel):
    username: str = Field(..., min_length=5, max_length=20, pattern=r"^[a-zA-Z0-9_]{5,20}$")
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=64, description="Password must contain at least one letter, one number, and one special character")

class EditDataUsersModel(BaseModel):
    username: str = Field(..., min_length=5, max_length=20, pattern=r"^[a-zA-Z0-9_]{5,20}$")
    email: EmailStr
    password: str | None = Field(default=None, min_length=8, max_length=64, description="Password must contain at least one letter, one number, and one special character")
    user_type: Literal["user", "admin"]
    verified_email: bool