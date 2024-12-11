from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView
from django.contrib.auth.views import LoginView
from django.views.generic import DetailView
from django.contrib import auth, messages
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import AuthenticationForm
from projects.models import Application
from users.forms import UserRegistrationForm

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

class UserRegistrationView(CreateView):
    template_name = 'main/index.html'
    form_class = UserRegistrationForm

    def get_success_url(self):
        # После успешной регистрации перенаправляем на профиль пользователя
        return reverse_lazy('users:profile', args=[self.request.user.username])

    def form_valid(self, form):
        user = form.save()  # Сохраняем форму и создаем пользователя
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
        context['applications'] = Application.objects.filter(applicant=self.request.user)
        return context