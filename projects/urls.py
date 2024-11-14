from django.urls import path
from .views import ApplicationCreateView, ProjectCreateView, ProjectDetailView, ProjectListView, TaskListView, TaskCreateView

app_name = 'projects'

urlpatterns = [
    path('<int:project_id>/tasks/', TaskListView.as_view(), name='task_list'),
    path('<int:project_id>/tasks/create/', TaskCreateView.as_view(), name='task_create'),
    path('', ProjectListView.as_view(), name='project_list'),
    path('create/', ProjectCreateView.as_view(), name='project_create'),
    path('<int:pk>/apply/', ApplicationCreateView.as_view(), name='apply'),
    path('<int:pk>/', ProjectDetailView.as_view(), name='detail'),  # для получения данных в формате JSON
]
