from typing import Iterable, List, Optional
from pymongo import ASCENDING
from uuid import UUID, uuid4

from sapp.repositories.base_mongo_repository import BaseMongoRepository, IndexDef
from sapp.core.exceptions import DataNotFoundError
from sapp.models import TeacherModel


class TeacherRepository(BaseMongoRepository):
    @property
    def collection_name(self) -> str:
        return 'teacher'

    @property
    def collection_indexes(self) -> Iterable[IndexDef]:
        return (
            IndexDef(field_name='id', sort=ASCENDING),
        )

    async def new_teacher(self, student: TeacherModel) -> TeacherModel:
        student.id = uuid4()
        await self.add_data(student.dict())
        return student

    async def get_teachers(self) -> Optional[List[TeacherModel]]:
        result = []
        criteria = {}
        teachers = await self.get_list_data(criteria_dict=criteria)
        for item in teachers:
            result.append(TeacherModel(**item))
        return result

    async def get_teacher(self, id: UUID) -> TeacherModel:
        model = await self.get_data({'id': id})
        if not model:
            raise DataNotFoundError(message=f'Teacher with id {id} not found')
        return TeacherModel(**model)

    async def delete_teacher(self, id: UUID):
        await self.delete_data({'id': id})

    async def update_student(self, id: UUID, student: TeacherModel):
        model = await self.get_data({'id': id})
        if not model:
            raise DataNotFoundError(message=f'Teacher with id {id} not found')
        await self.update_data({'id': id}, student.dict())
