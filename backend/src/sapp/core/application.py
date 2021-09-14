from fastapi import FastAPI
from typing import Type
from sapp.core.container import ContainerManager, BaseApplicationContainer
from sapp.settings import Settings
from logging import Logger

from sapp.controllers import StudentController, TeacherController, SchoolClassController


class Application(FastAPI):
    VERSION = '1.0.0'

    def __init__(self, cls_container: Type[BaseApplicationContainer]):
        self.container_manager = ContainerManager(cls_container)
        self.container = self.container_manager.get_container()
        self.settings = self.container.get(Settings)
        self.app_name = self.settings.title_application
        self.logger = self.container.get(Logger)
        self.student_controller = self.container.get(StudentController)
        self.teacher_controller = self.container.get(TeacherController)
        self.school_class_controller = self.container.get(SchoolClassController)


        super().__init__(title=self.app_name, version=self.VERSION)

        self.include_router(self.student_controller.router, tags=['Student'])
        self.include_router(self.teacher_controller.router, tags=['Teacher'])
        self.include_router(self.school_class_controller.router, tags=['School class'])

        self.run()

    def __setup_listeners(self):
        self.router.add_event_handler('startup', self.container_manager.run_startup)
        self.router.add_event_handler('shutdown', self.container_manager.run_shutdown)

    def run(self) -> None:
        self.logger.info(f'Application {self.app_name} is starting...')
