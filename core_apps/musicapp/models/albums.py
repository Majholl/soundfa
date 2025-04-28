from django.db import models
from time import time
from os import path
from .artists import ArtistsModel
from .musics import MusicModel


"""
    - Model of the albums in MYSQL db
"""

def album_file_cover(instance ,filename):
    try:
        splitedName = path.splitext(filename)
        fileName = f'{instance.title}_{instance.updated_at}{splitedName[-1]}'
        return path.join('albums', fileName)
    except Exception as err:
        print(f'Error while editting album img name : error {str(err)}')


def nowTimeStamp():
    return int(time())


class AlbumModel(models.Model):
    
    title = models.CharField(max_length=32)
    albumcover = models.FileField(upload_to=album_file_cover)

    artist_id = models.ManyToManyField(to=ArtistsModel, blank=True)
    music_id = models.ManyToManyField(to=MusicModel, blank=True)
    
    totaltracks = models.BigIntegerField(null=True, blank=True)
    description = models.CharField(max_length=256, null=True)
    
    created_at = models.BigIntegerField(default=nowTimeStamp)
    updated_at = models.BigIntegerField(default=nowTimeStamp)

    class Meta :
        db_table = 'albums'