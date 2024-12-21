from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from projects.models import Project
# Create your models here.

class Report(models.Model):
    STATUS_CHOICES = [
        ('pending', 'На рассмотрении'),
        ('approved', 'Принят'),
        ('revision', 'На доработке'),
        ('rejected', 'Отклонен'),
    ]

    project = models.ForeignKey(
        'projects.Project',
        on_delete=models.CASCADE,
        related_name='reports',
        verbose_name='Проект'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reports',
        verbose_name='Автор'
    )
    title = models.CharField(max_length=255, verbose_name='Название отчета')
    content = models.TextField(verbose_name='Содержание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='Статус'
    )
    feedback = models.TextField(blank=True, null=True, verbose_name='Комментарии преподавателя')

    class Meta:
        verbose_name = 'Отчет'
        verbose_name_plural = 'Отчеты'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.get_status_display()}"

class Note(models.Model):
    addressed_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='received_notes')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField(verbose_name='Заметка')
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(
        max_length=50,
        choices=[
            ('correction', 'Исправление'),
            ('feedback', 'Обратная связь'),
            ('commendation', 'Похвала'),
            ('criticism', 'Критика')
        ],
        default='feedback'
    )
    # Поля для GenericForeignKey
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    def __str__(self):
        return f"Заметка {self.author.username} для {self.content_object}"