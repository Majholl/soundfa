from django.db import models
from time import time
from os import path
from .artists import ArtistsModels
from .musics import MusicModel
from .genres import GenereModel

"""
    -This file is include all fields for the albums models 

    ## AlbumModel class which have all the fields needed
    ## album_file_cover function which save the given file's in the defined storage


"""
def album_file_cover(instance ,filename):
    try:
        splitedName = path.splitext(filename)
        fileName = f'{instance.title}_{instance.updated_at}{splitedName[-1]}'
        return path.join('albums', fileName)
    except Exception as err:
        print(f'Error while editting music img name : error {str(err)}')


def nowTimeStamp():
    return int(time())


class AlbumModel(models.Model):
    
    title = models.CharField(max_length=32)
    albumcover = models.FileField(upload_to=album_file_cover)

    artist_id = models.ManyToManyField(to=ArtistsModels, blank=True)
    music_id = models.ManyToManyField(to=MusicModel, blank=True)
    
    
    genre_id = models.ManyToManyField(to=GenereModel, blank=True)
    totaltracks = models.BigIntegerField(null=True, blank=True)
    description = models.CharField(max_length=256, null=True)
    
    albumtype = models.SmallIntegerField(default=1)
    
    created_at = models.BigIntegerField(default=nowTimeStamp)
    updated_at = models.BigIntegerField(default=nowTimeStamp)

    class Meta :
        db_table = 'albums'