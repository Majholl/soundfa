from django.db import models
from time import time
from os import path
from .artists import ArtistsModels
# from .albums import AlbumModel
from .musics import MusicModel

def genere_file_cover(instance , filename):
    return path.join(instance.name , filename)

def nowTimeStamp():
    return int(time())


class GenereModel(models.Model):
    
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=256)
    
    artist_id = models.ManyToManyField(to=ArtistsModels)
    music_id = models.ManyToManyField(to=MusicModel)
    # album_id = models.ManyToManyField(to=AlbumModel, null=True)
    
    generecover = models.FileField(upload_to=genere_file_cover)
    created_at = models.BigIntegerField(default=nowTimeStamp)
    
    updated_at = models.BigIntegerField(default=nowTimeStamp)

    class Meta:
        db_table = 'genere'
        
