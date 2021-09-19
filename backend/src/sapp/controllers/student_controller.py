from typing import Optional, List
from fastapi import APIRouter
from uuid import UUID
from datetime import datetime

from sapp.models.student import StudentModel
from sapp.repositories.student_repository import StudentRepository
from sapp.repositories.teacher_repository import TeacherRepository
from sapp.repositories.education_repository import AchievementRepository, EducationPlanRepository, \
    EducationTopicRepository
from sapp.repositories import SubjectRepository
from sapp.serializers.student import StudentSerializer
from sapp.serializers.education import AchievementSerializer
from sapp.serializers.process import StudentAchieveSerializer, StudentNewAchieveSerializer, \
    StudentNewAssessmentSerializer, StudentAssessmentSerializer


class StudentController:

    def __init__(
            self,
            repository: StudentRepository,
            teacher_repository: TeacherRepository,
            achievement_repository: AchievementRepository,
            education_plan_repository: EducationPlanRepository,
            subject_repository: SubjectRepository,
            topic_repository: EducationTopicRepository
    ) -> None:
        self.router = APIRouter()
        self.repository = repository
        self.teacher_repository = teacher_repository
        self.achievement_repository = achievement_repository
        self.education_plan_repository = education_plan_repository
        self.subject_repository = subject_repository
        self.topic_repository = topic_repository
        self._register_routes()

    def _register_routes(self):
        @self.router.get('/students', name='Get students')
        async def get_students() -> List[StudentSerializer]:
            result = []
            students = await self.repository.get_students()
            for student in students:
                result.append(StudentSerializer(
                    **student.dict()
                ))
            return result

        @self.router.get('/student/{id}', name='Get student by id')
        async def get_student(id: UUID):
            model = await self.repository.get_student(id)
            return model.dict()

        @self.router.post('/student/', name='Create new student')
        async def new_student(student: StudentSerializer):
            student_dob = datetime.combine(student.dob, datetime.min.time())
            new_student_object = StudentModel(
                first_name=student.first_name,
                last_name=student.last_name,
                patronymic=student.patronymic,
                dob=student_dob
            )
            await self.repository.new_student(new_student_object)

        @self.router.delete('/student/{id}', name='Delete student by id')
        async def delete_student(id: UUID):
            await self.repository.delete_student(id)

        @self.router.get('/student/{id_student}/achievements', name='Get students achievements')
        async def get_student_achieves(id_student: UUID) -> List[StudentAchieveSerializer]:
            result = []
            items = await self.repository.get_achievements(id_student)
            for item in items:
                try:
                    teacher = await self.teacher_repository.get_teacher(item.teacher_id)
                    achievement = await self.achievement_repository.get_achievement(item.achievement_id)
                    education_plan = await self.education_plan_repository.get_plan(item.plan_id)
                    subject = await self.subject_repository.get_subject(education_plan.subject_id)
                    result.append(
                        StudentAchieveSerializer(
                            id=item.id,
                            teacher=teacher.get_full_name,
                            subject=subject.name,
                            achievement=achievement.name,
                            created=item.created
                        )
                    )
                except Exception as exc:
                    pass
            return result

        @self.router.post('/student/{id_student}/achievements', name='New students achievement')
        async def new_student_achievement(id_student: UUID, achievement: StudentNewAchieveSerializer):
            await self.repository.new_achievement(id_student, achievement.teacher_id, achievement.achievement_id,
                                                  achievement.plan_id)

        @self.router.delete('/student/{id_student}/achievements/{id}', name='Delete students achievement')
        async def delete_student_achievement(id_student: UUID, id: UUID):
            await self.repository.delete_achievement(id_student, id)

        @self.router.get('/student/{id_student}/assessments', name='Get students assessments')
        async def get_student_assessments(
                id_student: UUID,
                year: Optional[int] = None,
                id_topic: Optional[UUID] = None
        ) -> List[StudentAssessmentSerializer]:
            """Получить список оценок студента"""
            result = []
            items = await self.repository.get_assessments(id_student, year, id_topic)
            for item in items:
                try:
                    teacher = await self.teacher_repository.get_teacher(item.teacher_id)
                    topic = await self.topic_repository.get_topic(item.topic_id)
                    result.append(
                        StudentAssessmentSerializer(
                            id=item.id,
                            teacher=teacher.get_full_name,
                            topic=topic.name,
                            created=item.created,
                            value=item.value)
                    )
                except Exception as exc:
                    pass
            return result

        @self.router.post('/student/{id_student}/assessments', name='Set student assessment')
        async def add_student_assessment(id_student: UUID, assessment: StudentNewAssessmentSerializer):
            """Новая оценка студенту"""
            await self.repository.new_assessment(
                id_student,
                assessment.teacher_id,
                assessment.topic_id,
                assessment.value
            )

        @self.router.delete('/student/{id_student}/assessments/{assessment_id}', name='Delete student assessment')
        async def delete_student_assessment(id_student: UUID, assessment_id: UUID):
            """Удалить оценку"""
            await self.repository.delete_assessment(id_student, assessment_id)

        @self.router.put('/student/{student_id}/assessments/{assessment_id}/{new_value}',
                         name='Update student assessment')
        async def set_student_assessment(student_id: UUID, assessment_id: UUID, new_value: int):
            """Обновить оценку"""
            await self.repository.update_assessment(student_id, assessment_id, new_value)

        @self.router.post('/student/{id_student}/quiz/{quiz_id}', name='Set student quiz')
        async def set_student_quiz(id_student: UUID, quiz_id: UUID):
            pass

        @self.router.delete('/student/{id_student}/quiz/{quiz_id}', name='Delete student quiz')
        async def delete_student_quiz(id_student: UUID, quiz_id: UUID):
            pass
