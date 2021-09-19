from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID, uuid4


class TopicAssessment(BaseModel):
    """Оценки ученика за уроки по теме"""
    topic_id: UUID
    student_id: UUID
    created: datetime
    value: int


class QuizProcess(BaseModel):
    """Ответы ученика в тесте"""
    question_id: UUID
    answer: UUID
    result: bool


class QuizStudent(BaseModel):
    """Тест студента"""
    quiz_id: UUID
    student_id: UUID
    quiz_start: datetime
    quiz_finish: datetime
    test_kind: int
    assessment: int
    results: List[QuizProcess]


class AchievementModel(BaseModel):
    """Достижения"""
    id: Optional[UUID] = Field(default_factory=uuid4)
    name: str
    weight: int


class StudentAchieveModel(BaseModel):
    """Достижения студентов"""
    student_id: UUID
    teacher_id: UUID
    plan_id: UUID
    achievement_id: UUID
    created: datetime
