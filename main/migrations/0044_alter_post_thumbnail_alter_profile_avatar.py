# Generated by Django 4.1 on 2023-10-16 15:52

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0043_alter_profile_bio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='thumbnail',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, force_format='PNG', keep_meta=True, null=True, quality=75, scale=None, size=(1280, 720), upload_to='media/posts/thumbnails'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=django_resized.forms.ResizedImageField(crop=['middle', 'center'], force_format='PNG', keep_meta=True, null=True, quality=75, scale=None, size=(360, 360), upload_to='media/user_profile/avatar'),
        ),
    ]
