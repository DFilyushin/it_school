from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


class SchoolClass(BaseModel):
    id: Optional[UUID]
    class_num: int
    class_name: str
    edu_start: datetime
    edu_finish: datetime
    teacher: UUID
    students: List[UUID]
