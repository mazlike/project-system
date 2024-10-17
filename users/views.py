from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView
from django.contrib import auth, messages

from users.forms import UserLoginForm

class UserLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    
    def get_success_url(self):
        redirect_page = self.request.POST.get('next', None)
        if redirect_page:
            return redirect_page
        return reverse_lazy('main:index')
    
    def form_valid(self, form):
        session_key = self.request.session.session_key
        user = form.get_user()
        print(user)
        if user:
            auth.login(self.request, user)
            if session_key:
                messages.success(self.request, "Вы успешно вошли в систему.")
                return HttpResponseRedirect(self.get_success_url())


class ProfileView(TemplateView):
    template_name = 'profile.html' 