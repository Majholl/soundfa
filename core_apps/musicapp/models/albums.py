from django.db import models
from time import time
from os import path
from .artists import ArtistsModels
from .musics import MusicModel
from .genres import GenereModel


def album_file_cover(instance ,filename):
    return path.join(instance.title, filename)


def nowTimeStamp():
    return int(time())


class AlbumModel(models.Model):
    
    title = models.CharField(max_length=32)
    artist_id = models.ManyToManyField(to=ArtistsModels)
    
    music_id = models.ManyToManyField(to=MusicModel)
    genre_id = models.ManyToManyField(to=GenereModel)
    
    totaltracks = models.BigIntegerField()
    description = models.CharField(max_length=256, null=True)
    
    albumcover = models.FileField(upload_to=album_file_cover)
    created_at = models.BigIntegerField(default=nowTimeStamp)
    
    updated_at = models.BigIntegerField(default=nowTimeStamp)

    class Meta :
        db_table = 'album'