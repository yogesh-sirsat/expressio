from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect

from main.forms import UserForm, ProfileForm
from main.models import Profile


def index(request):
    return render(request, 'main_page.html')


def sign_up_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        set_password = request.POST['setPassword']
        confirm_password = request.POST['confirmPassword']
        # logic
        if set_password != confirm_password:
            messages.warning(request, 'Given passwords did not match')
            return redirect('home')

        # create the user
        new_user = User.objects.create_user(username, email, set_password)
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
            messages.success(request, 'Your Profile Successfully Updated')
            return redirect('user_profile', user_form.username)

    return render(request, 'user_profile.html', {'username': username})
