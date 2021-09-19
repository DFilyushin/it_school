from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID, uuid4


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
