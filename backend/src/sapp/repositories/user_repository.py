from typing import Iterable, List, Optional
from pymongo import ASCENDING
from uuid import UUID, uuid4

from sapp.repositories.base_mongo_repository import BaseMongoRepository, IndexDef
from sapp.core.exceptions import DataNotFoundError
from sapp.models import UserModel


class UserRepository(BaseMongoRepository):
    @property
    def collection_name(self) -> str:
        return 'user'

    @property
    def collection_indexes(self) -> Iterable[IndexDef]:
        return (
            IndexDef(field_name='login', sort=ASCENDING),
        )

    async def new_user(self, user: UserModel) -> UserModel:
        await self.add_data(user.dict())
        return user

    async def get_users(self) -> Optional[List[UserModel]]:
        result = []
        criteria = {}
        users = await self.get_list_data(criteria_dict=criteria)
        for item in users:
            result.append(UserModel(**item))
        return result

    async def get_user(self, login: str) -> UserModel:
        model = await self.get_data({'id': id})
        if not model:
            raise DataNotFoundError(message=f'User {login} not found')
        return UserModel(**model)

    async def delete_user(self, login: str):
        await self.delete_data({'login': login})

    async def update_user(self, login: str, user: UserModel):
        model = await self.get_data({'login': login})
        if not model:
            raise DataNotFoundError(message=f'User with id {id} not found')
        await self.update_data({'login': login}, user.dict())
