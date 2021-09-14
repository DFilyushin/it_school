from fastapi import APIRouter
from uuid import UUID
from datetime import datetime

from sapp.models.teacher import TeacherModel
from sapp.repositories.teacher_repository import TeacherRepository
from sapp.serializers import TeacherSerializer


class TeacherController:

    def __init__(self, repository: TeacherRepository) -> None:
        self.router = APIRouter()
        self.repository = repository
        self._register_routes()

    def _register_routes(self):
        @self.router.get('/teachers', name='Get teachers')
        async def get_teachers():
            teachers = await self.repository.get_teachers()
            return teachers

        @self.router.get('/teacher/{id}', name='Get teacher by id')
        async def get_teacher(id: UUID):
            teacher = await self.repository.get_teacher(id)
            return teacher.dict()

        @self.router.post('/teacher/', name='Create new teacher')
        async def new_teacher(teacher: TeacherSerializer):
            teacher_dob = datetime.combine(teacher.dob, datetime.min.time())
            new_teacher = TeacherModel(
                first_name=teacher.first_name,
                last_name=teacher.last_name,
                patronymic=teacher.patronymic,
                dob=teacher_dob
            )
            await self.repository.new_teacher(new_teacher)

        @self.router.delete('/teacher/{id}', name='Delete teacher by id')
        async def delete_teacher(id: UUID):
            await self.repository.delete_teacher(id)