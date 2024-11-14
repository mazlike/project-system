from django import forms
from .models import Project
from .models import Task

class ProjectRequestForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = "Название идеи проекта"
        self.fields['description'].label = "Описание идеи проекта"


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'assigned_to', 'deadline']
