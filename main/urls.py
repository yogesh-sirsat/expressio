from django.conf.urls.static import static
from django.urls import path, include, re_path

from expressio import settings
from django.views.static import serve
from main import views

urlpatterns = [
                  path('', views.index, name='home'),
                  path('signup', views.sign_up_user, name='sign_up_user'),
                  path('signin', views.sign_in_user, name='sign_in_user'),
                  path('api/', include('main.api.urls', namespace='main_api')),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
