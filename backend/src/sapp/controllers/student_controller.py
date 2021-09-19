from typing import Optional
from fastapi import APIRouter
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
            new_student_object = StudentModel(
                first_name=student.first_name,
                last_name=student.last_name,
                patronymic=student.middle_name,
                dob=student_dob
            )
            await self.repository.new_student(new_student_object)

        @self.router.delete('/student/{id}', name='Delete student by id')
        async def delete_student(id: UUID):
            await self.repository.delete_student(id)

        @self.router.get('/student/{id_student}/achievements', name='Get students achievements')
        async def get_student_achieves(id_student: UUID):
            pass

        @self.router.post('/student/{id_student}/achievements/{id_achievement}', name='New students achievement')
        async def new_student_achievement(id_student: UUID, id_achievement: UUID):
            pass

        @self.router.get('/student/{id_student}/assessments', name='Get students assessments')
        async def get_student_assessments(id_student: UUID, year: Optional[int], subject: Optional[UUID]):
            pass

        @self.router.post('/student/{id_student}/assessments/{new_value}', name='Set student assessment')
        async def set_student_assessment(id_student: UUID, new_value: int):
            pass

        @self.router.delete('/student/{id_student}/assessments/{assessment_id}', name='Delete student assessment')
        async def set_student_assessment(id_student: UUID, assessment_id: UUID):
            pass

        @self.router.put('/student/{id_student}/assessments/{assessment_id}/{new_value}', name='Update student assessment')
        async def set_student_assessment(id_student: UUID, assessment_id: UUID, new_value: int):
            pass

        @self.router.post('/student/{id_student}/quiz/{quiz_id}', name='Set student quiz')
        async def set_student_quiz(id_student: UUID, quiz_id: UUID):
            pass

        @self.router.delete('/student/{id_student}/quiz/{quiz_id}', name='Delete student quiz')
        async def delete_student_quiz(id_student: UUID, quiz_id: UUID):
            pass
