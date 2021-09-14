from typing import Optional
from pydantic import BaseModel
from uuid import UUID
from datetime import date


class StudentSerializer(BaseModel):
    code: Optional[UUID]
    first_name: str
    last_name: str
    middle_name: str
    dob: date
