from django import forms

from users.models import User

from .models import Application, Project, TeacherApplication

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description']  # укажите поля, которые хотите включить
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название проекта'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Описание проекта'}),
        }
        
class SearchUserForm(forms.Form):
    username = forms.CharField(label='Имя пользователя', max_length=150)

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['project_title', 'project_description', 'leader', 'supervisor']

    project_title = forms.CharField(label="Название проекта", max_length=255)
    project_description = forms.CharField(label="Описание проекта", widget=forms.Textarea)
    leader = forms.ModelChoiceField(queryset=User.objects.filter(is_student=True), label="Лидер команды")
    supervisor = forms.ModelChoiceField(queryset=User.objects.filter(is_teacher=True), label="Руководитель проекта", required=False)

class TeacherApplicationForm(forms.ModelForm):
    class Meta:
        model = TeacherApplication
        fields = ['title', 'description', 'requirements']
    
    title = forms.CharField(label="Название проекта", max_length=255)
    description = forms.CharField(label="Описание проекта", widget=forms.Textarea)
    requirements = forms.CharField(label="Требования", widget=forms.Textarea)