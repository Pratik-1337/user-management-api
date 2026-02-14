from pydantic import BaseModel, Field
from typing import Optional

class UserCreate(BaseModel):
    name: str = Field(min_length=2)
    age: int = Field(gt=0)
    profession: Optional[str] = None

class UserUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    profession: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    name: str
    age: int
    profession: str