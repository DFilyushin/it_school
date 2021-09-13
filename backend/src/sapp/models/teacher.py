from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


class TeacherModel(BaseModel):
    code: UUID
    first_name: str
    last_name: str
    patronymic: str
    dob: datetime
