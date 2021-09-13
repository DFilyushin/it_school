from sapp.settings import Settings
from dataclasses import dataclass
from motor.motor_asyncio import AsyncIOMotorClient
from sapp.connectors.abstract_connector import ConnectionManager


@dataclass
class MongoDBConnectionManager(ConnectionManager):
    settings: Settings

    def __post_init__(self) -> None:
        self._mongodb_uri = self.settings.mongodb_dsn
        self._connection = None

    async def get_connection_async(self) -> AsyncIOMotorClient:
        if not self._connection:
            await self.run_startup()
        return self._connection

    async def run_startup(self) -> None:
        self._connection = AsyncIOMotorClient(self._mongodb_uri)

    async def run_shutdown(self) -> None:
        if self._connection:
            self._connection.close()
