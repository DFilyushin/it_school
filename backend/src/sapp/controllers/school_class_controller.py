from fastapi import APIRouter
from uuid import UUID
from datetime import datetime

from sapp.models import SchoolClass
from sapp.repositories.school_class_repository import SchoolClassRepository
from sapp.serializers import SchoolClassSerializer


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
        async def new_school_class(school_class: SchoolClassSerializer):
            new_class_object = SchoolClass(
                class_num=school_class.class_num,
                class_name=school_class.class_name,
                edu_start=datetime.combine(school_class.edu_start, datetime.min.time()),
                edu_finish=datetime.combine(school_class.edu_finish, datetime.min.time()),
                teacher=school_class.teacher,
                students=school_class.students)
            await self.repository.new_school_class(new_class_object)

        @self.router.delete('/class/{id}', name='Delete school class by id')
        async def delete_school_class(id: UUID):
            await self.repository.delete_school_class(id)
