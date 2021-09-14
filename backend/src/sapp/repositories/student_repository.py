from dataclasses import dataclass
from typing import Iterable, List, Optional
from pymongo import ASCENDING
from uuid import UUID, uuid4

from sapp.repositories.base_mongo_repository import BaseMongoRepository, IndexDef
from sapp.core.exceptions import DataNotFoundError
from sapp.models.student import StudentModel


class StudentRepository(BaseMongoRepository):
    @property
    def collection_name(self) -> str:
        return 'student'

    @property
    def collection_indexes(self) -> Iterable[IndexDef]:
        return (
            IndexDef(field_name='id', sort=ASCENDING),
        )

    async def new_student(self, student: StudentModel) -> StudentModel:
        student.id = uuid4()
        await self.add_data(student.dict())
        return student

    async def get_students(self, by_class: Optional[UUID]) -> Optional[List[StudentModel]]:
        result = []
        criteria = {}
        if by_class:
            criteria[''] = by_class
        students = await self.get_list_data({})
        for item in students:
            result.append(StudentModel(**item))
        return result

    async def get_student(self, id: UUID) -> StudentModel:
        model = await self.get_data({'id': id})
        if not model:
            raise DataNotFoundError(message=f'Student with id {id} not found')
        return StudentModel(**model)

    async def delete_student(self, id: UUID):
        await self.delete_data({'id': id})

    async def update_student(self, id: UUID, student: StudentModel):
        model = await self.get_data({'id': id})
        if not model:
            raise DataNotFoundError(message=f'Student with id {id} not found')
        await self.update_data({'id': id}, student.dict())
