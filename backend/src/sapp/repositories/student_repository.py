from dataclasses import dataclass
from datetime import datetime
from typing import Iterable, List, Optional
from pymongo import ASCENDING
from uuid import UUID, uuid4

from sapp.repositories.base_mongo_repository import BaseMongoRepository, IndexDef
from sapp.core.exceptions import DataNotFoundError
from sapp.models.student import StudentModel, StudentAchieveModel, TopicAssessmentModel


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

    async def get_students(self, by_class: Optional[UUID] = None) -> Optional[List[StudentModel]]:
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

    async def get_achievements(self, student_id: UUID) -> List[StudentAchieveModel]:
        result = []
        student = await self.get_student(student_id)
        for item in student.achievements:
            result.append(
                StudentAchieveModel(
                    id=item.id,
                    teacher_id=item.teacher_id,
                    plan_id=item.plan_id,
                    achievement_id=item.achievement_id,
                    created=item.created
                )
            )
            return result

    async def new_achievement(self, student_id: UUID, teacher_id: UUID, achieve_id: UUID, plan_id: UUID):
        new_object = StudentAchieveModel(
            teacher_id=teacher_id,
            plan_id=plan_id,
            achievement_id=achieve_id,
            created=datetime.utcnow()
        )
        await self.add_item_to_array({'id': student_id}, 'achievements', new_object.dict())

    async def delete_achievement(self, student_id: UUID, id: UUID):
        await self.remove_item_from_array({'id': student_id}, 'achievements', {'id': id})

    async def get_assessments(self, student_id: UUID, year: Optional[int], topic: Optional[UUID]) -> List[TopicAssessmentModel]:
        result = []
        student = await self.get_student(student_id)
        for item in student.assessments:
            if topic:
                if item.topic_id != topic:
                    continue
            result.append(
                TopicAssessmentModel(
                    id=item.id,
                    topic_id=item.topic_id,
                    created=item.created,
                    value=item.value)
            )
            return result

    async def new_assessment(self, student_id: UUID, teacher_id: UUID, topic_id: UUID, value: int):
        new_object = TopicAssessmentModel(
            topic_id=topic_id,
            teacher_id=teacher_id,
            created=datetime.utcnow(),
            value=value
        )
        await self.add_item_to_array({'id': student_id}, 'assessments', new_object.dict())

    async def delete_assessment(self, student_id: UUID, id: UUID):
        await self.remove_item_from_array({'id': student_id}, 'assessments', {'id': id})
