# Generated by Django 5.1.6 on 2025-04-23 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musicapp', '0003_alter_generemodel_album_id_and_more'),
        ('user', '0002_users_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='playlists',
            field=models.ManyToManyField(blank=True, related_name='playlists_users', to='musicapp.playlistmodel'),
        ),
    ]
