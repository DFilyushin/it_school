from typing import Iterable, List, Optional
from pymongo import ASCENDING
from uuid import UUID, uuid4

from sapp.repositories.base_mongo_repository import BaseMongoRepository, IndexDef
from sapp.core.exceptions import DataNotFoundError
from sapp.models import AchievementModel, EducationTopicModel, EducationPlanModel


class EducationPlanRepository(BaseMongoRepository):
    @property
    def collection_name(self) -> str:
        return 'education_plan'

    @property
    def collection_indexes(self) -> Iterable[IndexDef]:
        return (
            IndexDef(field_name='id', sort=ASCENDING),
            IndexDef(field_name='class_num', sort=ASCENDING),
            IndexDef(field_name='subject_id', sort=ASCENDING),
            IndexDef(field_name='teacher_id', sort=ASCENDING),
        )

    async def new_plan(self, plan: EducationPlanModel) -> EducationPlanModel:
        plan.id = uuid4()
        await self.add_data(plan.dict())
        return plan

    async def get_plans(
            self,
            class_num: Optional[int],
            subject_id: Optional[UUID],
            teacher_id: Optional[UUID]
    ) -> Optional[List[EducationPlanModel]]:
        result = []
        criteria = {}
        if class_num:
            criteria['class_num'] = class_num
        if subject_id:
            criteria['subject_id'] = subject_id
        if teacher_id:
            criteria['teacher_id'] = teacher_id
        plan_items = await self.get_list_data(criteria_dict=criteria)
        for item in plan_items:
            result.append(EducationPlanModel(**item))
        return result

    async def get_plan(self, id: UUID) -> EducationPlanModel:
        model = await self.get_data({'id': id})
        if not model:
            raise DataNotFoundError(message=f'Plan with id {id} not found')
        return EducationPlanModel(**model)

    async def get_plan_by_topic(self, id_topic: UUID) -> EducationPlanModel:
        criteria = {
            'topics.id': id_topic
        }
        model = await self.get_data(criteria_dict=criteria)
        if not model:
            raise DataNotFoundError(message=f'Plan not found')
        return EducationPlanModel(**model)

    async def delete_plan(self, id: UUID):
        await self.delete_data({'id': id})

    async def update_plan(self, id: UUID, plan: EducationPlanModel):
        model = await self.get_data({'id': id})
        if not model:
            raise DataNotFoundError(message=f'Plan with id {id} not found')
        await self.update_data({'id': id}, plan.dict())


class EducationTopicRepository(BaseMongoRepository):
    @property
    def collection_name(self) -> str:
        return 'education_topic'

    @property
    def collection_indexes(self) -> Iterable[IndexDef]:
        return (
            IndexDef(field_name='id', sort=ASCENDING),
        )

    async def new_topic(self, topic: EducationTopicModel) -> EducationTopicModel:
        topic.id = uuid4()
        await self.add_data(topic.dict())
        return topic

    async def get_topics(self) -> Optional[List[EducationTopicModel]]:
        result = []
        criteria = {}
        topics = await self.get_list_data(criteria_dict=criteria)
        for item in topics:
            result.append(EducationTopicModel(**item))
        return result

    async def get_topic(self, id: UUID) -> EducationTopicModel:
        model = await self.get_data({'id': id})
        if not model:
            raise DataNotFoundError(message=f'Teacher with id {id} not found')
        return EducationTopicModel(**model)

    async def delete_topic(self, id: UUID):
        await self.delete_data({'id': id})

    async def update_topic(self, id: UUID, topic: EducationTopicModel):
        model = await self.get_data({'id': id})
        if not model:
            raise DataNotFoundError(message=f'Teacher with id {id} not found')
        await self.update_data({'id': id}, topic.dict())


class AchievementRepository(BaseMongoRepository):
    @property
    def collection_name(self) -> str:
        return 'education_achievement'

    @property
    def collection_indexes(self) -> Iterable[IndexDef]:
        return (
            IndexDef(field_name='id', sort=ASCENDING),
        )

    async def new_achievement(self, achievement: AchievementModel) -> AchievementModel:
        achievement.id = uuid4()
        await self.add_data(achievement.dict())
        return achievement

    async def get_achievements(
            self,
            weight: Optional[int]
    ) -> Optional[List[AchievementModel]]:
        result = []
        criteria = {}
        if weight:
            criteria['weight'] = weight
        ach_items = await self.get_list_data(criteria_dict=criteria)
        for item in ach_items:
            result.append(AchievementModel(**item))
        return result

    async def get_achievement(self, id: UUID) -> AchievementModel:
        model = await self.get_data({'id': id})
        if not model:
            raise DataNotFoundError(message=f'Achievement with id {id} not found')
        return AchievementModel(**model)

    async def delete_achievement(self, id: UUID):

        await self.delete_data({'id': id})

    async def update_achievement(self, id: UUID, plan: AchievementModel):
        model = await self.get_data({'id': id})
        if not model:
            raise DataNotFoundError(message=f'Plan with id {id} not found')
        await self.update_data({'id': id}, plan.dict())
