from fastapi import APIRouter
from uuid import UUID
from datetime import datetime
from typing import List, Optional
from pydantic import Field

from sapp.models import EducationPlanModel, EducationTopicModel, AchievementModel
from sapp.repositories import EducationPlanRepository, EducationTopicRepository, AchievementRepository
from sapp.serializers import EducationPlanSerializer, EducationTopicSerializer, AchievementSerializer


class EducationController:

    def __init__(self, topic_repository: EducationTopicRepository, plan_repository: EducationPlanRepository,
                 achievement_repository: AchievementRepository) -> None:
        self.router = APIRouter()
        self.topic_repository = topic_repository
        self.plan_repository = plan_repository
        self.achievement_repository = achievement_repository
        self._register_routes()

    def _register_routes(self):
        # Topics
        @self.router.get('/education/topics', name='Get topics')
        async def get_topics() -> List[EducationTopicModel]:
            pass

        @self.router.get('/education/topic/{topic_id}', name='Get topic by id')
        async def get_topic(topic_id: UUID) -> EducationTopicModel:
            pass

        @self.router.post('/education/topic', name='New topic')
        async def new_topic(topic: EducationTopicSerializer) -> EducationTopicSerializer:
            new_topic_object = EducationTopicModel(
                name=topic.name,
                edu_quarter=topic.edu_quarter,
                edu_hours=topic.edu_hours,
                goal=topic.goal
            )
            await self.topic_repository.new_topic(new_topic_object)
            topic.id = new_topic_object.id
            return topic

        @self.router.delete('/education/topic/{topic_id}', name='Delete topic')
        async def delete_topic(topic_id: UUID):
            pass

        @self.router.put('/education/topic/{topic_id}', name='Update topic')
        async def update_topic(topic_id: UUID, topic: EducationTopicModel):
            pass

        # Plans
        @self.router.get('/education/plans', name='Get education plans')
        async def get_plans(class_num: int, subject_id: UUID, teacher_id: UUID) -> List[EducationPlanModel]:
            plans = await self.plan_repository.get_plans(class_num, subject_id, teacher_id)
            return plans

        @self.router.get('/education/plan/{plan_id}', name='Get plan by id')
        async def get_plan(plan_id: UUID) -> EducationPlanModel:
            plan = await self.plan_repository.get_plan(plan_id)
            return plan

        @self.router.post('/education/plan', name='New plan')
        async def new_plan(plan: EducationPlanSerializer) -> EducationPlanSerializer:
            new_plan_object = EducationPlanModel(
                created=datetime.utcnow(),
                class_num=plan.class_num,
                subject_id=plan.subject_id,
                teacher_id=plan.teacher_id,
                topics=plan.topics
            )
            await self.plan_repository.new_plan(new_plan_object)
            plan.id = new_plan_object.id
            return plan

        @self.router.delete('/education/plan/{plan_id}', name='Delete plan')
        async def delete_plan(plan_id: UUID):
            await self.plan_repository.delete_plan(plan_id)

        @self.router.put('/education/plan/{plan_id}', name='Update plan')
        async def update_topic(plan_id: UUID, plan: EducationPlanModel):
            await self.plan_repository.update_plan(plan_id, plan)

        # Achievement
        @self.router.get('/education/achievements', name='Get achievements')
        async def get_achievements(weight: Optional[int] = None) -> List[AchievementSerializer]:
            result = []
            items = await self.achievement_repository.get_achievements(weight)
            for item in items:
                result.append(AchievementSerializer(
                    id=item.id,
                    name=item.name,
                    weight=item.weight
                ))
            return result

        @self.router.get('/education/achievements/{id}', name='Get achievement by id')
        async def get_achievement(id: UUID) -> AchievementSerializer:
            achievement = await self.achievement_repository.get_achievement(id)
            return AchievementSerializer(**achievement.dict())

        @self.router.post('/education/achievement', name='New achievement')
        async def new_achievement(achievement: AchievementSerializer) -> AchievementSerializer:
            new_achi_object = AchievementModel(
                name=achievement.name,
                weight=achievement.weight
            )
            await self.achievement_repository.new_achievement(new_achi_object)
            achievement.id = new_achi_object.id
            return achievement

        @self.router.delete('/education/achievement/{id}', name='Delete achievement')
        async def delete_achievement(id: UUID):
            await self.achievement_repository.delete_achievement(id)

        @self.router.put('/education/achievement/{id}', name='Update achievement')
        async def update_achievement(id: UUID, achievement: AchievementSerializer):
            achievement_dict = achievement.dict()
            del(achievement_dict['id'])
            new_achievement = AchievementModel(id=id, **achievement_dict)
            await self.achievement_repository.update_achievement(id, new_achievement)
