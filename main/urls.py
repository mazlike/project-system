from django.urls import path
from .views import AboutView, IndexView, NewsView

app_name = 'main'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),  # Например, главная страница
    path('news/', NewsView.as_view(), name= 'news'),
    path('about/', AboutView.as_view(), name= 'about'),
]