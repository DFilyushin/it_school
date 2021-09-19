from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID, uuid4


class TopicAssessmentModel(BaseModel):
    """Оценки ученика за уроки по теме"""
    id: UUID = Field(default_factory=uuid4)
    teacher_id: UUID
    topic_id: UUID
    created: datetime
    value: int


class StudentAchieveModel(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    teacher_id: UUID
    plan_id: UUID
    achievement_id: UUID
    created: datetime


class StudentModel(BaseModel):
    id: Optional[UUID]
    first_name: str
    last_name: str
    patronymic: str
    dob: datetime
    achievements: List[StudentAchieveModel] = []
    assessments: List[TopicAssessmentModel] = []
