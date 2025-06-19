from pydantic import BaseModel
from typing import Optional

class BaseResponse(BaseModel):
    status: bool
    message: str
    detail: Optional[dict]