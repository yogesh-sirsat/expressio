# Generated by Django 4.1 on 2022-10-02 15:06

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0030_alter_post_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='thumbnail',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, default='', force_format='JPEG', keep_meta=True, null=True, quality=75, scale=None, size=(1280, 720), upload_to='posts/thumbnails'),
        ),
    ]
