import os
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from git import Repo

from projects.forms import SearchUserForm
from users.models import User

from django.contrib import messages

from .models import Project, Application, Repository

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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Передаем первый проект как "выбранный" по умолчанию
        context['selected_project'] = self.get_queryset().first()
        return context

class AddMemberView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        # Проверяем, является ли пользователь лидером проекта
        project = get_object_or_404(Project, id=self.kwargs['project_id'])
        return self.request.user == project.leader

    def get(self, request, *args, **kwargs):
        project = get_object_or_404(Project, id=self.kwargs['project_id'])
        form = SearchUserForm()
        return render(request, 'projects/add_member.html', {'form': form, 'project': project})

    def post(self, request, *args, **kwargs):
        project = get_object_or_404(Project, id=self.kwargs['project_id'])
        form = SearchUserForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            try:
                user = User.objects.get(username=username)
                if user == project.leader:
                    messages.error(request, 'Вы не можете добавить себя в проект.')
                elif user in project.members.all():
                    messages.error(request, 'Пользователь уже является участником проекта.')
                else:
                    project.add_member(user)
                    messages.success(request, f'Пользователь {user.username} добавлен в проект.')
            except User.DoesNotExist:
                messages.error(request, 'Пользователь с таким никнеймом не найден.')

        return redirect('projects:add_member', project_id=project.id)
  
class RepositoryView(DetailView):
    model = Repository
    template_name = 'projects/repository.html'
    context_object_name = 'repository'

    def get_object(self):
        return get_object_or_404(Repository, project_id=self.kwargs['project_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        repo = Repo(self.object.path)
        context['branches'] = repo.branches
        return context
    
class ApplicationsListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Application
    template_name = 'projects/applications_list.html'
    context_object_name = 'applications'

    def test_func(self):
        return self.request.user.is_teacher

    def get_queryset(self):
        return Application.objects.filter(project__created_by=self.request.user, status='pending')

class ApplicationActionView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_teacher

    def post(self, request, *args, **kwargs):
        application_id = kwargs.get('application_id')
        action = request.POST.get('action')
        application = get_object_or_404(Application, id=application_id)

        if application.project.created_by != request.user:
            messages.error(request, 'У вас нет прав на выполнение этого действия.')
            return redirect('projects:applications_list')

        if action == 'accept':
            application.status = 'approved'
            application.project.assign_leader(application.applicant)
            messages.success(request, f'Заявка от {application.applicant.username} одобрена. Пользователь назначен лидером проекта.')
        elif action == 'reject':
            application.status = 'rejected'
            messages.success(request, f'Заявка от {application.applicant.username} отклонена.')
        else:
            messages.error(request, 'Неизвестное действие.')
            return redirect('projects:applications_list')

        application.save()
        return redirect('projects:applications_list')

class ApplicationCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    def post(self, request, *args, **kwargs):
        project_id = kwargs.get('pk')
        project = get_object_or_404(Project, id=project_id)

        if Application.objects.filter(applicant=request.user, project=project).exists():
            messages.error(request, 'Вы уже подали заявку на этот проект.')
            return redirect('users:profile', username=request.user.username)

        Application.objects.create(applicant=request.user, project=project)
        messages.success(request, 'Заявка успешно отправлена.')
        return redirect('users:profile', username=request.user.username)

    def test_func(self):
        return self.request.user.is_student