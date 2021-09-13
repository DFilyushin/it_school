from typing import List
from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID


class EducationTopic(BaseModel):
    """Темы уроков"""
    name: str
    edu_quarter: int
    edu_hours: int
    goal: str
    material: List[UUID]


class EducationSubject(BaseModel):
    """Предмет"""
    code: UUID
    name: str


class EducationPlan(BaseModel):
    class_num: int
    subject_id: UUID
    teacher_id: UUID
    topics: List[EducationTopic]


class EducationMaterial(BaseModel):
    """"""
    code: UUID
    sort: int
    body: str


class QuizModel(BaseModel):
    """Тесты"""
    code: UUID
    plan_id: UUID
    teacher_id: UUID


class AnswerModel(BaseModel):
    """Ответы"""
    answer: str
    is_right: bool


class QuizQuestionModel(BaseModel):
    """Вопросы к тестированию"""
    quiz_id: UUID
    question: str
    weight: int
    answers: List[AnswerModel]
