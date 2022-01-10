from django.http import HttpResponse
from django.views.generic.edit import CreateView
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


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


def profile_update(request):
    pass
