# Generated by Django 4.1 on 2022-10-11 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0040_post_source_post_thumbnail_url_alter_post_thumbnail'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='description',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
