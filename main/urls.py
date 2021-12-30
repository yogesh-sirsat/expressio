from django.urls import path, include

from main import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/', include('main.api.urls', namespace='main_api'))
]
