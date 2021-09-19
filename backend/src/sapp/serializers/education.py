from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field
from uuid import UUID


class EducationSubjectSerializer(BaseModel):
    id: Optional[UUID]
    name: str


class QuizAnswerSerializer(BaseModel):
    answer: str
    is_right: bool


class QuizQuestionSerializer(BaseModel):
    quiz_id: UUID
    question: str
    weight: int
    answers: List[QuizAnswerSerializer]


class QuizSerializer(BaseModel):
    id: UUID
    plan_id: UUID
    teacher_id: UUID


class EducationTopicSerializer(BaseModel):
    id: Optional[UUID]
    name: str
    edu_quarter: int
    edu_hours: int
    goal: str


class EducationPlanSerializer(BaseModel):
    id: Optional[UUID]
    created: Optional[datetime]
    class_num: int
    subject_id: UUID
    teacher_id: UUID
    topics: List[EducationTopicSerializer]


class AchievementSerializer(BaseModel):
    """Достижения"""
    id: Optional[UUID]
    name: str
    weight: int
