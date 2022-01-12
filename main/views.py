from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse
from django.utils import timezone

from main.forms import UserForm, ProfileForm, PostForm
from main.models import Profile, Category, Post


def index(request):
    return render(request, 'main_page.html')


def sign_up_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        set_password = request.POST['setPassword']
        confirm_password = request.POST['confirmPassword']
        # logic
        if set_password != confirm_password:
            messages.warning(request, 'Given passwords did not match')
            return redirect('home')

        # create the user
        new_user = User.objects.create_user(username, email, set_password)
        new_user.first_name = firstname
        new_user.last_name = lastname
        new_user.save()
        login(request, new_user)
        messages.success(request, 'Your account has been created successfully')
        return redirect('home')
    else:
        return render(request, 'main_page.html')


def sign_in_user(request):
    if request.method == 'POST':
        # get the post parameters
        username = request.POST['signInUsername']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have successfully logged in')
            return redirect('home')

        else:
            messages.warning(request, ' Username/Password is Wrong ')
            return redirect('home')

    else:
        return render(request, 'main_page.html')


@login_required
def user_profile(request, username):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        # user form
        user_form.first_name = request.POST['first_name']
        user_form.last_name = request.POST['last_name']
        user_form.username = request.POST['username']
        user_form.email = request.POST['email']

        # profile form
        if request.method == 'FILES':
            profile_form.avatar = request.FILES['avatar']
        profile_form.bio = request.POST['bio']

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your Profile Is Successfully Updated')
            return redirect('user_profile', user_form.username)

    return render(request, 'user_profile.html', {'username': username})


@login_required
def write(request, username):
    categories = Category.objects.all()
    post_form = PostForm(request.POST, request.FILES)
    if request.method == 'POST':
        post_form.title = request.POST['title']
        post_form.category = categories.get(id=request.POST['category'])
        post_form.content = request.POST['content']
        if request.method == 'FILES':
            post_form.thumbnail = request.POST['thumbnail']
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.author = request.user
            post.save()

            messages.success(request, 'Your Post Is Successfully Published')

            return redirect('user_view', request.user.username)
        elif not post_form.is_valid():
            messages.error(request, 'Post Is Invalid')

    context = {
        'username': username,
        'categories': categories,
    }

    return render(request, 'write.html', context)


@login_required
def edit(request, username, slug):
    post = Post.objects.get(slug=slug)
    if request.user != post.author:
        return redirect(reverse('post_view', kwargs={'username': request.user.username,
                                                     'slug': post.slug}))

    categories = Category.objects.all()
    edit_post = PostForm(request.POST, request.FILES, instance=post)
    if request.method == 'POST':
        edit_post.title = request.POST['title']
        edit_post.category = categories.get(id=request.POST['category'])
        edit_post.content = request.POST['content']
        if request.method == 'FILES':
            edit_post.thumbnail = request.POST['thumbnail']
        if edit_post.is_valid():
            update_post = edit_post.save(commit=False)
            update_post.lastEdited = timezone.now()
            update_post.save()

            messages.success(request, 'Your Post Is Successfully Updated')

            return redirect(reverse('post_view', kwargs={'username': request.user.username,
                                                         'slug': slug}))
    context = {
        'username': username,
        'categories': categories,
        'post': post,
        'slug': slug,
    }
    return render(request, 'edit.html', context)


def post_view(request, username, slug):
    post = Post.objects.get(slug=slug)
    author = get_object_or_404(User, username=username)
    context = {
        'post': post,
        'author': author,
    }
    return render(request, 'post_view.html', context)


def author_view(request, username):
    author = get_object_or_404(User, username=username)
    author_posts = Post.objects.filter(author=author)
    context = {
        'author_posts': author_posts,
        'author': author,
    }
    return render(request, 'author_view.html', context)
