from typing import Iterable, List, Optional
from pymongo import ASCENDING
from pymongo.errors import DuplicateKeyError
from uuid import UUID

from sapp.core.listener_mixins import StartupListenerMixin
from sapp.repositories.base_mongo_repository import BaseMongoRepository, IndexDef
from sapp.core.exceptions import DataNotFoundError
from sapp.models import GroupModel, Groups


class GroupRepository(BaseMongoRepository, StartupListenerMixin):

    @property
    def collection_name(self) -> str:
        return 'group'

    @property
    def collection_indexes(self) -> Iterable[IndexDef]:
        return (
            IndexDef(field_name='name', sort=ASCENDING, unique=True),
        )

    async def run_startup(self) -> None:
        await super().run_startup()
        await self.create_default_groups()

    async def create_default_groups(self) -> None:
        for key in Groups.list():
            try:
                await self.add_data(GroupModel(name=key).dict())
            except DuplicateKeyError:
                pass

    async def get_groups(self) -> Optional[List[GroupModel]]:
        result = []
        criteria = {}
        users = await self.get_list_data(criteria_dict=criteria)
        for item in users:
            result.append(GroupModel(**item))
        return result

    async def get_group(self, id: UUID) -> GroupModel:
        model = await self.get_data({'id': id})
        if not model:
            raise DataNotFoundError(message=f'Group {id} not found')
        return GroupModel(**model)
