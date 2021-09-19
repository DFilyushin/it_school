from typing import Optional
from pydantic import BaseModel
from uuid import UUID
from datetime import date


class StudentSerializer(BaseModel):
    id: Optional[UUID]
    first_name: str
    last_name: str
    patronymic: str
    dob: date
