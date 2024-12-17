from projects.models import Project
from .models import Task
from django import forms


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'assigned_to', 'deadline']

    title = forms.CharField(label="Название задачи", max_length=255)
    description = forms.CharField(label="Описание задачи", widget=forms.Textarea)
    deadline = forms.DateTimeField(
        label="Дедлайн",
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        required=False
    )