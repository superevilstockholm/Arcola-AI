from pydantic import BaseModel, EmailStr, Field

class ChangeUsernameModel(BaseModel):
    username: str = Field(..., min_length=5, max_length=20, pattern=r"^[a-zA-Z0-9_]{5,20}$")

class ChangeEmailModel(BaseModel):
    email: EmailStr