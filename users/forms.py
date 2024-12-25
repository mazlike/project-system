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
    is_teacher = forms.BooleanField(
        label="Преподаватель?",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        required=False,  # Поле не обязательно для заполнения
        help_text="Отметьте, если вы являетесь преподавателем.",  # Текст подсказки
        initial=False,  # Начальное значение по умолчанию
        error_messages={'required': 'Пожалуйста, укажите, являетесь ли вы преподавателем.'}  # Сообщение об ошибке
        )
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'is_teacher']
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
