from fastapi import APIRouter
from uuid import UUID
from datetime import datetime

from sapp.models import UserModel
from sapp.repositories import UserRepository, GroupRepository
from sapp.serializers import UserSerializer
from hashlib import sha256


class UserController:

    def __init__(self, users: UserRepository, groups: GroupRepository) -> None:
        self.router = APIRouter()
        self.user_repository = users
        self.group_repository = groups
        self._register_routes()

    def _register_routes(self):
        @self.router.get('/groups', name='Get groups')
        async def get_groups():
            groups = await self.group_repository.get_groups()
            return groups

        @self.router.get('/users', name='Get users')
        async def get_users():
            teachers = await self.user_repository.get_users()
            return teachers

        @self.router.get('/user/{login}', name='Get user by login')
        async def get_user(login: str):
            user = await self.user_repository.get_user(login)
            return user.dict()

        @self.router.post('/user/', name='Create new user')
        async def new_user(user: UserSerializer):
            if user.password:
                pass_hash = sha256(user.password).digest()
            else:
                pass_hash = None
            new_user_object = UserModel(
                login=user.login,
                created=datetime.utcnow(),
                full_name=user.full_name,
                email=user.email,
                phone=user.phone,
                password=pass_hash,
                groups=user.groups)
            await self.user_repository.new_user(new_user_object)

        @self.router.delete('/user/{login}', name='Delete user by login')
        async def delete_teacher(login: str):
            await self.user_repository.delete_user(login)
