from django.db import models
from time import time
from os import path
from .artists import ArtistsModel

"""
    - Model of the musics in MYSQL db
"""


def music_file_cover(instance , filename):
    try:
        splitedName = path.splitext(filename)
        fileName = f'{instance.title}_{instance.updated_at}{splitedName[-1]}'
        return path.join('musics', fileName)
    except Exception as err:
        print(f'Error while editting music img name : error {str(err)}')


def nowTimeStamp():
    return int(time())


class MusicModel(models.Model):
    
    title = models.CharField(max_length=32)
    duration = models.CharField(max_length=32, null=True)
    
    lyrics = models.TextField(null=True)
    artist_id = models.ManyToManyField(to=ArtistsModel)
    
    musiccover = models.ImageField(upload_to=music_file_cover)
    musicfile = models.FileField(upload_to=music_file_cover)
    
    created_at = models.BigIntegerField(default=nowTimeStamp)
    updated_at = models.BigIntegerField(default=nowTimeStamp)

    class Meta:
        db_table = 'musics'