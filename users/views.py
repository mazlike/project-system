from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.views.generic import DetailView
from django.contrib import auth, messages
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import AuthenticationForm
from projects.forms import ApplicationForm, TeacherApplicationForm
from projects.models import Application, Project, TeacherApplication
from users.forms import UserRegistrationForm
from users.models import User
from django.db import transaction

class UserLoginView(LoginView):
    template_name = 'main/index.html'
    form_class = AuthenticationForm
    
    def get_success_url(self):
        redirect_page = self.request.POST.get('next', None)
        if redirect_page:
            return redirect_page
        return reverse_lazy('users:profile', args=[self.request.user.username])
    
    def form_valid(self, form):
        user = form.get_user()
        if user:
            auth.login(self.request, user)
            messages.success(self.request, "Вы успешно вошли в систему.")
            # Перенаправляем пользователя на URL, указанный в get_success_url()
            return redirect(self.get_success_url())
        # Если пользователь не найден или сессия отсутствует, возвращаем стандартный ответ
        return super().form_valid(form)
    def form_invalid(self, form):
        # Генерируем обновленную страницу с формой, где есть ошибки
        context = self.get_context_data(login_form=form)
        html = render_to_string('main/index.html', context, request=self.request)

        # Проверяем, это AJAX-запрос или нет
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'html': html})

        # Если запрос не AJAX, перенаправляем на главную страницу
        messages.error(self.request, "Проверьте корректность данных в форме.")
        return redirect('main:index')

class UserRegistrationView(CreateView):
    template_name = 'main/index.html'
    form_class = UserRegistrationForm

    def get_success_url(self):
        # После успешной регистрации перенаправляем на профиль пользователя
        return reverse_lazy('users:profile', args=[self.request.user.username])

    def form_valid(self, form):
        user = form.save()  # Сохраняем форму и создаем пользователя
        if user.is_teacher == True:
            user.is_student = False
            user.save()
        
        auth.login(self.request, user)  # Выполняем авторизацию для нового пользователя
        messages.success(self.request, f"{user.username}, Вы успешно зарегистрированы и вошли в аккаунт.")

        # Проверяем, это ли AJAX-запрос
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return self.render_messages()

        # Перенаправляем пользователя, если запрос не AJAX
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        # Генерируем обновленную страницу с формой, где есть ошибки
        context = self.get_context_data(register_form=form)
        html = render_to_string('main/index.html', context, request=self.request)

        # Проверяем, это AJAX-запрос или нет
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'html': html})

        # Если запрос не AJAX, перенаправляем на главную страницу
        messages.error(self.request, "Проверьте корректность данных в форме.")
        return redirect('main:index')


    def render_messages(self):
        """Рендеринг только блока сообщений."""
        html = render_to_string('messages.html', {'messages': messages.get_messages(self.request)})
        return JsonResponse({'html': html})
    
