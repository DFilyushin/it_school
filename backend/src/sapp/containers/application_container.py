from logging import Logger
from injector import singleton, provider

from sapp.connectors.mongo_connector import MongoDBConnectionManager
from sapp.core.container import BaseApplicationContainer
from sapp.settings import Settings


class ApplicationContainer(BaseApplicationContainer):

    @singleton
    @provider
    def provide_settings(self) -> Settings:
        return Settings()

    @singleton
    @provider
    def provide_logger(self, setting: Settings) -> Logger:
        return Logger(name=setting.title_application, level=setting.debug_level)

    @singleton
    @provider
    def provide_mongodb_connection_manager(self, settings: Settings) -> MongoDBConnectionManager:
        return MongoDBConnectionManager(settings)
