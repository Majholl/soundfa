from django.db import models
from os import path
from time import time

from .musics import MusicModel


"""
    -This file is include all fields for the playlists models 

    ## playlists class which have all the fields needed
    ## playlist_file_cover function which save the given file's in the defined storage

"""



def playlist_file_cover(instance ,filename):
    try:
        splitedName = path.splitext(filename)
        fileName = f'{instance.title}_{instance.updated_at}{splitedName[-1]}'
        return path.join('playlists', fileName)
    except Exception as err:
        print(f'Error while editting playlist img name : error {str(err)}')


def nowTimeStamp():
    return int(time())


class PlaylistModel(models.Model):
    
    title = models.CharField(max_length=32)
    music_id = models.ManyToManyField(to=MusicModel, blank=True)
    
    playlistcover = models.FileField(upload_to=playlist_file_cover)
    totaltracks = models.BigIntegerField(null=True, blank=True)
    
    description = models.CharField(max_length=256, null=True)
    created_at = models.BigIntegerField(default=nowTimeStamp)
    
    updated_at = models.BigIntegerField(default=nowTimeStamp)

    
    class Meta:
        db_table = 'playlists'