class ProfileView(LoginRequiredMixin, DetailView):
    template_name = 'users/profile.html'
    context_object_name = 'user'

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Передаем заявки и форму для подачи заявки в контекст
        if user.is_teacher:
            context['teacher_applications'] = TeacherApplication.objects.filter(created_by=user)
            context['teacher_application_form'] = TeacherApplicationForm()
            
            # Если пользователь - преподаватель, показываем заявки, адресованные ему
            context['applications'] = Application.objects.filter(supervisor=user, status='pending')
        else:
            # Если пользователь - студент, показываем его заявки и учителя
            context['teacher_applications'] = TeacherApplication.objects.all()
            context['applications'] = Application.objects.filter(applicant=user)
        context['application_form'] = ApplicationForm()
        if user.is_teacher:
            context['projects'] = Project.objects.filter(created_by=user)
        else:
            context['projects'] = Project.objects.filter(members=user)
        return context
    
    def post(self, request, *args, **kwargs):
        if 'submit_application' in request.POST:
            form = ApplicationForm(request.POST)
            if form.is_valid():
                application = form.save(commit=False)
                application.applicant = request.user
                
                # Получаем данные из js
                leader_username = request.POST.get('leader_input')
                team_members_usernames = request.POST.getlist('team_members_input')
                
                # Находим лидера и участников команды
                leader = User.objects.filter(username=leader_username).first()
                team_members = User.objects.filter(username__in=team_members_usernames)
                application.leader = leader
                
                application.save()
                application.team_members.set(team_members)  # Сохраняем участников команды
                
                messages.success(request, 'Заявка успешно отправлена.')
            else:
                messages.error(request, 'Ошибка при отправке заявки.')
            return redirect('users:profile', username=request.user.username)
        
        # Обработка принятия заявки преподавателем
        elif 'approve_application' in request.POST:
            application_id = request.POST.get('application_id')
            application = get_object_or_404(Application, id=application_id)
            
            if application.supervisor != request.user:
                messages.error(request, 'У вас нет прав на выполнение этого действия.')
                return redirect('users:profile', username=self.request.user.username)

            application.status = "approved"
            # Проверяем, что заявка одобрена
            if application.status == 'approved':
                with transaction.atomic():
                    # Создаем проект
                    project = application.create_project()

                    # Удаляем заявку
                    application.delete()
            messages.success(request, f"Заявка принята. Проект '{project.title}' создан.")
            return redirect('users:profile', username=self.request.user.username)
        elif 'create_application' in request.POST:
            form = TeacherApplicationForm(request.POST)
            if form.is_valid():
                application = form.save(commit=False)
                application.created_by = request.user
                application.save()
                messages.success(request, 'Заявка успешно создана.')
            else:
                messages.error(request, 'Ошибка при создании заявки.')
            return redirect('users:profile', username=request.user.username)
        
        elif 'apply_for_application' in request.POST:
            application_id = request.POST.get('application_id')
            teacher_application = get_object_or_404(TeacherApplication, id=application_id)

            # Получаем данные из формы
            leader_username = request.POST.get('leader_input')
            team_members_usernames = request.POST.getlist('team_members_input')
            
            # Проверяем, указан ли лидер
            if not leader_username:
                messages.error(request, 'Пожалуйста, укажите лидера команды.')
                return redirect('users:profile', username=request.user.username)

            # Проверяем, указаны ли участники
            if not team_members_usernames:
                messages.error(request, 'Пожалуйста, добавьте хотя бы одного участника команды.')
                return redirect('users:profile', username=request.user.username)
            print(request.POST)

            # Находим лидера и участников команды
            leader = User.objects.filter(username=leader_username).first()
            team_members = User.objects.filter(username__in=team_members_usernames)
            print(team_members)
            if not team_members.exists():
                messages.error(request, 'Не удалось найти участников команды.')
                return redirect('users:profile', username=request.user.username)
            
            # Создаем заявку
            student_application = Application.objects.create(
                applicant=request.user,
                project_title=teacher_application.title,
                project_description=teacher_application.description,
                supervisor=teacher_application.created_by,
                leader=leader
            )
            student_application.team_members.set(team_members)

            messages.success(request, 'Заявка на проект успешно отправлена.')
            return redirect('users:profile', username=request.user.username)
        elif 'delete_application' in request.POST:
            application_id = request.POST.get('application_id')
            if request.user.is_teacher:
                application = get_object_or_404(TeacherApplication, id=application_id, created_by=request.user)
            else:
                application = get_object_or_404(Application, id=application_id, applicant=request.user)

            application.delete()
            messages.success(request, 'Заявка успешно удалена.')
            return redirect('users:profile', username=request.user.username)
        return super().post(request, *args, **kwargs)
    
class UserSearchView(View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('query', '')
        users = User.objects.filter(username__icontains=query, is_student=True)[:5]  # Топ-5 результатов
        results = [{'username': user.username, 'id': user.id} for user in users]
        return JsonResponse(results, safe=False)
