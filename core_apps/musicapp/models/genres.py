from django.db import models

from time import time
from os import path
from loguru import logger


from .artists import ArtistsModel
from .albums import AlbumModel
from .musics import MusicModel
from .playlists import PlaylistModel


# -------------------------------------------------------------------
    ### Genere Model ###

# This model adds genere for artists, musics and albums and playlist:
# - Many-to-many relationship with artist, musics, albums, playlist
# - Timestamp fields for creation and last update

# -------------------------------------------------------------------



def genere_file_cover(instance , filename):
    
    try:
        
        splitedName = path.splitext(filename) 
        fileName = f'{instance.name}_{int(time())}{splitedName[-1]}'
        return path.join('generes', fileName)
    
    except Exception as err:
        logger.info(f'Error saving album cover image name | album-id : {instance.pk} | {str(err)}')
        print(f'Error saving album cover image name | album-id : {instance.pk} | {str(err)}')





class GenereModel(models.Model):
    
    name = models.CharField('Genere name', max_length=32)
    description = models.CharField('Genere description', max_length=256, null=True, blank=True)
    
    artist_id = models.ManyToManyField(verbose_name='Artists', to=ArtistsModel, related_name='gerene_artists', blank=True)
    music_id = models.ManyToManyField(verbose_name='Musics', to=MusicModel, related_name='genere_musics', blank=True )
    album_id = models.ManyToManyField(verbose_name='Albums', to=AlbumModel, related_name='genere_albums', blank=True)
    playlist_id = models.ManyToManyField(verbose_name='Playlists', to=PlaylistModel, related_name='genere_playlists', blank=True)
    
    cover = models.FileField(verbose_name='Genere cover', upload_to=genere_file_cover)
    created_at = models.DateTimeField('Creatation datetime', auto_now_add=True)
    updated_at = models.DateTimeField('Last modification', auto_now=True)
    
    
    class Meta:
        verbose_name = 'Genere'
        db_table = 'generes'
        ordering = ['-name']
         
         
    def __str__(self):
        return f'{self.name}'       
