from typing import Optional, List
from pydantic import BaseModel
from uuid import UUID
from datetime import date


class SchoolClassSerializer(BaseModel):
    id: Optional[UUID]
    class_num: int
    class_name: str
    edu_start: date
    edu_finish: date
    teacher: UUID
    students: List[UUID]
