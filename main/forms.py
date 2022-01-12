from django import forms
from django.forms import ModelForm
from .models import Profile, Post
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email',)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('avatar', 'bio')


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'category', 'thumbnail', 'content')

    def PostSave(self, user):
        post = self.save(commit=False)
        post.author = user
        post.save()
        return post
