from typing import Iterable, List, Optional
from pymongo import ASCENDING
from uuid import UUID, uuid4

from sapp.repositories.base_mongo_repository import BaseMongoRepository, IndexDef
from sapp.core.exceptions import DataNotFoundError
from sapp.models import QuizModel, QuizQuestionModel, QuizAnswerModel


class ProcessRepository(BaseMongoRepository):
    pass
