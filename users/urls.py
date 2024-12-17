from django.urls import path
from django.contrib.auth import views as auth_views
from users import views

app_name = 'users'

urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('profile/<str:username>', views.ProfileView.as_view(), name='profile'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('search-students/', views.UserSearchView.as_view(), name='search-students'),
    
]