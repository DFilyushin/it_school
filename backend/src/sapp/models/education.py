from typing import List
from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID, uuid4


class EducationTopicModel(BaseModel):
    """Темы уроков"""
    id: UUID = Field(default_factory=uuid4)
    name: str
    edu_quarter: int
    edu_hours: int
    goal: str


class EducationSubjectModel(BaseModel):
    """Предмет"""
    id: UUID = Field(default_factory=uuid4)
    name: str


class EducationPlanModel(BaseModel):
    """План"""
    id: UUID = Field(default_factory=uuid4)
    created: datetime
    class_num: int
    subject_id: UUID
    teacher_id: UUID
    topics: List[EducationTopicModel]


class EducationMaterial(BaseModel):
    """Материал по темам"""
    id: UUID
    topic_id: UUID
    sort: int
    body: str


class QuizModel(BaseModel):
    """Тесты"""
    id: UUID
    created: datetime
    plan_id: UUID
    teacher_id: UUID


class QuizAnswerModel(BaseModel):
    """Ответы"""
    answer: str
    is_right: bool


class QuizQuestionModel(BaseModel):
    """Вопросы к тестированию"""
    quiz_id: UUID
    question: str
    weight: int
    answers: List[QuizAnswerModel]
