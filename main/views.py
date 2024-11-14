from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from users.forms import UserLoginForm


class IndexView(TemplateView):
    template_name = 'main/index.html'
    def dispatch(self, request, *args, **kwargs):
        # Проверка, авторизован ли пользователь
        if request.user.is_authenticated:
            # Перенаправление авторизованного пользователя на страницу профиля
            return redirect(reverse_lazy('users:profile', args=[self.request.user.username]))
        # Если пользователь не авторизован, продолжаем обычный процесс
        return super().dispatch(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная'
        context['form'] = UserLoginForm()
        return context
    
class NewsView(TemplateView):
    template_name = 'main/news.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Новости'
        return context

class AboutView(TemplateView):
    template_name = 'main/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'О проекте'
        return context
    
