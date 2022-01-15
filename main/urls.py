from django.conf.urls.static import static
from django.urls import path, include, re_path
from django.contrib.auth import views as auth_views
from expressio import settings
from django.views.static import serve
from main import views

urlpatterns = [
                path('', views.index, name='home'),
                path('signup', views.sign_up_user, name='sign_up_user'),
                path('signin', views.sign_in_user, name='sign_in_user'),
                path('logout', auth_views.LogoutView.as_view(), name='logout'),
                path('<str:username>', views.author_view, name='author_view'),
                path('<str:username>/profile', views.user_profile, name='user_profile'),
                path('<str:username>/write', views.write, name='write'),
                path('<str:username>/<slug:slug>/edit', views.edit, name='edit'),
                path('<str:username>/<slug:slug>', views.post_view, name='post_view'),
                path('<str:username>/<slug:slug>/post-stars', views.post_stars, name='post_stars'),
                path('<str:username>/<slug:slug>/post-saves', views.post_saves, name='post_saves'),
                path('api/', include('main.api.urls', namespace='main_api')),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
