from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID, uuid4


class TeacherModel(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    first_name: str
    last_name: str
    patronymic: str
    dob: datetime

    @property
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'
