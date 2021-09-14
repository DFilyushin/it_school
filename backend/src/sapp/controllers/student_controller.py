from fastapi import APIRouter, Header
from uuid import UUID
from datetime import datetime

from sapp.models.student import StudentModel
from sapp.repositories.student_repository import StudentRepository
from sapp.serializers.student import StudentSerializer


class StudentController:

    def __init__(self, repository: StudentRepository) -> None:
        self.router = APIRouter()
        self.repository = repository
        self._register_routes()

    def _register_routes(self):
        @self.router.get('/students', name='Get students')
        async def get_students():
            students = await self.repository.get_students()
            return students

        @self.router.get('/student/{id}', name='Get student by id')
        async def get_student(id: UUID):
            model = await self.repository.get_student(id)
            return model.dict()

        @self.router.post('/student/', name='Create new student')
        async def new_student(student: StudentSerializer):
            student_dob = datetime.combine(student.dob, datetime.min.time())
            new_student = StudentModel(
                first_name=student.first_name,
                last_name=student.last_name,
                patronymic=student.middle_name,
                dob=student_dob
            )
            await self.repository.new_student(new_student)

        @self.router.delete('/student/{id}', name='Delete student by id')
        async def delete_student(id: UUID):
            await self.repository.delete_student(id)
