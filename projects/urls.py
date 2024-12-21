from django.urls import path
from django.contrib.auth import views as auth_views
from projects import views

app_name = 'projects'

urlpatterns = [
    path('project/<uuid:uuid>',views.ProjectView.as_view(), name='project'),
    path('project/<uuid:project_uuid>/download/<int:file_id>/', views.download_file, name='download_file'),
]