from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, TemplateView, UpdateView
from django.contrib.auth.views import LoginView
from django.views.generic import DetailView
from django.contrib import auth, messages
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import AuthenticationForm
from projects.forms import ApplicationForm, TeacherApplicationForm
from projects.models import Application, Project, TeacherApplication
from tasks.forms import TaskForm
from users.forms import UserRegistrationForm
from users.models import User

class ProjectView(LoginRequiredMixin, DetailView):
    template_name = 'projects/project.html'
    model = Project  # Модель проекта
    context_object_name = 'project'
    
    def get_object(self):
        project_id = self.kwargs.get('id')  # Извлекаем ID из URL
        return get_object_or_404(Project, id=project_id)
    
    def get_context_data(self, **kwargs):
        # Получаем стандартный контекст от родительского класса
        context = super().get_context_data(**kwargs)

        # Добавляем данные о проекте
        project = self.get_object()  # Это объект проекта, связанный с DetailView
        context['project'] = project

        # Пример добавления дополнительных данных
        context['project_title'] = project.title
        context['project_description'] = project.description
        
        context['leader'] = project.leader
        context['members'] = project.members.all()  # Получаем всех участников проекта
        
        tasks = project.tasks.all()
        context['tasks'] = tasks
        context['task_form'] = TaskForm()
        return context
    
    def post(self, request, *args, **kwargs):
        project_id = self.kwargs.get('id')
        
        # Обработка создания задачи
        if 'create_task' in request.POST:
            project = get_object_or_404(Project, id=project_id)
            form = TaskForm(request.POST)
            if form.is_valid():
                task = form.save(commit=False)
                task.project = project  # Привязываем задачу к проекту
                task.save()
                messages.success(request, 'Задача успешно создана.')
            else:
                messages.error(request, 'Ошибка при создании задачи.')
            return redirect('projects:project', id=project.id)
        
        return super().get(request, *args, **kwargs)