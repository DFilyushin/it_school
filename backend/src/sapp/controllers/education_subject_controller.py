from fastapi import APIRouter
from uuid import UUID

from sapp.models import EducationSubjectModel
from sapp.repositories import SubjectRepository
from sapp.serializers import EducationSubjectSerializer


class EducationSubjectController:

    def __init__(self, repository: SubjectRepository) -> None:
        self.router = APIRouter()
        self.repository = repository
        self._register_routes()

    def _register_routes(self):
        @self.router.get('/subjects', name='Get subjects')
        async def get_subjects():
            subjects = await self.repository.get_subjects()
            return subjects

        @self.router.get('/subject/{id}', name='Get subject by id')
        async def get_subject(id: UUID):
            teacher = await self.repository.get_subject(id)
            return teacher.dict()

        @self.router.post('/subject/', name='Create new subject')
        async def new_subject(subject: EducationSubjectSerializer):
            new_subject_object = EducationSubjectModel(name=subject.name)
            await self.repository.new_subject(new_subject_object)
            return subject

        @self.router.delete('/subject/{id}', name='Delete subject by id')
        async def delete_subject(id: UUID):
            await self.repository.delete_subject(id)
