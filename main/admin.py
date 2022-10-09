from django.contrib import admin
from django import forms
from . import models
from main.models import *
from tinymce.widgets import TinyMCE


# Register your models here.

class PostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=TinyMCE())
    class Meta:
        model = Post
        fields = '__all__'

class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'status', 'published')
    prepopulated_fields = {'slug': ('title',), }
    form = PostAdminForm


class CommentAdmin(admin.ModelAdmin):
    list_display = ('content', 'author', 'posted_at',)
    readonly_fields = ('posted_at',)


admin.site.register(Follow)
admin.site.register(Subscription)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Post, PostAdmin)
