from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count, Exists, Q
from django.db.models.functions import Greatest
from main.forms import UserForm, ProfileForm, PostContentForm, PostForm
from main.models import *
from django.contrib.postgres.search import SearchHeadline, SearchQuery, SearchVector, SearchRank
from django.contrib.postgres.search import TrigramSimilarity


def get_paginated_posts(request):
    items_per_page = 10
    page = request.GET.get('page')
    post_type = request.GET.get('posts_type', 'global')  # Default to 'global' if not provided

    user = request.user
    if post_type != 'global' and not user.is_authenticated:
        return JsonResponse({'rendered_posts': ''})

    queryset = Post.objects.filter(status="published")
    if post_type != 'global':
        queryset = queryset.filter(author__in=user.followings.all().values_list('following'))

    paginator = Paginator(queryset, items_per_page)

    try:
        current_page = paginator.page(page)
    except EmptyPage:
        return JsonResponse({'rendered_posts': ''})

    # Render the data in a template
    rendered_posts = render_to_string('includes/rendered_posts.html', { 'posts': current_page, 'user_is_authenticated': user.is_authenticated })
    return JsonResponse({'rendered_posts': rendered_posts})

def home(request):
    
    user = request.user

    who_to_follow = User.objects.annotate(count=Count("followers")).order_by("-count")[:5]

    most_contributors = User.objects.annotate(count=Count("posts")).order_by("-count")[:5]

    context = {
        'is_global_posts_exists': Post.objects.filter(status="published").exists(),
        'who_to_follow': who_to_follow,
        'most_contributors': most_contributors,
    }

    if request.user.is_authenticated:
        context['is_following_authors_posts_exists'] = Post.objects.filter(
            status="published", author__in=user.followings.all().values_list('following', flat=True)
        ).exists()

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


def tag_view(request, tag):
    tag_specific_posts = Post.objects.filter(tags__slug=tag)

    context = {
        'tag_posts': tag_specific_posts,
        'requested_tag': tag,
    }

    return render(request, 'tag_posts.html', context)


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

        try:
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your Profile Is Successfully Updated')
            return redirect('user_profile', user_form.username)
        except:
            messages.error(request, 'Sorry, your profile updating failed!')
            return redirect('user_profile', user_form.username)

    return render(request, 'user_profile.html', {'username': username})


@login_required
def write(request, username):
    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES)
        if request.method == 'FILES':
            post_form.thumbnail = request.POST['thumbnail']
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.author = request.user
            post.save()
            post_form.save_m2m()

            messages.success(request, 'Your Post Is Successfully Published')

            context = {
                "username": request.user.username,
                "slug": post.slug,
            }
            return redirect(reverse('post_view', kwargs=context))
        
        else:
            messages.error(request, 'Post Is Invalid')
    else:
        post_form = PostForm()
    context = {
        'username': username,
        'post_form': post_form,
    }

    return render(request, 'write.html', context)

@login_required
def unpublish(request, username, slug):
    post = get_object_or_404(Post, slug=slug)
    if(request.user.id is post.author.id):
        post_title = post.title
        post.status = 'draft'
        post.save()
        messages.success(request, f'<b>{post_title}</b> successfully drafted.')
    else:
        messages.error(request, 'Only author can unpublish their posts.')
    return redirect(reverse('author_view', kwargs={'username': username}))

@login_required
def edit(request, username, slug):
    post = Post.objects.get(slug=slug)
    if request.user != post.author:
        return redirect(reverse('post_view', kwargs={'username': request.user.username,
                                                     'slug': post.slug}))

    if request.method == 'POST':
        edit_post = PostForm(request.POST, request.FILES, instance=post)
        if request.method == 'FILES':
            edit_post.thumbnail = request.POST['thumbnail']
        if edit_post.is_valid():
            update_post = edit_post.save(commit=False)
            update_post.lastEdited = timezone.now()
            update_post.save()
            edit_post.save_m2m()

            messages.success(request, 'Your Post Is Successfully Updated')

            return redirect(reverse('post_view', kwargs={'username': request.user.username,
                                                    'slug': slug}))
        messages.error(request, 'Post Is Invalid')
    else:
        edit_post = PostForm(instance=post)

    context = {
        'username': username,
        'post': post,
        'slug': slug,
        'edit_post': edit_post,
    }
    return render(request, 'edit.html', context)

@login_required
def delete_post(request, username, slug):
    post = get_object_or_404(Post, slug=slug)
    if(request.user.id is post.author.id):
        post_title = post.title
        post.delete()
        messages.success(request, f'<b>{post_title}</b> successfully deleted')
    else:
        messages.error(request, 'Only author can delete their posts.')
    return redirect(reverse('author_view', kwargs={'username': username}))


