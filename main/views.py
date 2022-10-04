from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from main.forms import UserForm, ProfileForm, PostContentForm, PostForm
from main.models import Profile, Category, Post


def home(request):
    all_posts = Post.objects.filter(status="published")
    user = request.user

    who_to_follow = Profile.objects.annotate(user_followers=Count('followers')).order_by('-user_followers')[0:5]

    # for the future pending work
    # all_posts_paginator = Paginator(all_posts, 2)
    # following_authors_posts_paginator = Paginator(following_authors_posts,2)
    #
    # gp_page_number = request.GET.get('gp-page')
    # fp_page_number = request.GET.get('fp-page')
    #
    # all_posts = all_posts_paginator.get_page(gp_page_number)
    # following_authors_posts = following_authors_posts_paginator.get_page(fp_page_number)

    context = {
        'all_posts': all_posts,
        'who_to_follow': who_to_follow,
    }

    if request.user.is_authenticated:
        following_authors_posts = all_posts.filter(author__in=user.profile.following.all())
        context['following_authors_posts'] = following_authors_posts

    return render(request, 'main_page.html', context)


def sign_up_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        set_password = request.POST['setPassword']
        confirm_password = request.POST['confirmPassword']
        redirect_path = request.POST['next']

        # logic
        if set_password != confirm_password:
            messages.warning(request, 'Given passwords did not match')
            return HttpResponseRedirect(redirect_path)

        # create the user
        new_user = User.objects.create_user(username, email, set_password)
        new_user.first_name = firstname
        new_user.last_name = lastname
        new_user.save()
        login(request, new_user)
        messages.success(request, 'Your account has been created successfully')
        return HttpResponseRedirect(redirect_path)

    else:
        return render(request, 'main_page.html')


def sign_in_user(request):
    # redirect_to = request.REQUEST.get('next', '')
    if request.method == 'POST':
        # get the post parameters
        username = request.POST['signInUsername']
        password = request.POST['password']
        redirect_path = request.POST['next']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Success')
            return HttpResponseRedirect(redirect_path)

        else:
            messages.warning(request, 'Check Credentials')
            return HttpResponseRedirect(redirect_path)

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
    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES)
        post_content_form = PostContentForm(request.POST)
        post_form.title = request.POST['title']
        post_form.category = categories.get(id=request.POST['category'])
        post_form.content = post_content_form
        if request.method == 'FILES':
            post_form.thumbnail = request.POST['thumbnail']
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.author = request.user
            post.save()

            messages.success(request, 'Your Post Is Successfully Published')

            context = {
                "username": request.user.username,
                "slug": post.slug,
            }
            return redirect('post_view', context)
        elif not post_form.is_valid():
            messages.error(request, 'Post Is Invalid')
    else:
        post_form = PostForm()
    context = {
        'username': username,
        'categories': categories,
        'post_form': post_form,
    }

    return render(request, 'write.html', context)

@login_required
def unpublish(request, username, slug):
    post = Post.objects.get(slug=slug)
    post.status = 'draft'
    post.save();
    return redirect('author_view', username);

@login_required
def edit(request, username, slug):
    post = Post.objects.get(slug=slug)
    if request.user != post.author:
        return redirect(reverse('post_view', kwargs={'username': request.user.username,
                                                     'slug': post.slug}))

    categories = Category.objects.all()
    if request.method == 'POST':
        edit_post = PostForm(request.POST, request.FILES, instance=post)
        post_content_form = PostContentForm(request.POST)
        edit_post.title = request.POST['title']
        edit_post.category = categories.get(id=request.POST['category'])
        if request.method == 'FILES':
            edit_post.thumbnail = request.POST['thumbnail']
        update_post = edit_post.save(commit=False)
        update_post.lastEdited = timezone.now()
        update_post.save()

        messages.success(request, 'Your Post Is Successfully Updated')

        return redirect(reverse('post_view', kwargs={'username': request.user.username,
                                                    'slug': slug}))
    else:
        edit_post = PostForm(instance=post)

    context = {
        'username': username,
        'categories': categories,
        'post': post,
        'slug': slug,
        'edit_post': edit_post,
    }
    return render(request, 'edit.html', context)


