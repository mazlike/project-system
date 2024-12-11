from django.urls import include, path
from .views import AddMemberView, ApplicationActionView, ApplicationCreateView, ApplicationsListView, ProjectCreateView, ProjectListView, RepositoryView

app_name = 'projects'

urlpatterns = [
    path('<int:project_id>/repository/', RepositoryView.as_view(), name='repository'),
    path('create/', ProjectCreateView.as_view(), name='project_create'),
    path('<int:project_id>/add_member/', AddMemberView.as_view(), name='add_member'),
    path('', ProjectListView.as_view(), name='project_list'),
    
    # Подключение URL-адресов из приложения tasks
    path('<int:project_id>/tasks/', include('tasks.urls', namespace='tasks')),
    
    path('<int:pk>/apply/', ApplicationCreateView.as_view(), name='apply'),
    path('applications/<int:application_id>/action/', ApplicationActionView.as_view(), name='application_action'),
    path('applications/', ApplicationsListView.as_view(), name='applications_list'),
]
