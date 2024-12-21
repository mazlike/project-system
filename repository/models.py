from django.db import models
from django.conf import settings
from git import Repo, exc
from projects.models import Project
from tasks.models import Task

class File(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='files')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='files', null=True, blank=True)
    user_file_name = models.CharField(max_length=255, null=True, blank=True)
    file_name = models.CharField(max_length=255, null=True, blank=True)
    file_path = models.CharField(max_length=255, null=True, blank=True)  # Путь к файлу в репозитории
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='uploaded_files')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        task_info = f" (Задача: {self.task.title})" if self.task else ""  # Проверяем, есть ли задача
        return f"{self.file.name}{task_info}"
    
class Repository(models.Model):
    project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name='repository')
    path = models.CharField(max_length=255, unique=True)  # Путь к локальному репозиторию
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Repository for {self.project.title}"
    
    def get_last_changes(self):
        """
        Возвращает последние изменения из репозитория.
        :param limit: Количество последних коммитов для вывода.
        :return: Список изменений.
        """
        try:
            repo = Repo(self.path)
            # Определяем ветку по умолчанию
            try:
                default_branch = repo.head.reference.name  # Получаем текущую ветку
            except exc.GitCommandError as e:
                return {'error': f"Ошибка при определении ветки по умолчанию: {str(e)}"}
            changes = []

            # Получаем последние коммиты
            for commit in repo.iter_commits(default_branch):  # Используем 'main' или 'master' в зависимости от ветки
                changes.append({
                    'message': commit.message.strip(),  # Сообщение коммита
                    'date': commit.committed_datetime,  # Дата коммита
                })

            return changes
        except Exception as e:
            # Обработка ошибок
            return {'error': str(e)}