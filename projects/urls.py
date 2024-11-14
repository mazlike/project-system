from django.urls import path
from .views import ProjectRequestView, TaskListView, TaskCreateView

app_name = 'projects'

urlpatterns = [
    path('request/', ProjectRequestView.as_view(), name='project_request'),
    path('<int:project_id>/tasks/', TaskListView.as_view(), name='task_list'),
    path('<int:project_id>/tasks/create/', TaskCreateView.as_view(), name='task_create'),
]
