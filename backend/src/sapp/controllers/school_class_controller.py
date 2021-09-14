from fastapi import APIRouter, Header
from uuid import UUID
from datetime import datetime

from sapp.models.student import StudentModel
from sapp.repositories.school_class_repository import SchoolClassRepository
from sapp.serializers.student import StudentSerializer


class SchoolClassController:

    def __init__(self, repository: SchoolClassRepository) -> None:
        self.router = APIRouter()
        self.repository = repository
        self._register_routes()

    def _register_routes(self):
        @self.router.get('/classes', name='Get classes')
        async def get_school_classes(class_num: int):
            school_classes = await self.repository.get_school_classes(class_num)
            return school_classes

        @self.router.get('/class/{id}', name='Get school class by id')
        async def get_school_class(id: UUID):
            model = await self.repository.get_school_class(id)
            return model.dict()

        @self.router.post('/class/', name='Create new class')
        async def new_school_class(student: StudentSerializer):
            student_dob = datetime.combine(student.dob, datetime.min.time())
            new_student = StudentModel(
                first_name=student.first_name,
                last_name=student.last_name,
                patronymic=student.middle_name,
                dob=student_dob
            )
            await self.repository.new_student(new_student)

        @self.router.delete('/class/{id}', name='Delete school class by id')
        async def delete_school_class(id: UUID):
            await self.repository.delete_school_class(id)
