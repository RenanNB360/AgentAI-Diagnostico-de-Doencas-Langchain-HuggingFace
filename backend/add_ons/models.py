from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    name: str
    gender: Optional[str] = None
    age: Optional[int] = None
    date: str
    time: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    gender: Optional[str] = None
    age: Optional[int] = None
    date: Optional[str] = None
    time: Optional[str] = None
