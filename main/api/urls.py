from django.urls import path
from .views import PostList, PostDetail

app_name = 'main_api'

urlpatterns = [
    path('<int:pk>/', PostDetail.as_view(), name='detailCreate'),
    path('', PostList.as_view(), name='listCreate')
]
