from django.urls import path
from .views import AddMemberView, ApplicationActionView, ApplicationCreateView, ApplicationsListView, ProjectCreateView, ProjectListView, RepositoryView, TaskListView, TaskCreateView

app_name = 'projects'

urlpatterns = [
    path('<int:project_id>/tasks/', TaskListView.as_view(), name='task_list'),
    path('<int:project_id>/tasks/create/', TaskCreateView.as_view(), name='task_create'),
    
    path('<int:project_id>/repository/', RepositoryView.as_view(), name='repository'),
    path('<int:pk>/apply/', ApplicationCreateView.as_view(), name='apply'),
    path('create/', ProjectCreateView.as_view(), name='project_create'),
    path('<int:project_id>/add_member/', AddMemberView.as_view(), name='add_member'),
    path('', ProjectListView.as_view(), name='project_list'),
    
    path('applications/<int:application_id>/action/', ApplicationActionView.as_view(), name='application_action'),
    path('applications/', ApplicationsListView.as_view(), name='applications_list'),
]
