import asyncio
from abc import ABC, abstractmethod
from typing import Type

from sapp.core.listener_mixins import StartupListenerMixin, ShutdownListenerMixin
from sapp.settings import Settings
from injector import Module, singleton, provider, Injector
from fastapi import Request


class BaseApplicationContainer(ABC, Module):

    @singleton
    @provider
    @abstractmethod
    def provide_settings(self) -> Settings:
        return Settings()


class ContainerManager:

    def __init__(self, cls_container: Type[BaseApplicationContainer]) -> None:
        self.container = Injector(cls_container())

    def get_container(self) -> Injector:
        return self.container

    async def run_startup(self) -> None:
        tasks = []

        binding_collection = []

        for binding in self.container.binder._bindings:
            binding_collection.append(binding)

        for binding in binding_collection:
            if issubclass(binding, StartupListenerMixin):
                startup_container_obj = self.container.get(binding)
                tasks.append(startup_container_obj.run_startup())

        await asyncio.gather(*tasks)

    async def run_shutdown(self) -> None:
        tasks = []

        for binding in self.container.binder._bindings:
            if issubclass(binding, ShutdownListenerMixin):
                startup_container_obj = self.container.get(binding)
                tasks.append(startup_container_obj.run_shutdown())

        await asyncio.gather(*tasks)


async def get_container_injector(request: Request) -> BaseApplicationContainer:
    return request.app.container
