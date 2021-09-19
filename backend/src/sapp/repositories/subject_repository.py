from dataclasses import dataclass
from typing import Iterable, List, Optional
from pymongo import ASCENDING
from uuid import UUID, uuid4

from sapp.repositories.base_mongo_repository import BaseMongoRepository, IndexDef
from sapp.core.exceptions import DataNotFoundError
from sapp.models import EducationSubjectModel


class SubjectRepository(BaseMongoRepository):
    @property
    def collection_name(self) -> str:
        return 'education_subject'

    @property
    def collection_indexes(self) -> Iterable[IndexDef]:
        return (
            IndexDef(field_name='id', sort=ASCENDING),
            IndexDef(field_name='name', sort=ASCENDING),
        )

    async def new_subject(self, subject: EducationSubjectModel) -> EducationSubjectModel:
        subject.id = uuid4()
        await self.add_data(subject.dict())
        return subject

    async def get_subjects(self) -> Optional[List[EducationSubjectModel]]:
        result = []
        criteria = {}
        subjects = await self.get_list_data(criteria_dict=criteria)
        for item in subjects:
            result.append(EducationSubjectModel(**item))
        return result

    async def get_subject(self, id: UUID) -> EducationSubjectModel:
        subject_model = await self.get_data({'id': id})
        if not subject_model:
            raise DataNotFoundError(message=f'Subject with id {id} not found')
        return EducationSubjectModel(**subject_model)

    async def delete_subject(self, id: UUID):
        await self.delete_data({'id': id})

    async def update_subject(self, id: UUID, student: EducationSubjectModel):
        model = await self.get_data({'id': id})
        if not model:
            raise DataNotFoundError(message=f'Teacher with id {id} not found')
        await self.update_data({'id': id}, student.dict())
