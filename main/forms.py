from django import forms
from django.forms import ModelForm
from .models import Profile, Post
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from tinymce.widgets import TinyMCE
from taggit.forms import TagWidget


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email',)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('avatar', 'bio')

class PostContentForm(forms.Form):
    content = forms.CharField(widget=TinyMCE())

class PostForm(forms.ModelForm):
    content = forms.CharField(widget=TinyMCE())
    class Meta:
        model = Post
        fields = ('title', 'thumbnail', 'description', 'content', 'source', 'tags')
        widgets = {
            'tags': TagWidget(),
        }

    def PostSave(self, user):
        post = self.save(commit=False)
        post.author = user
        post.save()
        return post
