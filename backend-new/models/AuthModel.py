from pydantic import BaseModel, Field, EmailStr

class RegisterModel(BaseModel):
    username: str = Field(..., min_length=5, max_length=20, pattern=r"^[a-zA-Z0-9_]{5,20}$")
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=64, description="Password must contain at least one letter, one number, and one special character")

class LoginModel(BaseModel):
    username: str = Field(..., min_length=5, max_length=20, pattern=r"^[a-zA-Z0-9_]{5,20}$")
    password: str = Field(..., min_length=8, max_length=64)

class ResetPasswordByPasswordModel(BaseModel):
    old_password: str = Field(..., min_length=8, max_length=64)
    new_password: str = Field(..., min_length=8, max_length=64)