def post_view(request, username, slug):
    post = Post.objects.get(slug=slug)
    author = get_object_or_404(User, username=username)
    user = request.user
    user_follows_author = False
    user_subscribed_author = False
    star_post_status = 'notStarred'
    save_post_satus = 'notSaved'

    if user.is_authenticated:
        user_follows_author = author.followers.filter(follower=user).exists()
        user_subscribed_author = author.subscribers.filter(subscriber=user).exists()
        if post.stars.filter(id=user.id).exists():
            star_post_status = 'starred'
        if post.saves.filter(id=user.id).exists():
            save_post_satus = 'saved'
    
    post_comments = post.comments.all()

    context = {
        'post': post,
        'author': author,
        'user_follows_author': user_follows_author,
        'user_subscribed_author': user_subscribed_author,
        'star_post_status': star_post_status,
        'save_post_satus': save_post_satus,
        'total_stars': post.get_total_stars(),
        'total_saves': post.get_total_saves(),
        'post_comments': post_comments,
    }
    return render(request, 'post_view.html', context)


def author_view(request, username):
    author = get_object_or_404(User, username=username)
    author_posts = author.posts.filter(status="published")

    context = {
        'author_posts': author_posts,
        'author': author,
    }
    if request.user.is_authenticated:
        user = request.user
        user_follows_author = author.followers.filter(follower=user).exists()
        user_subscribed_author = author.subscribers.filter(subscriber=user).exists()
        context['user_follows_author'] = user_follows_author
        context['user_subscribed_author'] = user_subscribed_author

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

    total_stars = post.get_total_stars()

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

    total_saves = post.get_total_saves()

    return JsonResponse({'total_saves': total_saves, 'save_post_status': status})


@login_required
def follow_author(request, username):
    author = User.objects.get(username=username)
    user = request.user
    follow_relation = author.followers.filter(follower=user)
    if follow_relation.exists():
        follow_relation.delete()
    else:
        Follow.objects.create(follower=user, following=author)

    author_followers = author.followers.count()

    return JsonResponse({'author_followers': author_followers})

@login_required
def subscribe_author(request, username):
    author = User.objects.get(username=username)
    subscription = author.subscribers.filter(subscriber=request.user)
    if subscription.exists():
        subscription.delete()
    else:
        Subscription.objects.create(author=author, subscriber=request.user)

    author_subscribers = author.subscribers.count()

    return JsonResponse({"author_subscribers": author_subscribers})


@login_required
def comment_post(request, username, slug):
    post = Post.objects.get(id=request.POST.get('post_id'))
    comment_content = request.POST.get('content')

    comment = Comment.objects.create(author=request.user, post=post, content=comment_content)
    comment_item = render_to_string('includes/comment_item.html', {'comment': comment, 'post': post,}, request=request)

    return JsonResponse({'comment_item': comment_item})


@login_required
def reply_comment(request, username, slug):
    parent_comment = Comment.objects.get(id=request.POST.get('parent_id'))
    reply_content = request.POST.get('content')
    post = parent_comment.post

    reply_comment = Comment.objects.create(author=request.user, post=post, content=reply_content, parent=parent_comment)
    reply_item = render_to_string('includes/reply_item.html', {'reply': reply_comment}, request=request)

    return JsonResponse({'reply_item': reply_item})


@login_required
def user_starred_posts(request, username):
    user = User.objects.get(username=username)
    posts = user.post_stars.all()

    context = {
        "posts": posts,
    }

    return render(request, 'user_starred_posts.html', context)


@login_required
def user_saved_posts(request, username):
    user = User.objects.get(username=username)
    posts = user.post_saves.all()

    context = {
        "posts": posts,
    }

    return render(request, 'user_saved_posts.html', context)


def search_view(request):
    search_results = []
    similar_search_results = []
    if request.method == "GET":
        searched_text = request.GET.get('search-input')
        query = SearchQuery(searched_text)
        vector = SearchVector('title','tags__name', 'description', 'content')
        expressions = ('title','tags__name', 'description', 'content')
        title_headline = SearchHeadline('title', query, start_sel='<mark>', stop_sel='</mark>')
        description_headline = SearchHeadline('description', query, start_sel='<mark>', stop_sel='</mark>')
        content_headline = SearchHeadline('content', query, start_sel='<mark>', stop_sel='</mark>')
        search_results = Post.objects.annotate(
            search=vector, title_headline=title_headline, description_headline=description_headline, content_headline=content_headline
        ).filter(search=query)
        search_results = set(search_results)

        if(len(search_results) <= 10):
            search_results_ids = {post.id for post in search_results}
            similar_search_results = Post.objects.exclude(id__in=search_results_ids).annotate(similarity=Greatest(
                TrigramSimilarity('title', searched_text), 
                TrigramSimilarity('tags__name', searched_text), 
                TrigramSimilarity('description', searched_text),
                TrigramSimilarity('content', searched_text)),
            ).filter(
                Q(similarity__gte=0.1)
            ).order_by('-similarity').distinct()


    context = {
        "searched_text": searched_text,
        "search_results": search_results,
        "similar_search_results": similar_search_results,
    }

    return render(request, 'search_results.html', context)