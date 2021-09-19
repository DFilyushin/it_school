from fastapi import FastAPI
from typing import Type
from sapp.core.container import ContainerManager, BaseApplicationContainer
from sapp.settings import Settings
from logging import Logger

from sapp.controllers import StudentController, TeacherController, SchoolClassController, EducationSubjectController, \
    UserController, QuizController, EducationController


class Application(FastAPI):
    VERSION = '1.0.0'
    API_VERSION = 1

    def __init__(self, cls_container: Type[BaseApplicationContainer]):
        self.container_manager = ContainerManager(cls_container)
        self.container = self.container_manager.get_container()
        self.settings = self.container.get(Settings)
        self.app_name = self.settings.title_application
        self.logger = self.container.get(Logger)

        self.student_controller = self.container.get(StudentController)
        self.teacher_controller = self.container.get(TeacherController)
        self.school_class_controller = self.container.get(SchoolClassController)
        self.subject_controller = self.container.get(EducationSubjectController)
        self.user_controller = self.container.get(UserController)
        self.quiz_controller = self.container.get(QuizController)
        self.education_controller = self.container.get(EducationController)

        super().__init__(title=self.app_name, version=self.VERSION)
        self.__setup_listeners()
        self.__setup_routers()

        self.run()

    def __setup_routers(self):
        api_prefix = f'/api/v{self.API_VERSION}'
        self.include_router(self.student_controller.router, tags=['Student'], prefix=api_prefix)
        self.include_router(self.teacher_controller.router, tags=['Teacher'], prefix=api_prefix)
        self.include_router(self.school_class_controller.router, tags=['School class'], prefix=api_prefix)
        self.include_router(self.subject_controller.router, tags=['Subject'], prefix=api_prefix)
        self.include_router(self.user_controller.router, tags=['Users'], prefix=api_prefix)
        self.include_router(self.quiz_controller.router, tags=['Quiz'], prefix=api_prefix)
        self.include_router(self.education_controller.router, tags=['Education'], prefix=api_prefix)

    def __setup_listeners(self):
        self.router.add_event_handler('startup', self.container_manager.run_startup)
        self.router.add_event_handler('shutdown', self.container_manager.run_shutdown)

    def run(self) -> None:
        self.logger.info(f'Application {self.app_name} is starting...')
