from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from .models import Task
from .forms import TaskForm
from .models import Project
from .forms import ProjectRequestForm
from django.contrib import messages

class ProjectRequestView(CreateView):
    model = Project
    form_class = ProjectRequestForm
    template_name = 'projects/project_request.html'
    success_url = reverse_lazy('projects:project_list')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        messages.success(self.request, "Заявка на проект успешно отправлена!")
        return super().form_valid(form)

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
