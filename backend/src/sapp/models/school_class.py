from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID, uuid4


class SchoolClass(BaseModel):
    id: Optional[UUID] = Field(default_factory=uuid4)
    class_num: int
    class_name: str
    edu_start: datetime
    edu_finish: datetime
    teacher: UUID
    students: List[UUID]
