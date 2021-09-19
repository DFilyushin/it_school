from datetime import datetime
from pydantic import BaseModel
from uuid import UUID


class StudentAchieveSerializer(BaseModel):
    id: UUID
    teacher: str
    subject: str
    achievement: str
    created: datetime


class StudentNewAchieveSerializer(BaseModel):
    teacher_id: UUID
    plan_id: UUID
    achievement_id: UUID


class StudentNewAssessmentSerializer(BaseModel):
    teacher_id: UUID
    topic_id: UUID
    value: int


class StudentAssessmentSerializer(BaseModel):
    id: UUID
    teacher: str
    topic: str
    created: datetime
    value: int
