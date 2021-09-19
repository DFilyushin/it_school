from typing import Iterable, List, Optional
from pymongo import ASCENDING
from uuid import UUID, uuid4

from sapp.repositories.base_mongo_repository import BaseMongoRepository, IndexDef
from sapp.core.exceptions import DataNotFoundError
from sapp.models import QuizModel, QuizQuestionModel, QuizAnswerModel


class QuizRepository(BaseMongoRepository):
    @property
    def collection_name(self) -> str:
        return 'quiz_table'

    @property
    def collection_indexes(self) -> Iterable[IndexDef]:
        return (
            IndexDef(field_name='id', sort=ASCENDING),
        )

    async def new_quiz(self, quiz: QuizModel) -> QuizModel:
        quiz.id = uuid4()
        await self.add_data(quiz.dict())
        return quiz

    async def get_quizzes(self, class_num: int) -> Optional[List[QuizModel]]:
        result = []
        criteria = {}
        quizzes = await self.get_list_data(criteria_dict=criteria)
        for item in quizzes:
            result.append(QuizModel(**item))
        return result

    async def get_quiz(self, id: UUID) -> QuizModel:
        model = await self.get_data({'id': id})
        if not model:
            raise DataNotFoundError(message=f'Teacher with id {id} not found')
        return QuizModel(**model)

    async def delete_quiz(self, id: UUID):
        await self.delete_data({'id': id})

    async def update_quiz(self, id: UUID, quiz: QuizModel):
        model = await self.get_data({'id': id})
        if not model:
            raise DataNotFoundError(message=f'Teacher with id {id} not found')
        await self.update_data({'id': id}, quiz.dict())


class QuizQuestionRepository(BaseMongoRepository):

    @property
    def collection_name(self) -> str:
        return 'quiz_question'

    @property
    def collection_indexes(self) -> Iterable[IndexDef]:
        return (
            IndexDef(field_name='id', sort=ASCENDING),
            IndexDef(field_name='quiz_id', sort=ASCENDING),
        )

    async def new_question(self, qq: QuizQuestionModel) -> QuizQuestionModel:
        qq.id = uuid4()
        await self.add_data(qq.dict())
        return qq

    async def get_questions(self, quiz_id: int) -> Optional[List[QuizQuestionModel]]:
        result = []
        criteria = {'quiz_id': quiz_id}
        questions = await self.get_list_data(criteria_dict=criteria)
        for item in questions:
            result.append(QuizQuestionModel(**item))
        return result

    async def get_question(self, id: UUID) -> QuizQuestionModel:
        model = await self.get_data({'id': id})
        if not model:
            raise DataNotFoundError(message=f'Question with id {id} not found')
        return QuizQuestionModel(**model)

    async def delete_question(self, id: UUID):
        await self.delete_data({'id': id})

    async def update_quiz(self, id: UUID, question: QuizQuestionModel):
        model = await self.get_data({'id': id})
        if not model:
            raise DataNotFoundError(message=f'Question with id {id} not found')
        await self.update_data({'id': id}, question.dict())
