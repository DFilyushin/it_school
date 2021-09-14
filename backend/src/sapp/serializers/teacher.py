from pydantic import BaseModel
from datetime import date
from uuid import UUID


class TeacherSerializer(BaseModel):
    code: UUID
    first_name: str
    last_name: str
    patronymic: str
    dob: date
