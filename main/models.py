from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django_resized import ResizedImageField
from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    avatar = ResizedImageField(size=(360, 360), crop=['middle', 'center'], upload_to='user_profile/avatar',
                               default="user_profile/avatar/default_user_avatar.jpg")
    bio = models.TextField(max_length=500, default="")

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
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='published')
    excerpt = models.TextField(null=True)
    content = models.TextField()
    published = models.DateTimeField(default=timezone.now)
    lastEdited = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10, choices=options, default='published')
    thumbnail = ResizedImageField(size=(720, 1280), upload_to='posts/thumbnails', default="", blank=True, null=True)
    claps = models.IntegerField(default=0)
    objects = models.Manager()  # default manager
    PostObjects = PostObjects()  # custom manager

    class Meta:
        ordering = ('-published',)

    def __str__(self):
        return self.title
