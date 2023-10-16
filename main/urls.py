from django.conf.urls.static import static
from django.urls import path, include, re_path
from django.contrib.auth import views as auth_views
from expressio import settings
from django.views.static import serve
from main import views

import os

urlpatterns = [
  path('', views.home, name='home'),
  path('signup', views.sign_up_user, name='sign_up_user'),
  path('signin', views.sign_in_user, name='sign_in_user'),
  path('logout', auth_views.LogoutView.as_view(), name='logout'),
  path('get_paginated_posts', views.get_paginated_posts, name='get_paginated_posts'),
  path('search/', views.search_view, name='search_view'),
  path('tag/<slug:tag>', views.tag_view, name='tag_view'),
  path('<str:username>', views.author_view, name='author_view'),
  path('<str:username>/profile', views.user_profile, name='user_profile'),
  path('<str:username>/profile/starred-posts', views.user_starred_posts, name='user_starred_posts'),
  path('<str:username>/profile/saved-posts', views.user_saved_posts, name='user_saved_posts'),
  path('<str:username>/write', views.write, name='write'),
  path('<str:username>/<slug:slug>/unpublish', views.unpublish, name='unpublish'),
  path('<str:username>/<slug:slug>/edit', views.edit, name='edit'),
  path('<str:username>/<slug:slug>/delete', views.delete_post, name='delete_post'),
  path('<str:username>/<slug:slug>', views.post_view, name='post_view'),
  path('<str:username>/<slug:slug>/star-post', views.star_post, name='star_post'),
  path('<str:username>/<slug:slug>/save-post', views.save_post, name='save_post'),
  path('<str:username>/author-view/follow-author', views.follow_author, name='follow_author'),
  path('<str:username>/author-view/subscribe-author', views.subscribe_author, name='subscribe_author'),
  path('<str:username>/<slug:slug>/comment-post', views.comment_post, name='comment_post'),
  path('<str:username>/<slug:slug>/reply-comment', views.reply_comment, name='reply_comment'),
  path('api/', include('main.api.urls', namespace='main_api')),

]
if os.getenv('USE_AWS_S3') != 'True':
  urlpatterns += static(settings.base.MEDIA_URL, document_root=settings.base.MEDIA_ROOT)
