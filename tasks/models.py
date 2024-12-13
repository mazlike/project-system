from django.db import models
from projects.models import Project
from django.conf import settings
from django.utils.timezone import now
class Task(models.Model):
    STATUS_CHOICES = [
        ('открыта', 'Открыта'),
        ('в работе', 'В работе'),
        ('выполнена', 'Выполнена'),
        ('требуется проверка', 'Требуется проверка'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255)
    description = models.TextField()
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tasks')
    created_at = models.DateTimeField(default=now, verbose_name="Дата создания")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    solution = models.TextField(blank=True, null=True)
    code_branch = models.CharField(max_length=255, blank=True, null=True)
    deadline = models.DateTimeField(verbose_name="Срок выполнения", null=True, blank=True)

    def __str__(self):
        return self.title