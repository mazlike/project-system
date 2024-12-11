from django.urls import path
from tasks.views import TaskCreateView, TaskListView

app_name = 'tasks' 

urlpatterns = [
    path('', TaskListView.as_view(), name='task_list'),
    path('create/', TaskCreateView.as_view(), name='task_create'),
    ]