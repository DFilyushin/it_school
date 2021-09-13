from abc import ABC
from typing import Any


class ConnectionManager(ABC):

    async def get_connection_async(self) -> Any: ...

    async def run_startup(self) -> Any: ...

    async def run_shutdown(self) -> Any: ...
