from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


class StudentModel(BaseModel):
    id: Optional[UUID]
    first_name: str
    last_name: str
    patronymic: str
    dob: datetime
