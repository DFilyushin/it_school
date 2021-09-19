from logging import Logger
from injector import singleton, provider

from sapp.connectors.mongo_connector import MongoDBConnector
from sapp.core.container import BaseApplicationContainer
from sapp.settings import Settings
from sapp.services.student_service import StudentService
from sapp.controllers import StudentController, SchoolClassController, TeacherController, EducationSubjectController, \
    UserController, QuizController, EducationController
from sapp.repositories import StudentRepository, SchoolClassRepository, TeacherRepository, SubjectRepository, \
    UserRepository, GroupRepository, QuizRepository, QuizQuestionRepository, EducationPlanRepository, \
    EducationTopicRepository, AchievementRepository


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
    def provide_student_controller(
            self,
            repository: StudentRepository,
            teacher: TeacherRepository,
            achievement: AchievementRepository,
            education_plan_repository: EducationPlanRepository,
            subject_repository: SubjectRepository,
            topic_repository: EducationTopicRepository
    ) -> StudentController:
        return StudentController(
            repository,
            teacher,
            achievement,
            education_plan_repository,
            subject_repository,
            topic_repository
        )

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

    @singleton
    @provider
    def provide_subject_controller(self, repository: SubjectRepository) -> EducationSubjectController:
        return EducationSubjectController(repository)

    @singleton
    @provider
    def provide_subject_repository(self, connector: MongoDBConnector, settings: Settings) -> SubjectRepository:
        return SubjectRepository(connector, settings)

    @singleton
    @provider
    def provide_user_repository(self, connector: MongoDBConnector, settings: Settings) -> GroupRepository:
        return GroupRepository(connector, settings)

    @singleton
    @provider
    def provide_group_repository(self, connector: MongoDBConnector, settings: Settings) -> UserRepository:
        return UserRepository(connector, settings)

    @singleton
    @provider
    def provide_user_controller(self, users: UserRepository, groups: GroupRepository) -> UserController:
        return UserController(users, groups)

    @singleton
    @provider
    def provide_quiz_repository(self, connector: MongoDBConnector, settings: Settings) -> QuizRepository:
        return QuizRepository(connector, settings)

    @singleton
    @provider
    def provide_quiz_question_repository(self, connector: MongoDBConnector,
                                         settings: Settings) -> QuizQuestionRepository:
        return QuizQuestionRepository(connector, settings)

    @singleton
    @provider
    def provide_quiz_controller(self, quiz: QuizRepository, quiz_question: QuizQuestionRepository) -> QuizController:
        return QuizController(quiz, quiz_question)

    @singleton
    @provider
    def provide_education_plan_repository(self, connector: MongoDBConnector,
                                          settings: Settings) -> EducationPlanRepository:
        return EducationPlanRepository(connector, settings)

    @singleton
    @provider
    def provide_education_achievement_repository(
            self, connector: MongoDBConnector,
            settings: Settings
    ) -> AchievementRepository:
        return AchievementRepository(connector, settings)

    @singleton
    @provider
    def provide_education_topic_repository(
            self,
            connector: MongoDBConnector,
            settings: Settings
    ) -> EducationTopicRepository:
        return EducationTopicRepository(connector, settings)

    @singleton
    @provider
    def provide_education_controller(
            self,
            topic: EducationTopicRepository,
            plan: EducationPlanRepository,
            achievement: AchievementRepository
    ) -> EducationController:
        return EducationController(topic, plan, achievement)

    @singleton
    @provider
    def provide_student_service(self) -> StudentService:
        return StudentService()
