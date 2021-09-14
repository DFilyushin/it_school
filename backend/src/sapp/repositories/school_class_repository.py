from dataclasses import dataclass
from typing import Iterable, List, Optional
from pymongo import ASCENDING
from uuid import UUID, uuid4

from sapp.repositories.base_mongo_repository import BaseMongoRepository, IndexDef
from sapp.core.exceptions import DataNotFoundError
from sapp.models.school_class import SchoolClass


class SchoolClassRepository(BaseMongoRepository):
    @property
    def collection_name(self) -> str:
        return 'school_class'

    @property
    def collection_indexes(self) -> Iterable[IndexDef]:
        return (
            IndexDef(field_name='id', sort=ASCENDING),
            IndexDef(field_name='edu_start', sort=ASCENDING),
            IndexDef(field_name='class_num', sort=ASCENDING)
        )

    async def new_school_class(self, school_class: SchoolClass) -> SchoolClass:
        school_class.id = uuid4()
        await self.add_data(school_class.dict())
        return school_class

    async def delete_school_class(self, id: UUID):
        await self.delete_data({'id': id})

    async def get_school_class(self, id: UUID) -> SchoolClass:
        model = await self.get_data({'id': id})
        return SchoolClass(**model)

    async def get_school_classes(self, by_year: int) -> List[SchoolClass]:
        result = []
        criteria = {'class_num': by_year}
        models = await self.get_list_data(criteria_dict=criteria)
        for item in models:
            result.append(SchoolClass(**item))
        return result

    async def update_school_class(self, id: UUID, school_class: SchoolClass):
        model = await self.get_data({'id': id})
        if not model:
            raise DataNotFoundError(f'School class {id} not found!')
        await self.update_data({'id': id}, school_class.dict())
