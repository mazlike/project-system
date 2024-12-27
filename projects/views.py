import os
from django.http import FileResponse, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from git import Repo # type: ignore
from projects.models import Evaluation, Project
from reports.models import Note, Report
from repository.models import File
from tasks.forms import TaskForm, Task
from users.models import User
from django.contrib.contenttypes.models import ContentType
from django.utils.timezone import now
from django.db.models import Q
from django.db.models import Count

class ProjectView(LoginRequiredMixin, DetailView):
    template_name = 'projects/project.html'
    model = Project  # Модель проекта
    context_object_name = 'project'
    
    def get_object(self):
        project_uuid = self.kwargs.get('uuid')  # Извлекаем ID из URL
        return get_object_or_404(Project, uuid=project_uuid)
    
    def get_context_data(self, **kwargs):
        # Получаем стандартный контекст от родительского класса
        context = super().get_context_data(**kwargs)

        # Добавляем данные о проекте
        project = self.get_object()  # Это объект проекта, связанный с DetailView
        context['project'] = project
        # Добавляем информацию об оценках
        
        context['has_evaluation'] = project.evaluations.exists()
        if context['has_evaluation'] == True:
            context['evaluation'] = project.evaluations.last().grade
        # Пример добавления дополнительных данных
        context['project_title'] = project.title
        context['project_description'] = project.description
        
        context['leader'] = project.leader
        context['curator'] = project.created_by
        context['members'] = project.members.all()  # Получаем всех участников проекта
        
        tasks = project.tasks.all()
        context['tasks'] = tasks
        context['task_form'] = TaskForm()
        # Получаем заметки для каждой задачи
        task_notes = {}
        for task in tasks:
            notes = Note.objects.filter(
                content_type=ContentType.objects.get_for_model(Task),
                object_id=task.id
            )
            task_notes[task.id] = notes
        # Получаем файлы для каждой задачи
        task_files = {}
        for task in tasks:
            task_files = task.files.all()  # Получаем файлы, связанные с задачей

        context['task_files'] = task_files
        context['task_notes'] = task_notes  # Добавляем заметки в контекст
        # Получаем репозиторий проекта
        repository = project.repository
        if repository:
        # Получаем список файлов в репозитории
            repo_path = repository.path
            if os.path.exists(repo_path):
                repository_files = os.listdir(repo_path)
                # Связываем файлы с объектами модели File
                file_objects = File.objects.filter(project=project, file_name__in=repository_files)
                context['repository_files'] = file_objects
                # Получаем последние изменения из репозитория
                context['last_changes'] = repository.get_last_changes()
                print("Last changes:", context['last_changes'])
            else:
                context['repository_files'] = []
                context['last_changes'] = []
        else:
            context['repository_files'] = []
        context['total_tasks'] = tasks.count()  # Всего задач
        context['completed_tasks'] = tasks.filter(status='выполнена').count()  # Выполненные задачи
        context['necessary_completed_tasks'] = tasks.filter(status='выполнена', is_necessary=True).count()  # Необходимые выполненные задачи
        # Фильтруем просроченные задачи
        overdue_tasks = tasks.filter(
            Q(deadline__lt=now()) &  # Дедлайн меньше текущего времени
            Q(status__in=['открыта', 'в работе']) &  # Статус "открыта" или "в работе"
            Q(marked_as_completed_at__isnull=True) |  # Задача не отмечена как выполненная
            Q(marked_as_completed_at__gt=now())  # Или отмечена как выполненная, но после дедлайна
        )

        context['overdue_tasks'] = overdue_tasks.count()  # Количество просроченных задач


        # Вычисляем данные для заметок (если нужно)
        # Получаем все заметки для проекта
        # Получаем заметки для всех задач
        task_notes = Note.objects.filter(
            content_type=ContentType.objects.get_for_model(Task),
            object_id__in=tasks.values_list('id', flat=True)
        )
        if task_notes:
            # Фильтруем заметки, оставленные текущим пользователем
            user_notes = task_notes.filter(author=self.request.user)
            
            # Группируем заметки по категориям и подсчитываем их количество
            category_counts = task_notes.values('category').annotate(count=Count('id'))
            category_stats = {item['category']: item['count'] for item in category_counts}
            
            # Добавляем данные в контекст
            context['total_notes'] = notes.count()  # Всего заметок
            context['user_notes_count'] = user_notes.count()  # Заметок, созданных текущим пользователем
            context['category_stats'] = category_stats  # Статистика по категориям
        return context
    
    def post(self, request, *args, **kwargs):
        project_uuid = self.kwargs.get('uuid')
        
        # Обработка создания задачи
        if 'create_task' in request.POST:
            project = get_object_or_404(Project, uuid=project_uuid)
            is_necessary = request.POST.get('is_necessary') == "on"
            form = TaskForm(request.POST)
            if form.is_valid():
                task = form.save(commit=False)
                task.project = project  # Привязываем задачу к проекту
                if is_necessary != False: task.is_necessary = is_necessary
                task.save()
                messages.success(request, 'Задача успешно создана.')
            else:
                messages.error(request, 'Ошибка при создании задачи.')
            return redirect('projects:project', uuid=project_uuid)
        if 'delete_task' in request.POST:
            task_id = request.POST.get('task_id')
            task = get_object_or_404(Task, id=task_id)

            # Удаляем задачу из системы
            if task:

                # Удаляем запись о задаче из базы данных
                task.delete()

                messages.success(request, 'Задача успешна удалена.')
            else:
                messages.error(request, 'Задачи не существует')

            return redirect('projects:project', uuid=project_uuid)
            
        if 'create_note' in request.POST:
            note_content = request.POST.get('noteContent')  # Получаем содержимое заметки
            addressed_to_id = request.POST.get('addressedTo')  # Получаем ID адресата
            object_type = request.POST.get('objectType')  # Тип объекта (task, report и т.д.)
            object_id = request.POST.get('objectId')  # ID объекта
            note_category = request.POST.get('noteCategory')
            
            if note_content:
                # Определяем объект, к которому привязываем заметку
                if object_type == 'task':
                    content_object = Task.objects.get(id=object_id)
                elif object_type == 'report':
                    content_object = Report.objects.get(id=object_id)
                else:
                    messages.error(request, 'Что-то пошло не так')
                    return redirect('projects:project', uuid=project_uuid)
                if addressed_to_id:
                    user = User.objects.get(id = addressed_to_id )
                else:
                    user = None
                # Создаем заметку
                Note.objects.create(
                    author=request.user,
                    addressed_to=user ,
                    content=note_content,
                    content_object=content_object,
                    category=note_category,
                )
                messages.success(request, 'Заметка успешно создана')
                return redirect('projects:project', uuid=project_uuid)
        if 'delete_note' in request.POST:
            note_id = request.POST.get('note_id')
            note = get_object_or_404(Note, id=note_id)

            # Удаляем задачу из системы
            if note:
                # Удаляем запись о задаче из базы данных
                note.delete()
                messages.success(request, 'Заметка успешна удалена.')
            else:
                messages.error(request, 'Заметки не существует')

            return redirect('projects:project', uuid=project_uuid)    
            
        if 'upload_file' in request.POST:
            task_id = request.POST.get('taskId')
            project = get_object_or_404(Project, uuid=project_uuid)
            task = get_object_or_404(Task, id=task_id) if task_id else None
            file = request.FILES.get('file')
            user_file_name = request.POST.get('user_file_name')

            if file:
                # Получаем репозиторий проекта
                repository = project.repository
                repo_path = repository.path

                # Сохраняем файл в репозитории
                file_path_in_repo = os.path.join(repo_path, file.name)
                with open(file_path_in_repo, 'wb+') as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)

                # Фиксируем изменения в репозитории
                repo = Repo(repo_path)
                repo.index.add([file.name])
                repo.index.commit(f"Uploaded file: {file.name}")

                # Создаём запись в базе данных
                uploaded_file = File.objects.create(
                    project=project,
                    task=task,
                    user_file_name=user_file_name,
                    file_name=file.name,
                    file_path=file_path_in_repo,  # Сохраняем путь к файлу в репозитории
                    uploaded_by=request.user
                )

                messages.success(request, 'Файл успешно загружен.')
            else:
                messages.error(request, 'Необходимо выбрать файл для загрузки.')

            return redirect('projects:project', uuid=project_uuid)
        if 'delete_file' in request.POST:
            file_id = request.POST.get('file_id')
            file = get_object_or_404(File, id=file_id)

            # Проверяем, имеет ли пользователь право удалять файл
            if request.user == file.uploaded_by:
                # Получаем путь к файлу в репозитории
                file_path = file.file_path

                # Удаляем файл из файловой системы
                if os.path.exists(file_path):
                    os.remove(file_path)

                    # Получаем репозиторий проекта
                    repository = file.project.repository
                    repo_path = repository.path

                    # Удаляем файл из индекса Git-репозитория
                    repo = Repo(repo_path)
                    repo.index.remove([os.path.basename(file_path)])

                    # Создаем коммит для удаления файла
                    repo.index.commit(f"Deleted file: {file.file_name}")

                    # Удаляем запись о файле из базы данных
                    file.delete()

                    messages.success(request, 'Файл успешно удалён.')
                else:
                    messages.error(request, 'Файл не найден в файловой системе.')
            else:
                messages.error(request, 'У вас нет прав на удаление этого файла.')

            return redirect('projects:project', uuid=project_uuid)
        # Обработка изменения статуса задачи
        if 'change_status' in request.POST:
            task_id = request.POST.get('task_id')
            new_status = request.POST.get('status')
            task = get_object_or_404(Task, id=task_id)

            task.status = new_status
            task.save()
            messages.success(request, 'Статус задачи успешно изменён.')

            return redirect('projects:project', uuid=project_uuid)
        if 'submit_evaluation' in request.POST:
            project = self.get_object()
            grade = request.POST.get('grade')
            team_comment = request.POST.get('team-comment')
            personal_comment = request.POST.get('personal-comment')

            if grade:
                Evaluation.objects.create(
                    project=project,
                    grade=grade,
                    team_comment=team_comment,
                    personal_comment=personal_comment,
                )
                messages.success(request, 'Оценка успешно сохранена.')
            else:
                messages.error(request, 'Пожалуйста, выберите оценку.')

            return redirect('projects:project', uuid=project.uuid)
        return super().get(request, *args, **kwargs)
# Представление для скачивания файла
def download_file(request, project_uuid, file_id):
    file = get_object_or_404(File, id=file_id)

    # Проверяем, что файл принадлежит проекту
    if file.project.uuid != project_uuid:
        return HttpResponse("Файл не найден", status=404)

    # Проверяем, что файл существует
    if not os.path.exists(file.file_path):
        return HttpResponse("Файл не найден", status=404)

    # Определяем MIME-тип файла
    if file.file_name.endswith('.docx'):
        content_type = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    elif file.file_name.endswith('.xlsx'):
        content_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    else:
        content_type = 'application/octet-stream'

    # Открываем файл и возвращаем его как ответ
    response = FileResponse(open(file.file_path, 'rb'), content_type=content_type)
    response['Content-Disposition'] = f'attachment; filename="{file.file_name}"'
    return response