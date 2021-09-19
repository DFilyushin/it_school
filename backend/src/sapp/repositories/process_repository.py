from typing import Iterable, List, Optional
from datetime import datetime
from pymongo import ASCENDING
from uuid import UUID, uuid4

from sapp.repositories.base_mongo_repository import BaseMongoRepository, IndexDef
from sapp.core.exceptions import DataNotFoundError
from sapp.models import QuizModel, QuizQuestionModel, QuizAnswerModel


class ProcessAchievementRepository(BaseMongoRepository):
    @property
    def collection_name(self) -> str:
        return 'process_achievement'

    @property
    def collection_indexes(self) -> Iterable[IndexDef]:
        return (
            IndexDef(field_name='id', sort=ASCENDING),
        )
