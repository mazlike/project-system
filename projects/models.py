from django.db import models
from django.shortcuts import get_object_or_404

from core import settings


# В models.py
class Project(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Используйте AUTH_USER_MODEL для пользователя
    created_at = models.DateTimeField(auto_now_add=True)
    leader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='Руководитель')
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='projects', blank=True)
    
    def __str__(self):
        return self.title
    
    def assign_leader(self, user):
        """Назначает лидера проекта."""
        self.leader = user
        self.save()

    def add_member(self, user):
        """Добавляет участника в проект."""
        self.members.add(user)
        self.save()

class Task(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('needs_revision', 'Needs Revision'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255)
    description = models.TextField()
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tasks')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    solution = models.TextField(blank=True, null=True)
    code_branch = models.CharField(max_length=255, blank=True, null=True)
    deadline = models.DateTimeField(verbose_name="Срок выполнения", null=True, blank=True)
    
    def __str__(self):
        return self.title

    
class Application(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected'), ('leader', 'Leader')], default='pending')
    
    def __str__(self):
        return f"{self.applicant.username} -> {self.project.title}"

class File(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    file = models.FileField(upload_to='files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.project.title} - {self.file.name}"
    

class Repository(models.Model):
    project = models.OneToOneField(Project, on_delete=models.CASCADE)
    path = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"{self.project.title} Repository"