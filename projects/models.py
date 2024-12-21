from django.db import models
from django.conf import settings
import uuid

class Project(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название проекта")
    description = models.TextField(verbose_name="Описание проекта", default="Описание проекта отсутствует")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_projects', verbose_name="Создан у", default=1)  # Устанавливаем дефолтного пользователя
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    leader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='led_projects', verbose_name="Лидер проекта")
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='projects', blank=True, verbose_name="Участники проекта")
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    
    def __str__(self):
        return self.title

    
    
class Application(models.Model):
    applicant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='applications')
    project_title = models.CharField(max_length=255, verbose_name="Название проекта", null=True)
    project_description = models.TextField(verbose_name="Описание проекта",null=True)
    team_members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='applications_as_member', blank=True, verbose_name="Участники команды")
    leader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name='led_applications', verbose_name="Лидер команды")
    supervisor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='supervised_applications', verbose_name="Руководитель проекта")
    applied_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата подачи заявки")
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', verbose_name="Статус")

    def __str__(self):
        return f"{self.applicant.username} -> {self.project_title}"
    
    def create_project(self):
        """
        Создает проект на основе заявки.
        """
        from projects.models import Project  # Избегаем циклического импорта
        project = Project.objects.create(
            title=self.project_title,
            description=self.project_description,
            created_by=self.supervisor,  # Проект создается преподавателем
            leader=self.leader
        )
        # Добавляем участников команды
        project.members.set(self.team_members.all())

        return project
    
class TeacherApplication(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название проекта")
    description = models.TextField(verbose_name="Описание проекта")
    requirements = models.TextField(verbose_name="Требования к команде")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_teacher_applications', verbose_name="Создан у")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return self.title
    
class Evaluation(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='evaluations')
    grade = models.CharField(max_length=2, choices=[('5', '5'), ('4', '4'), ('3', '3'), ('na', 'н/а')])
    team_comment = models.TextField(blank=True, null=True)
    personal_comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Оценка для проекта {self.project.title}"