from django.db import models
from django.dispatch import receiver
from projects.models import Project
from django.conf import settings
from django.utils.timezone import now
from django.db.models.signals import pre_save

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
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='открыта')
    solution = models.TextField(blank=True, null=True)
    code_branch = models.CharField(max_length=255, blank=True, null=True)
    deadline = models.DateTimeField(verbose_name="Срок выполнения", null=True, blank=True)
    status_changed_at = models.DateTimeField(null=True, blank=True)
    marked_as_completed_at = models.DateTimeField(null=True, blank=True)
    is_necessary = models.BooleanField(verbose_name="Необходимо", default=False)    
    
    def __str__(self):
        return self.title
    
    def mark_as_completed(self):
        """Метод для установки задачи как выполненной или требующей проверки."""
        if self.status in ['выполнена', 'требуется проверка']:
            self.marked_as_completed_at = now()
            self.save()

    def check_deadline(self):
        """Метод для проверки дедлайна и установки статуса 'не в срок'."""
        if self.deadline and self.deadline < now() and self.status not in ['выполнена', 'требуется проверка']:
            self.status = 'не в срок'
            self.save()

@receiver(pre_save, sender=Task)
def update_status_fields(sender, instance, **kwargs):
    """Сигнал для обновления полей при изменении статуса."""
    if instance.pk:
        old_instance = Task.objects.get(pk=instance.pk)
        if old_instance.status != instance.status:
            instance.status_changed_at = now()
            if instance.status in ['выполнена', 'требуется проверка']:
                instance.marked_as_completed_at = now()