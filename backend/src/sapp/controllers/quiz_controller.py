import uuid

from fastapi import APIRouter
from uuid import UUID
from datetime import datetime

from sapp.models import QuizModel, QuizQuestionModel, QuizAnswerModel
from sapp.repositories import QuizRepository, QuizQuestionRepository
from sapp.serializers import QuizSerializer, QuizAnswerSerializer, QuizQuestionSerializer


class QuizController:

    def __init__(self, quiz: QuizRepository, question: QuizQuestionRepository) -> None:
        self.router = APIRouter()
        self.quiz_repository = quiz
        self.question_repository = question
        self._register_routes()

    def _register_routes(self):
        @self.router.get('/quizzes', name='Get quizzes')
        async def get_quizzes(class_num: int):
            quizzes = await self.quiz_repository.get_quizzes(class_num)
            return quizzes

        @self.router.get('/quiz/{id}', name='Get quiz by id')
        async def get_quiz(id: UUID):
            quiz = await self.quiz_repository.get_quiz(id)
            return quiz.dict()

        @self.router.post('/quiz/', name='Create new quiz')
        async def new_quiz(quiz: QuizSerializer):
            new_quiz_object = QuizModel(
                id=uuid.uuid4(),
                created=datetime.utcnow(),
                plan_id=quiz.plan_id,
                teacher_id=quiz.teacher_id
            )
            await self.quiz_repository.new_quiz(new_quiz_object)

        @self.router.delete('/quiz/{id}', name='Delete quiz by id')
        async def delete_quiz(id: UUID):
            await self.quiz_repository.delete_quiz(id)

        @self.router.put('/quiz/{id}', name='Update quiz by id')
        async def delete_quiz(id: UUID, quiz: QuizSerializer):
            new_quiz_object = QuizModel(
                id=quiz.id,
                plan_id=quiz.plan_id,
                teacher_id=quiz.teacher_id
            )
            await self.quiz_repository.update_quiz(id, new_quiz_object)

        @self.router.get('/questions', name='Get questions')
        async def get_quizzes(quiz_id: int):
            questions = await self.question_repository.get_questions(quiz_id)
            return questions

        @self.router.get('/question/{id}', name='Get question by id')
        async def get_quiz(id: UUID):
            question = await self.question_repository.get_question(id)
            return question.dict()

        @self.router.put('/question/{id}', name='Update question by id')
        async def update_question(id: UUID, question: QuizQuestionSerializer) -> QuizQuestionModel:
            new_question = QuizQuestionModel(
                quiz_id=question.quiz_id,
                question=question.question,
                weight=question.weight,
                answers=question.answers
            )
            await self.question_repository.update_quiz(id, new_question)
            return new_question.dict()

        @self.router.post('/question/', name='Add new question by id')
        async def add_question(question: QuizQuestionSerializer):
            new_question = QuizQuestionModel(
                quiz_id=uuid.uuid4(),
                question=question.question,
                weight=question.weight,
                answers=question.answers
            )
            await self.question_repository.add_data(new_question.dict())

        @self.router.delete('/question/{id}', name='Delete question by id')
        async def delete_question(id: UUID):
            await self.question_repository.delete_question(id)
