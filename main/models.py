import os

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.text import slugify
from django_resized import ResizedImageField
from tinymce import models as tinymce_models
from taggit.managers import TaggableManager


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = ResizedImageField(size=(360, 360), crop=['middle', 'center'], upload_to='user_profile/avatar',
                               default="user_profile/avatar/default_user_avatar.jpg")
    bio = models.TextField(max_length=500, default="")

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    def __str__(self):
        return f"{self.user.username}' Profile"



class Follow(models.Model):
    following = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    follower = models.ForeignKey(User, related_name='followings', on_delete=models.CASCADE)
    following_since = models.DateTimeField(default=timezone.now)


class Subscription(models.Model):
    author = models.ForeignKey(User, related_name="subscribers", on_delete=models.CASCADE)
    subscriber = models.ForeignKey(User, related_name="subscriptions", on_delete=models.CASCADE)
    starts_at = models.DateField(default=timezone.now)


class Post(models.Model):
    class PostObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status='published')

    options = (
        ('draft', 'Draft'),
        ('published', 'Published'), 
    )

    author = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='posts', null=True)
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='published', blank=True)
    content = tinymce_models.HTMLField()
    tags = TaggableManager(blank=True)
    published = models.DateTimeField(default=timezone.now)
    lastEdited = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10, choices=options, default='published')
    thumbnail = ResizedImageField(size=(1280, 720), upload_to='posts/thumbnails', default="", blank=True, null=True)
    stars = models.ManyToManyField(User, related_name='post_stars', blank=True)
    saves = models.ManyToManyField(User, related_name='post_saves', blank=True)
    objects = models.Manager()  # default manager
    PostObjects = PostObjects()  # custom manager

    class Meta:
        ordering = ('-published', 'title', 'id')

    def __str__(self):
        return self.title

    def get_total_stars(self):
        return self.stars.count()

    def get_total_saves(self):
        return self.saves.count()

    def thumbnail_name(self):
        return os.path.basename(self.thumbnail.name)

    def display_all_tags(self):
        return ", ".join(tag for tag in self.tags.names())

    def save(self, *args, **kwargs):
        super(Post, self).save(*args, **kwargs)
        if not self.slug:
            self.slug = "{}{}{}".format(slugify(self.title), "-", self.id)
            Post.objects.filter(id=self.id).update(slug=self.slug)


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    parent = models.ForeignKey('self', related_name='replies', on_delete=models.SET_NULL, null=True, blank=True)
    content = models.TextField(blank=False)
    posted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        ordering = ("-posted_at",)

