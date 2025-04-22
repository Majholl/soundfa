from django.db import models
from time import time
from os import path


from .artists import ArtistsModel
from .albums import AlbumModel
from .musics import MusicModel



def genere_file_cover(instance , filename):
    
    try:
        
        splitedName = path.splitext(filename) 
        fileName = f'{instance.name}_{instance.updated_at}{splitedName[-1]}'
        return path.join('generes', fileName)
    
    except Exception as err:
        print(f'Error while editing artist img name : error {str(err)}')



def nowTimeStamp():
    return int(time())


class GenereModel(models.Model):
    
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=256, null=True, blank=True)
    
    artist_id = models.ManyToManyField(to=ArtistsModel, blank=True)
    music_id = models.ManyToManyField(to=MusicModel, blank=True)
    
    album_id = models.ManyToManyField(to=AlbumModel, blank=True)
    generecover = models.FileField(upload_to=genere_file_cover)
    
    created_at = models.BigIntegerField(default=nowTimeStamp)
    updated_at = models.BigIntegerField(default=nowTimeStamp)

    class Meta:
        db_table = 'generes'
        
