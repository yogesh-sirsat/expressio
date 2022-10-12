# Generated by Django 4.1 on 2022-10-10 14:58

from django.db import migrations, models
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0038_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='avatar_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='thumbnail',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, default='', force_format='PNG', keep_meta=True, null=True, quality=75, scale=None, size=(1280, 720), upload_to='posts/thumbnails'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=django_resized.forms.ResizedImageField(crop=['middle', 'center'], force_format='PNG', keep_meta=True, null=True, quality=75, scale=None, size=(360, 360), upload_to='user_profile/avatar'),
        ),
    ]