from pydantic import BaseModel, Field
from typing import Optional

class User(BaseModel):
    user_id: str
    username: str
    hashed_password: str
    role: str = Field(description="Role: admin, analyst, or viewer")
    is_active: bool = True

class UserCreate(BaseModel):
    username: str
    password: str
    role: str = "viewer"

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None
