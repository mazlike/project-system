from django.db.models.signals import post_save
from django.dispatch import receiver
from git import Repo # type: ignore
import os

from projects.models import Project
from repository.models import Repository

@receiver(post_save, sender=Project)
def create_repository(sender, instance, created, **kwargs):
    if created:
        repo_path = os.path.join('path/to/repositories', str(instance.uuid)).replace('\\','/')  # Укажите базовый путь
        os.makedirs(repo_path, exist_ok=True)
        Repo.init(repo_path)  # Инициализация Git-репозитория
        Repository.objects.create(project=instance, path=repo_path)