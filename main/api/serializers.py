from rest_framework import serializers

from main.models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'category', 'author', 'title', 'slug', 'content', 'published',
                  'lastEdited', 'status', 'thumbnail', 'claps',)
