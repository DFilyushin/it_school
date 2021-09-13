from os.path import isfile
from pathlib import Path
from typing import Optional
from pydantic import BaseSettings
from logging import DEBUG

base_dir = Path(__file__).parent.parent.parent.absolute()


class Settings(BaseSettings):
    title_application: str = 'SchoolApp'
    debug_level: int = DEBUG

    mongodb_hosts: str
    mongodb_username: str
    mongodb_password: str
    mongodb_database: str
    mongodb_replica_set_name: Optional[str] = None
    mongodb_auth_db: str

    @property
    def mongodb_dsn(self) -> str:
        mongodb_dsn = 'mongodb://{}:{}@{}/{}'.format(
            self.mongodb_username,
            self.mongodb_password,
            self.mongodb_hosts,
            self.mongodb_auth_db
        )

        if self.mongodb_replica_set_name:
            mongodb_dsn += f'?replicaSet={self.mongodb_replica_set_name}'

        return mongodb_dsn

    class Config:
        config_file_name = f'{base_dir}/.env'
        if isfile(config_file_name):
            env_file = config_file_name
