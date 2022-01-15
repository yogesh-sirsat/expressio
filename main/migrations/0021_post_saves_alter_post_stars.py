# Generated by Django 4.0 on 2022-01-15 20:00

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0020_alter_post_stars'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='saves',
            field=models.ManyToManyField(null=True, related_name='post_saves', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='post',
            name='stars',
            field=models.ManyToManyField(null=True, related_name='post_stars', to=settings.AUTH_USER_MODEL),
        ),
    ]
