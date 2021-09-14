from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID, uuid4


class TeacherModel(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    first_name: str
    last_name: str
    patronymic: str
    dob: datetime
