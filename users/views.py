from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView
from django.contrib.auth.views import LoginView
from django.contrib import auth, messages
from django.contrib.auth.mixins import LoginRequiredMixin

from users.forms import UserLoginForm, UserRegistrationForm

class UserLoginView(LoginView):
    template_name = 'main/index.html'
    form_class = UserLoginForm
    
    def get_success_url(self):
        redirect_page = self.request.POST.get('next', None)
        if redirect_page:
            return redirect_page
        return reverse_lazy('users:profile', args=[self.request.user.username])
    
    def form_valid(self, form):
        session_key = self.request.session.session_key
        user = form.get_user()
        if user:
            auth.login(self.request, user)
            messages.success(self.request, "Вы успешно вошли в систему.")
            # Перенаправляем пользователя на URL, указанный в get_success_url()
            return redirect(self.get_success_url())
        # Если пользователь не найден или сессия отсутствует, возвращаем стандартный ответ
        return super().form_valid(form)

class UserRegistrationView(CreateView):
    template_name = 'users/registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('users:profile')

    def form_valid(self, form):
        user = form.instance

        if user:
            form.save()
            auth.login(self.request, user)

        messages.success(self.request, f"{user.username}, Вы успешно зарегистрированы и вошли в аккаунт")
        return HttpResponseRedirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home - Регистрация'
        return context

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'users/profile.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu_items'] = [
            {'name': 'Менеджер проектов', 'url': 'projects:manager'},
            {'name': 'Задач', 'url': 'tasks:overview'},
        ]
        context['title'] = 'Профиль'
        return context
    def dispatch(self, request, *args, **kwargs):
        # Проверяем, совпадает ли username из URL с текущим пользователем
        if kwargs.get('username') != request.user.username:
            # Перенаправляем на страницу профиля текущего пользователя
            return redirect('profile', username=request.user.username)
        return super().dispatch(request, *args, **kwargs)