# Generated by Django 4.0 on 2022-01-01 17:42

from django.db import migrations, models
import django.db.models.deletion
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('main', '0007_delete_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', django_resized.forms.ResizedImageField(crop=None, default='user_profile/avatar/default_user_avatar.jpg', force_format='JPEG', keep_meta=True, quality=75, size=(360, 480), upload_to='user_profile/avatar')),
                ('bio', models.TextField(max_length=500, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
        ),
    ]