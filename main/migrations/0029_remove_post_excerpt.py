# Generated by Django 4.1 on 2022-10-02 10:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0028_alter_post_slug_alter_post_thumbnail'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='excerpt',
        ),
    ]