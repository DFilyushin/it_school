from typing import List
from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID


class GroupModel(BaseModel):
    code: UUID
    name: str


class UserModel(BaseModel):
    login: str = Field(min_length=8, max_length=31)
    created: datetime = Field(default_factory=datetime.utcnow())
    full_name: str = Field(min_length=8, max_length=255)
    email: str
    phone: str
    password: str
    groups: List[UUID]
