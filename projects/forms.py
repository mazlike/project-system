from django import forms

from .models import Project

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
