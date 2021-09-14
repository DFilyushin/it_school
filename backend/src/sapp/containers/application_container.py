from logging import Logger
from injector import singleton, provider

from sapp.connectors.mongo_connector import MongoDBConnector
from sapp.core.container import BaseApplicationContainer
from sapp.settings import Settings
from sapp.controllers import StudentController, SchoolClassController, TeacherController
from sapp.repositories import StudentRepository, SchoolClassRepository, TeacherRepository


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
    def provide_mongodb_connection_manager(self, settings: Settings) -> MongoDBConnector:
        return MongoDBConnector(settings)

    @singleton
    @provider
    def provide_student_controller(self, repository: StudentRepository) -> StudentController:
        return StudentController(repository)

    @singleton
    @provider
    def provide_student_repository(self, connector: MongoDBConnector, settings: Settings) -> StudentRepository:
        return StudentRepository(connector, settings)

    @singleton
    @provider
    def provide_teacher_controller(self, repository: TeacherRepository) -> TeacherController:
        return TeacherController(repository)

    @singleton
    @provider
    def provide_teacher_repository(self, connector: MongoDBConnector, settings: Settings) -> TeacherRepository:
        return TeacherRepository(connector, settings)

    @singleton
    @provider
    def provide_school_class_controller(self, repository: SchoolClassRepository) -> SchoolClassController:
        return SchoolClassController(repository)

    @singleton
    @provider
    def provide_school_class_repository(self, connector: MongoDBConnector, settings: Settings) -> SchoolClassRepository:
        return SchoolClassRepository(connector, settings)
