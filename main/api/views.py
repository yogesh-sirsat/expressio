from rest_framework import generics
from main.models import Post
from .serializers import PostSerializer


# Create your views here.
class PostList(generics.ListCreateAPIView):
    queryset = Post.PostObjects.all()
    serializer_class = PostSerializer


class PostDetail(generics.RetrieveDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
