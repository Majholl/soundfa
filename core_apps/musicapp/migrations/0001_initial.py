# Generated by Django 5.1.6 on 2025-02-28 21:37

import core_apps.musicapp.models.albums
import core_apps.musicapp.models.artists
import core_apps.musicapp.models.genres
import core_apps.musicapp.models.musics
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ArtistsModels',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('realname', models.CharField(max_length=64, null=True)),
                ('bio', models.CharField(max_length=256, null=True)),
                ('image', models.ImageField(upload_to=core_apps.musicapp.models.artists.artists_direcrory)),
                ('created_at', models.BigIntegerField(default=core_apps.musicapp.models.artists.nowTimeStamp)),
                ('updated_at', models.BigIntegerField(default=core_apps.musicapp.models.artists.nowTimeStamp)),
            ],
            options={
                'db_table': 'artists',
            },
        ),
        migrations.CreateModel(
            name='MusicModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32)),
                ('duration', models.SmallIntegerField(null=True)),
                ('lyrics', models.TextField(null=True)),
                ('musiccover', models.ImageField(upload_to=core_apps.musicapp.models.musics.music_file_cover)),
                ('musicfile', models.FileField(upload_to=core_apps.musicapp.models.musics.music_file_cover)),
                ('created_at', models.BigIntegerField(default=core_apps.musicapp.models.musics.nowTimeStamp)),
                ('updated_at', models.BigIntegerField(default=core_apps.musicapp.models.musics.nowTimeStamp)),
                ('artist_id', models.ManyToManyField(to='musicapp.artistsmodels')),
            ],
            options={
                'db_table': 'music',
            },
        ),
        migrations.CreateModel(
            name='GenereModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('description', models.CharField(max_length=256)),
                ('generecover', models.FileField(upload_to=core_apps.musicapp.models.genres.genere_file_cover)),
                ('created_at', models.BigIntegerField(default=core_apps.musicapp.models.genres.nowTimeStamp)),
                ('updated_at', models.BigIntegerField(default=core_apps.musicapp.models.genres.nowTimeStamp)),
                ('artist_id', models.ManyToManyField(to='musicapp.artistsmodels')),
                ('music_id', models.ManyToManyField(to='musicapp.musicmodel')),
            ],
            options={
                'db_table': 'genere',
            },
        ),
        migrations.CreateModel(
            name='AlbumModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32)),
                ('totaltracks', models.BigIntegerField()),
                ('description', models.CharField(max_length=256, null=True)),
                ('albumcover', models.FileField(upload_to=core_apps.musicapp.models.albums.album_file_cover)),
                ('created_at', models.BigIntegerField(default=core_apps.musicapp.models.albums.nowTimeStamp)),
                ('updated_at', models.BigIntegerField(default=core_apps.musicapp.models.albums.nowTimeStamp)),
                ('artist_id', models.ManyToManyField(to='musicapp.artistsmodels')),
                ('genre_id', models.ManyToManyField(to='musicapp.generemodel')),
                ('music_id', models.ManyToManyField(to='musicapp.musicmodel')),
            ],
            options={
                'db_table': 'album',
            },
        ),
    ]
