from django.db import models
from time import time
from os import path
from .artists import ArtistsModels

"""
    -This file is include all fields for the music models 

    ## MusicModel class which have all the fields needed
    ## music_file_cover function which save the given file's in the defined storage

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
    artist_id = models.ManyToManyField(to=ArtistsModels)
    
    musiccover = models.ImageField(upload_to=music_file_cover)
    musicfile = models.FileField(upload_to=music_file_cover)
    
    created_at = models.BigIntegerField(default=nowTimeStamp)
    updated_at = models.BigIntegerField(default=nowTimeStamp)

    class Meta:
        db_table = 'musics'