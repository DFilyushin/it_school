from typing import List
from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID


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
