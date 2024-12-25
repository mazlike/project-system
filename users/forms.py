from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from users.models import User
    
class UserRegistrationForm(UserCreationForm):

    first_name = forms.CharField(max_length=30, required=True, label="Имя")
    last_name = forms.CharField(max_length=30, required=True, label="Фамилия")
    email = forms.EmailField(required=True, label="Электронная почта")
    
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput,
        help_text="Пароль должен быть минимум 8 символов"
    )
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']
class ProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "username",
            "email",)

    first_name = forms.CharField(max_length=30, label="Имя")
    last_name = forms.CharField(max_length=30, label="Фамилия")

class SearchUserForm(forms.Form):
    username = forms.CharField(label='Имя пользователя', max_length=150)
