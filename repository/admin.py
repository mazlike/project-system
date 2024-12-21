import os
from django.utils.html import format_html
from django.contrib import admin
from .models import File, Repository

# Регистрация модели Repository
@admin.register(Repository)
class RepositoryAdmin(admin.ModelAdmin):
    list_display = ('project', 'path', 'created_at')
    actions = ['clean_repository']  # Добавляем действие

    def clean_repository(self, request, queryset):
        """
        Удаляет все файлы из репозитория.
        """
        for repository in queryset:
            repo_path = repository.path
            if os.path.exists(repo_path):
                files = os.listdir(repo_path)
                for file_name in files:
                    file_path = os.path.join(repo_path, file_name)
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                self.message_user(request, f"Репозиторий {repository.project.title} очищен.")
            else:
                self.message_user(request, f"Репозиторий {repository.project.title} не существует.", level='error')

    clean_repository.short_description = "Очистить репозиторий"

@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('file_name', 'project', 'task', 'uploaded_by', 'uploaded_at')
    actions = ['delete_files_from_repository']  # Добавляем действие

    def delete_files_from_repository(self, request, queryset):
        """
        Удаляет файлы из репозитория и базы данных.
        """
        for file in queryset:
            # Удаляем файл из репозитория
            repository = file.project.repository
            repo_path = repository.path
            file_path = os.path.join(repo_path, file.file_name)
            if os.path.exists(file_path):
                os.remove(file_path)

            # Удаляем файл из базы данных
            file.delete()

        self.message_user(request, "Выбранные файлы удалены из репозитория и базы данных.")

    delete_files_from_repository.short_description = "Удалить файлы из репозитория и базы данных"   