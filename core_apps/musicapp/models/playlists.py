from django.db import models
from os import path
from loguru import logger
from time import time

from .musics import MusicModel


# -------------------------------------------------------------------
    ### Playlist Model ###

# This model adds playlists for users:
# - Many-to-many relationship with Users
# - Timestamp fields for creation and last update

# -------------------------------------------------------------------




def playlist_file_cover(instance ,filename):
    try:
        
        splitedName = path.splitext(filename)
        fileName = f'{instance.title}_{int(time())}{splitedName[-1]}'
        return path.join('playlists', fileName)
   
    except Exception as err:
        logger.info(f'Error saving playlist cover image name | playlist-id : {instance.pk} | {str(err)}')
        print(f'Error saving playlist cover image name | playlist-id : {instance.pk} | {str(err)}')



class PlaylistModel(models.Model):
    
    title = models.CharField('Playlist title', max_length=32)
    cover = models.FileField('Playlist cover', upload_to=playlist_file_cover, blank=True, null=True)
    public_playlist = models.SmallIntegerField('Public Playlist', default=0)
    
    music_id = models.ManyToManyField(verbose_name='Musics', to=MusicModel, blank=True, related_name='music_id')
    
    totaltracks = models.BigIntegerField('Playlist tracks count', null=True, blank=True)
    description = models.CharField('playlist description', max_length=256, null=True)
    created_at = models.DateTimeField('Creatation datetime', auto_now_add=True)
    updated_at = models.DateTimeField('Last modification', auto_now=True)
    
    class Meta:
        verbose_name = 'playlist'
        db_table = 'playlists'
        ordering = ['-title']
    
    
    def count_totaltracks(self, count):
        self.totaltracks = count
        self.save()
    
    def make_playlist_public(self):
        if self.public_playlist == 0:
            self.public_playlist = 1 
            self.save()
            
            
    def make_playlist_private(self):
        if self.public_playlist == 1:
            self.public_playlist = 0 
            self.save()       
            
                 
    @property 
    def is_playlist_public(self):
        return bool(self.public_playlist == 1)
       
       
    def __str__(self):
        return f'{self.title}'