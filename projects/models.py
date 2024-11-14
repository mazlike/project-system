from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название проекта")
    description = models.TextField(verbose_name="Описание проекта")
    progress = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="Прогресс проекта")  # в процентах
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_projects", verbose_name="Создатель")
    members = models.ManyToManyField(User, blank=True, related_name="joined_projects", verbose_name="Участники")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return self.name


class Task(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название задачи")
    description = models.TextField(verbose_name="Описание задачи")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks", verbose_name="Проект")
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="tasks", verbose_name="Исполнитель")
    deadline = models.DateTimeField(verbose_name="Срок выполнения", null=True, blank=True)
    is_completed = models.BooleanField(default=False, verbose_name="Завершена")

    def __str__(self):
        return self.title
    
class Application(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(User, on_delete=models.CASCADE)
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending')
    
    def __str__(self):
        return f"{self.applicant.username} -> {self.project.title}"