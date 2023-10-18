"""expressio URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.contrib.auth import views as auth_views
from django.views.static import serve

from expressio import settings

import os

urlpatterns = [
    path('', include('main.urls')),
    path(os.getenv('ADMIN_DASHBOARD_URL', 'admin'), admin.site.urls),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('tinymce/', include('tinymce.urls')),

]
if os.getenv('USE_AWS_S3') != 'True':
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve,
            {'document_root': settings.base.MEDIA_ROOT}),
        re_path(r'^static/(?P<path>.*)$', serve,
            {'document_root': settings.base.STATIC_ROOT}),
    ]