def post_view(request, username, slug):
    post = Post.objects.get(slug=slug)
    author = get_object_or_404(User, username=username)
    user = request.user
    follow_author_status = 'notFollowed'
    subscribe_author_status = 'notSubscribed'
    star_post_status = 'notStarred'
    save_post_satus = 'notSaved'

    if author.profile.followers.filter(id=user.id).exists():
        follow_author_status = 'followed'
    if author.profile.subscribers.filter(id=user.id).exists():
        subscribe_author_status = 'subscribed'
    if post.stars.filter(id=user.id).exists():
        star_post_status = 'starred'
    if post.saves.filter(id=user.id).exists():
        save_post_satus = 'saved'

    context = {
        'post': post,
        'author': author,
        'follow_author_status': follow_author_status,
        'subscribe_author_status': subscribe_author_status,
        'star_post_status': star_post_status,
        'save_post_satus': save_post_satus,
        'total_stars': post.get_totalStars(),
        'total_saves': post.get_totalSaves()
    }
    return render(request, 'post_view.html', context)


def author_view(request, username):
    author = get_object_or_404(User, username=username)
    author_posts = author.posts.filter(status="published")
    user = request.user

    follow_author_status = 'notFollowed'
    subscribe_author_status = 'notSubscribed'

    if author.profile.followers.filter(id=user.id).exists():
        follow_author_status = 'followed'
    if author.profile.subscribers.filter(id=user.id).exists():
        subscribe_author_status = 'subscribed'
    context = {
        'author_posts': author_posts,
        'author': author,
        'follow_author_status': follow_author_status,
        'subscribe_author_status': subscribe_author_status,
    }
    return render(request, 'author_view.html', context)


@login_required
def star_post(request, username, slug):
    post_id = request.POST.get('post_id')
    user_response = request.POST.get('response')

    post = get_object_or_404(Post, id=post_id)
    
    if post.stars.filter(id=request.user.id).exists():
        if(user_response == 'clicked'):
            post.stars.remove(request.user)
            status = 'notStarred'
        else:
            status = 'starred'    
    else:
        if(user_response == 'clicked'):
            post.stars.add(request.user)
            status = 'starred'
        else:
            status = 'notStarred'    

    total_stars = post.get_totalStars()

    return JsonResponse({'total_stars': total_stars, 'star_post_status':status})


@login_required
def save_post(request, username, slug):
    post_id = request.POST.get('post_id')
    user_response = request.POST.get('response')

    post = get_object_or_404(Post, id=post_id)

    if post.saves.filter(id=request.user.id).exists():
        if(user_response == 'clicked'):
            post.saves.remove(request.user)
            status = 'notSaved'
        else:
            status = 'saved'    
    else:
        if(user_response == 'clicked'):
            post.saves.add(request.user)
            status = 'saved'
        else:
            status = 'notSaved'    

    total_saves = post.get_totalSaves()

    return JsonResponse({'total_saves': total_saves, 'save_post_status': status})


@login_required
def follow_author(request, username):
    author_username = request.POST.get('author_username')
    author = User.objects.get(username=author_username)
    user = request.user
    if author.profile.followers.filter(id=user.id).exists():
        author.profile.followers.remove(user)
        user.profile.following.remove(author)
    else:
        author.profile.followers.add(user)
        user.profile.following.add(author)

    author_followers = author.profile.followers.count()

    return JsonResponse({'author_followers': author_followers})

@login_required
def subscribe_author(request, username):
    author_username = request.POST.get('author_username')
    author = User.objects.get(username=author_username)
    if author.profile.subscribers.filter(id=request.user.id).exists():
        author.profile.subscribers.remove(request.user)
    else:
        author.profile.subscribers.add(request.user)

    return JsonResponse({'username': username})
