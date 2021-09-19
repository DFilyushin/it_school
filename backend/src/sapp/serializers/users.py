from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr


class UserSerializer(BaseModel):
    login: str = Field(min_length=8, max_length=31)
    full_name: str = Field(min_length=8, max_length=255)
    email: EmailStr
    phone: str
    password: Optional[str]
    groups: List[str]
