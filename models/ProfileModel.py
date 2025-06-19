from pydantic import BaseModel, Field

class ChangeUsernameModel(BaseModel):
    username: str = Field(..., min_length=5, max_length=20)