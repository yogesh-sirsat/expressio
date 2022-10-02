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


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    avatar = ResizedImageField(size=(360, 360), crop=['middle', 'center'], upload_to='user_profile/avatar',
                               default="user_profile/avatar/default_user_avatar.jpg")
    bio = models.TextField(max_length=500, default="")
    following = models.ManyToManyField(User, related_name='user_following', blank=True)
    followers = models.ManyToManyField(User, related_name='user_followers', blank=True)
    subscribers = models.ManyToManyField(User, related_name='user_subscribers', blank=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        try:
            instance.profile.save()
        except ObjectDoesNotExist:
            Profile.objects.create(user=instance)
        if created:
            Profile.objects.create(user=instance)

    def __str__(self):
        return f"{self.user.username}' Profile"

    post_save.connect(create_user_profile, sender=User)

    def get_totalFollowing(self):
        return self.following.count()

    def get_totalFollowers(self):
        return self.followers.count()


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Post(models.Model):
    class PostObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status='published')

    options = (
        ('draft', 'Draft'),
        ('published', 'Published'), 
    )

    category = models.ForeignKey(Category, on_delete=models.PROTECT, default=1)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', null=True)
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='published', blank=True)
    content = tinymce_models.HTMLField()
    published = models.DateTimeField(default=timezone.now)
    lastEdited = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10, choices=options, default='published')
    thumbnail = ResizedImageField(size=(480, 720), upload_to='posts/thumbnails', default="", blank=True, null=True)
    stars = models.ManyToManyField(User, related_name='post_stars', blank=True)
    saves = models.ManyToManyField(User, related_name='post_saves', blank=True)
    objects = models.Manager()  # default manager
    PostObjects = PostObjects()  # custom manager

    class Meta:
        ordering = ('-published', 'title', 'id')

    def __str__(self):
        return self.title

    def get_totalStars(self):
        return self.stars.count()

    def get_totalSaves(self):
        return self.saves.count()

    def thumbnail_name(self):
        return os.path.basename(self.thumbnail.name)

    def save(self, *args, **kwargs):
        super(Post, self).save(*args, **kwargs)
        if not self.slug:
            self.slug = "{}{}{}".format(slugify(self.title), "-", self.id)
            Post.objects.filter(id=self.id).update(slug=self.slug)
