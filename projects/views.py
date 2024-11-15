from django.shortcuts import get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Task
from .forms import TaskForm
from .models import Project, Application

from django.contrib import messages

class ProjectCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Project
    fields = ['title', 'description']
    template_name = 'projects/project_form.html'
    success_url = reverse_lazy('projects:project_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        return self.request.user.is_teacher
    
class ProjectListView(ListView):
    model = Project
    template_name = 'projects/project_list.html'
    context_object_name = 'projects'

class ApplicationCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Application
    fields = []
    
    def form_valid(self, form):
        form.instance.applicant = self.request.user
        form.instance.project = get_object_or_404(Project, pk=self.kwargs['pk'])
        messages.success(self.request, 'Ваша заявка успешно отправлена!')
        return super().form_valid(form)
    
    def test_func(self):
        return self.request.user.is_student

class TaskListView(ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    
    def get_queryset(self):
        return Task.objects.filter(project__id=self.kwargs['project_id'])

class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    
    def form_valid(self, form):
        form.instance.project_id = self.kwargs['project_id']
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('tasks:task_list', kwargs={'project_id': self.kwargs['project_id']})
    
