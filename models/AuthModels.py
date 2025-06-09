from pydantic import BaseModel, Field, EmailStr

class RegisterModel(BaseModel):
    username: str = Field(..., min_length=5, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=64)

class LoginModel(BaseModel):
    username: str = Field(..., min_length=5, max_length=50)
    password: str = Field(..., min_length=8, max_length=64)