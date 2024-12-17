from django.urls import path
from django.contrib.auth import views as auth_views
from projects import views

app_name = 'projects'

urlpatterns = [
    path('project/<int:id>',views.ProjectView.as_view(), name='project'),
]