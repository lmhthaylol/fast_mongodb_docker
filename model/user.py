from typing import Optional
from pydantic import BaseModel, Field

class UserRegister(BaseModel):
    username: str
    password: str
    email: Optional[str] = None
    role: Optional[str] = Field(default="Reader")

class UserLogin(BaseModel):
    username: str
    password: str

class CurrentUser(BaseModel):
    username: str
    role: str
    email: Optional[str] = None