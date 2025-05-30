# Generated by Django 5.1.6 on 2025-05-06 17:57

import core_apps.user.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musicapp', '0004_alter_artistsmodel_options'),
        ('user', '0007_users_account_status_users_reset_password_attempt_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='users',
            options={'ordering': ['-created_at'], 'verbose_name': 'User'},
        ),
        migrations.AlterField(
            model_name='users',
            name='account_status',
            field=models.CharField(choices=[('active', 'Active'), ('deactive', 'Deactive'), ('locked', 'Locked')], default='active', max_length=8, verbose_name='Account status'),
        ),
        migrations.AlterField(
            model_name='users',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='User creatation datetime'),
        ),
        migrations.AlterField(
            model_name='users',
            name='email',
            field=models.EmailField(db_index=True, max_length=254, unique=True, verbose_name='Email address'),
        ),
        migrations.AlterField(
            model_name='users',
            name='playlists',
            field=models.ManyToManyField(blank=True, related_name='playlists_users', to='musicapp.playlistmodel', verbose_name='Playlist'),
        ),
        migrations.AlterField(
            model_name='users',
            name='profile',
            field=models.ImageField(blank=True, upload_to=core_apps.user.models.profile_file_cover, verbose_name='User profile'),
        ),
        migrations.AlterField(
            model_name='users',
            name='reset_password',
            field=models.CharField(max_length=6, null=True, verbose_name='Reset password'),
        ),
        migrations.AlterField(
            model_name='users',
            name='reset_password_attempt',
            field=models.IntegerField(default=0, verbose_name='Reset password attempt'),
        ),
        migrations.AlterField(
            model_name='users',
            name='reset_password_expire_time',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Reset password expiration time'),
        ),
        migrations.AlterField(
            model_name='users',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Last modification of user'),
        ),
        migrations.AlterField(
            model_name='users',
            name='usertype',
            field=models.CharField(choices=[('user', 'User'), ('admin', 'Admin'), ('superadmin', 'Superadmin')], default='user', max_length=10, verbose_name='User type'),
        ),
    ]
