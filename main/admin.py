from django.contrib import admin
from django import forms
from . import models
from main.models import Post
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


admin.site.register(models.Profile)
admin.site.register(models.Post, PostAdmin)
