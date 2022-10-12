# Generated by Django 4.1 on 2022-10-11 09:55

from django.db import migrations, models
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0039_profile_avatar_url_alter_post_thumbnail_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='source',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='thumbnail_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='thumbnail',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, force_format='PNG', keep_meta=True, null=True, quality=75, scale=None, size=(1280, 720), upload_to='posts/thumbnails'),
        ),
    ]